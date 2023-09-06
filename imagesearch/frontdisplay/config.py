import gradio as gr
from PIL import Image
from imagesearch.vectordb.config import add_pictures_to_db,search_similar_to_uuid,delete_object_by_uuid, CLASSNAME
import io
import base64

def image_to_base64(pil_image):
    """Convert PIL Image to base64 encoded string."""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def base64_to_image(base64_string):
    """Convert base64 string to PIL Image."""
    image_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_bytes))

def predict_image(input_image):
    # Convert input image (PIL Image) to base64
    img_b64 = image_to_base64(input_image)
    # Add picture to db
    tmpfile = add_pictures_to_db(img_b64, "gradio_input")
    
    # similarity search
    results = search_similar_to_uuid(tmpfile)

    # delete after search is done
    delete_object_by_uuid(tmpfile)

    # Check for erros
    if 'errors' in results:
        raise gr.Error("Error occured during processing of the image")
    
    foundImage = results['data']['Get'][f"{CLASSNAME}"][-1].get('image')

    return base64_to_image(foundImage)

iface = gr.Interface(fn=predict_image,inputs="image",outputs="image")