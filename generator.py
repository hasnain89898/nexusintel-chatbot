"""Embedding generation using OpenAI."""

import logging
from openai import OpenAI
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingGenerator:
    """Generates vector embeddings using OpenAI API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
    
    def generate(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []
        
        # OpenAI has a limit on batch size, process in batches
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Clean empty strings
            batch = [t if t.strip() else "empty" for t in batch]
            
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)
                logger.info(f"Generated {len(embeddings)} embeddings (batch {i // batch_size + 1})")
            except Exception as e:
                logger.error(f"Embedding generation failed: {e}")
                raise
        
        return all_embeddings
    
    def generate_single(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        result = self.generate([text])
        return result[0] if result else []
