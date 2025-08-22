from google.cloud import vision_v1
from google.cloud.vision_v1.types import Image, Feature

# Use an async client
client = vision_v1.ImageAnnotatorAsyncClient()

async def analyze_image_from_gcs(gcs_uri: str) -> dict:
    """Analyzes an image in GCS using the Vision API."""
    image = Image()
    image.source.image_uri = gcs_uri

    features = [
        Feature(type_=Feature.Type.LABEL_DETECTION, max_results=10),
        Feature(type_=Feature.Type.IMAGE_PROPERTIES), # For dominant colors
    ]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    
    response = await client.annotate_image(request=request)
    
    # --- Parse the response ---
    labels = [label.description for label in response.label_annotations]
    
    colors_info = response.image_properties_annotation.dominant_colors.colors
    colors = [
        {"red": color.color.red, "green": color.color.green, "blue": color.color.blue, "score": color.score}
        for color in colors_info
    ]
    
    return {"labels": labels, "colors": sorted(colors, key=lambda c: c['score'], reverse=True)}