from typing import AsyncGenerator, Optional, Any, Dict
import google.generativeai as genai
from .base import BaseAIAdapter, Message, MemoryScope
from .memory import MemoryManager

class GeminiAdapter(BaseAIAdapter):
    """Gemini AI adapter implementation."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """Initialize Gemini adapter.
        
        Args:
            api_key: Google API key
            model: Model name (default: gemini-pro)
        """
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.memory_manager = MemoryManager()
        self._memory_scope = MemoryScope.USER
        
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
        """Generate a response using Gemini API."""
        try:
            # Prepare messages for API
            chat = self.model.start_chat(history=[])
            
            # Add messages to chat
            for msg in messages:
                if msg.role == "user":
                    chat.send_message(msg.content)
                elif msg.role == "assistant":
                    # Gemini doesn't support assistant messages in history
                    continue
                    
            # Generate response
            response = chat.send_message(
                messages[-1].content,
                stream=True,
                generation_config=kwargs.get("generation_config", {})
            )
            
            # Stream the response
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
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
        # Gemini doesn't support embeddings directly
        # Return a dummy embedding
        return [0.0] * 1536  # Standard embedding size 