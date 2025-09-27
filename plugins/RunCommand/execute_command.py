def execute_command(command, subprocess):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        # capture_output=True 捕获输出(stdout/stderr)
        # text=True  解码为文本字符串,可以返回text
        # check=True  当返回非零退出码时引发 CalledProcessError 异常，开不开差不多（）
        # shell=True  允许使用 shell 的特性，不建议开

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    except subprocess.CalledProcessError as e:
        return {
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }
    except Exception as e:
        return {
            "stdout": None,
            "stderr": str(e),
            "returncode": -1
        }      