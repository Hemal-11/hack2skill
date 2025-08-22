from google.cloud import vision_v1

# Use an async client
client = vision_v1.ImageAnnotatorAsyncClient()

async def analyze_image_from_gcs(gcs_uri: str) -> dict:
    """Analyzes an image in GCS using the Vision API."""
    image = vision_v1.Image()
    image.source.image_uri = gcs_uri

    features = [
        vision_v1.Feature(type_=vision_v1.Feature.Type.LABEL_DETECTION, max_results=10),
        vision_v1.Feature(type_=vision_v1.Feature.Type.IMAGE_PROPERTIES), # For dominant colors
    ]

    # Build a single request object
    request = vision_v1.AnnotateImageRequest(image=image, features=features)

    # --- THE FIX: Use the batch method, which is more robust ---
    # We pass a list containing our single request.
    response = await client.batch_annotate_images(requests=[request])

    # The result is a list of responses, so we take the first one.
    first_result = response.responses[0]

    if first_result.error.message:
        raise Exception(f"Vision API Error: {first_result.error.message}")

    # --- Parse the results from the 'first_result' object ---
    labels = [label.description for label in first_result.label_annotations]

    colors_info = first_result.image_properties_annotation.dominant_colors.colors
    colors = [
        {"red": int(color.color.red), "green": int(color.color.green), "blue": int(color.color.blue), "score": color.score}
        for color in colors_info
    ]

    return {"labels": labels, "colors": sorted(colors, key=lambda c: c['score'], reverse=True)}