import logging
from google.api_core.exceptions import GoogleAPICallError
from vertexai.generative_models import GenerativeModel, GenerationConfig
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexTextGenerator:
    """
    A wrapper for Vertex AI's Generative Models (Gemini).
    Handles text generation tasks like the artisan storyteller.
    """

    def __init__(self, model_name: str = settings.GEMINI_MODEL_ID):
        """Initializes the Vertex AI client and model."""
        try:
            self.model = GenerativeModel(model_name)
            logger.info(f"Successfully initialized Vertex AI model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI model: {e}", exc_info=True)
            raise

    @retry(wait=wait_exponential(multiplier=1, min=2, max=6), stop=stop_after_attempt(3))
    async def generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """
        A general-purpose method to generate text from a system and user prompt.
        """
        try:
            logger.info("Generating content with Vertex AI Gemini...")
            generation_config = GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                max_output_tokens=1024,
            )
            
            response = await self.model.generate_content_async(
                [system_prompt, user_prompt],
                generation_config=generation_config
            )
            
            generated_text = response.text.strip()
            logger.info("Successfully generated content.")
            return generated_text

        except Exception as e:
            logger.error(f"An unexpected error occurred during content generation: {e}", exc_info=True)
            raise

    # The original storyteller method can also use the new generic one, or stay as is.
    # For simplicity, we will keep it separate for now.
   

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def generate_story_from_prompts(self, artisan_heritage: str, piece_story: str) -> str:
        """
        Generates a polished product story from two prompts using Gemini.

        Args:
            artisan_heritage: The artisan's background and craft context.
            piece_story: The story behind the specific item.

        Returns:
            A single, cohesive story as a string.
        """
        system_prompt = """
        You are an expert storyteller for an artisan marketplace. Your task is to weave together two distinct pieces of information from an artisan into a single, elegant, and compelling product description.

        **Your Goal:**
        1.  **Preserve the Artisan's Voice:** Do not invent facts or use overly corporate language. The tone should feel authentic, personal, and reflect the spirit of the provided text.
        2.  **Combine Seamlessly:** Create a smooth narrative that flows naturally from the artisan's heritage to the story of the specific piece.
        3.  **Be Eloquent:** Elevate the language slightly to make it more engaging for a buyer, but avoid making it sound generic.
        4.  **Format for Readability:** Use paragraphs to structure the story. Start by introducing the artisan and their craft, then transition to the unique story of the item.
        """

        user_prompt = f"""
        Here is the information from the artisan. Please create a product story.

        **Part 1: About the Artisan & Their Heritage**
        "{artisan_heritage}"

        **Part 2: The Story of This Specific Piece**
        "{piece_story}"
        """

        try:
            logger.info("Generating story with Vertex AI Gemini...")
            # Configuration for creative but controlled output
            generation_config = GenerationConfig(
                temperature=0.4,
                top_p=0.95,
                top_k=40,
                max_output_tokens=1024,
            )
            
            # Use async generation
            response = await self.model.generate_content_async(
                [system_prompt, user_prompt],
                generation_config=generation_config
            )
            
            generated_text = response.text.strip()
            logger.info("Successfully generated story.")
            return generated_text

        except GoogleAPICallError as e:
            logger.error(f"Google API call error during story generation: {e}", exc_info=True)
            raise  # Re-raise to be handled by the endpoint
        except Exception as e:
            logger.error(f"An unexpected error occurred during story generation: {e}", exc_info=True)
            raise

# Singleton instance to be used across the application
vertex_text_client = VertexTextGenerator()