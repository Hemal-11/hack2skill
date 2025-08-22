from PIL import Image, ImageEnhance, ImageFilter
import io

def local_enhance_image(image_bytes: bytes) -> bytes:
    """
    Applies a basic auto-contrast and sharpening filter to an image.
    Serves as a fallback for the Vertex AI Imagen enhancer.
    """
    img = Image.open(io.BytesIO(image_bytes))
    
    # 1. Auto-contrast to improve dynamic range
    # This specific function is not in Pillow, but we can simulate it with Contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2) # Increase contrast by 20%
    
    # 2. Sharpen the image
    img = img.filter(ImageFilter.SHARPEN)
    
    # Save the enhanced image back to bytes
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    return byte_arr.getvalue()