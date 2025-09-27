from typing import AsyncGenerator, Optional, Any, Dict
import json
import aiohttp
from .base import BaseAIAdapter, Message, MemoryScope
from .memory import MemoryManager
import prerequisites.prerequisite as presets_tool

class DeepseekAdapter(BaseAIAdapter):
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.memory_manager = MemoryManager()
        self._memory_scope = MemoryScope.GLOBAL
        self.current_preset = ""
        
    @property
    def memory_scope(self) -> MemoryScope:
        return self._memory_scope
        
    @memory_scope.setter
    def memory_scope(self, scope: MemoryScope):
        self._memory_scope = scope
        
    async def generate_response(
        self,
        messages: list[Message],
        context_id: str,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        try:
            # Get system prompt from presets
            system_prompt = presets_tool.gen_presets(
                kwargs.get("uid", 0),
                kwargs.get("bot_name", "小依"),
                kwargs.get("event_user", "用户")
            )
            
            # Prepare messages for API
            api_messages = []
            
            # Add system message from preset
            if system_prompt:
                api_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
                
            # Add conversation messages
            for msg in messages:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
                
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": api_messages,
                "stream": True,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000)
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Deepseek API error: {error_text}")
                        
                    async for line in response.content:
                        if line:
                            try:
                                line = line.decode('utf-8').strip()
                                if line.startswith('data: '):
                                    line = line[6:]  # Remove 'data: ' prefix
                                    if line == '[DONE]':
                                        break
                                        
                                    chunk = json.loads(line)
                                    if 'choices' in chunk and len(chunk['choices']) > 0:
                                        delta = chunk['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            content = delta['content']
                                            # Create assistant message for memory
                                            assistant_msg = Message(
                                                role="assistant",
                                                content=content
                                            )
                                            # Add to memory
                                            self.add_to_memory(context_id, assistant_msg)
                                            yield content
                                            
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
            
    async def clear_memory(self, context_id: str):
        """Clear memory for the given context."""
        await self.memory_manager.clear_memory(context_id, self.memory_scope)
        
    def get_memory(self, context_id: str) -> list[Message]:
        """Get memory for the given context."""
        return self.memory_manager.get_memory(context_id, self.memory_scope)
        
    def add_to_memory(self, context_id: str, message: Message):
        """Add a message to memory."""
        self.memory_manager.add_to_memory(context_id, message, self.memory_scope)
        
    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding for the given text."""
        # Deepseek doesn't support embeddings directly
        # Return a dummy embedding
        return [0.0] * 1536  # Standard embedding size 