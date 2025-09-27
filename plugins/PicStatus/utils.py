import asyncio
import platform
import psutil
import re
import time
from datetime import datetime
from typing import Dict, List, Optional
import aiohttp
from .config import config

class SystemInfo:
    @staticmethod
    def get_cpu_info() -> Dict:
        """获取CPU信息"""
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    @staticmethod
    def get_memory_info() -> Dict:
        """获取内存信息"""
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024 * 1024 * 1024), 2),  # GB
            "used": round(mem.used / (1024 * 1024 * 1024), 2),    # GB
            "percent": mem.percent
        }
    
    @staticmethod
    def get_disk_info() -> List[Dict]:
        """获取磁盘信息"""
        disks = []
        for part in psutil.disk_partitions():
            if any(re.match(pattern, part.mountpoint) for pattern in config.IGNORE_DISK_PARTS):
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "total": round(usage.total / (1024 * 1024 * 1024), 2),  # GB
                    "used": round(usage.used / (1024 * 1024 * 1024), 2),    # GB
                    "percent": usage.percent
                })
            except:
                continue
        return disks
    
    @staticmethod
    def get_network_info() -> List[Dict]:
        """获取网络信息"""
        nets = []
        for name, stats in psutil.net_io_counters(pernic=True).items():
            if any(re.match(pattern, name) for pattern in config.IGNORE_NETWORK_INTERFACES):
                continue
            if stats.bytes_sent == 0 and stats.bytes_recv == 0 and config.IGNORE_0B_NET:
                continue
            nets.append({
                "name": name,
                "bytes_sent": round(stats.bytes_sent / (1024 * 1024), 2),  # MB
                "bytes_recv": round(stats.bytes_recv / (1024 * 1024), 2)   # MB
            })
        return nets
    
    @staticmethod
    def get_process_info() -> List[Dict]:
        """获取进程信息"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if any(re.match(pattern, proc.info['name']) for pattern in config.IGNORE_PROCESSES):
                    continue
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": round(proc.info['memory_percent'], 1)
                })
            except:
                continue
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:config.PROCESS_LIMIT]
    
    @staticmethod
    def get_system_info() -> Dict:
        """获取系统基本信息"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = time.time() - psutil.boot_time()
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": f"{hours}小时{minutes}分钟"
        }

class NetworkTester:
    @staticmethod
    async def test_site(session: aiohttp.ClientSession, site: Dict) -> Dict:
        """测试网站连接"""
        start_time = time.time()
        try:
            async with session.get(site['url'], timeout=config.TEST_TIMEOUT) as resp:
                if resp.status == 200:
                    return {
                        "name": site['name'],
                        "url": site['url'],
                        "status": "正常",
                        "time": round((time.time() - start_time) * 1000, 2)  # ms
                    }
        except:
            pass
        return {
            "name": site['name'],
            "url": site['url'],
            "status": "异常",
            "time": 0
        }
    
    @staticmethod
    async def test_all_sites() -> List[Dict]:
        """测试所有配置的网站"""
        async with aiohttp.ClientSession() as session:
            tasks = [NetworkTester.test_site(session, site) for site in config.TEST_SITES]
            return await asyncio.gather(*tasks)

class InfoCollector:
    @staticmethod
    async def collect_all() -> Dict:
        """收集所有系统信息"""
        system_info = SystemInfo()
        network_tester = NetworkTester()
        
        # 并行收集信息
        system_basic, cpu_info, memory_info, disk_info, network_info, process_info, network_test = await asyncio.gather(
            asyncio.to_thread(system_info.get_system_info),
            asyncio.to_thread(system_info.get_cpu_info),
            asyncio.to_thread(system_info.get_memory_info),
            asyncio.to_thread(system_info.get_disk_info),
            asyncio.to_thread(system_info.get_network_info),
            asyncio.to_thread(system_info.get_process_info),
            network_tester.test_all_sites()
        )
        
        return {
            "system": system_basic,
            "cpu": cpu_info,
            "memory": memory_info,
            "disk": disk_info,
            "network": network_info,
            "process": process_info,
            "network_test": network_test
        } 