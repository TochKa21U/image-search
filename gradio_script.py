import gradio as gr
from PIL import Image
from imagesearch.vectordb.config import add_pictures_to_db,search_similar_to_uuid,delete_object_by_uuid, CLASSNAME
import io
import base64

import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("This is a debug message")


# def image_to_base64(pil_image):
#     """Convert PIL Image to base64 encoded string."""
#     buffered = io.BytesIO()
#     pil_image.save(buffered, format="JPEG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     return img_str
def image_to_base64(pil_image):
    """Convert PIL Image to base64 encoded bytes."""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())

def base64_to_image(base64_string):
    """Convert base64 string to PIL Image."""
    image_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_bytes))

def image_to_bytes(pil_image):
    """Convert PIL Image to bytes."""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return buffered.getvalue()


def predict_image(input_image):
    # Convert input image (PIL Image) to base64
    # Check data type
    print(type(input_image))
    converted_image = image_to_bytes(input_image)
    # print(f"Converted : {converted_image}")
    
    # img_b64 = image_to_base64(input_image)
    # # Add picture to db
    tmpfile = add_pictures_to_db(converted_image, "gradio_input")
    logging.debug(f"Tmp file : {type(tmpfile)}")
    logging.debug(tmpfile)
    # similarity search
    results = search_similar_to_uuid(tmpfile)

    # delete after search is done
    delete_object_by_uuid(tmpfile)

    # Check for erros
    if 'errors' in results:
        raise gr.Error("Error occured during processing of the image")
    
    foundImage = results['data']['Get'][f"{CLASSNAME}"][-1].get('image')
    logging.debug(f"Found image results : {foundImage}")
    print(f"Found image results : {foundImage}")
    # return "Current627875b8be6c"
    return base64_to_image(foundImage)

# iface = gr.Interface(fn=predict_image,inputs=gr.inputs.Image(type="bytes", label="Upload Image"),outputs=gr.outputs.Image(type="pil", label="Most Similar Image"))
iface = gr.Interface(fn=predict_image,inputs=gr.inputs.Image(type="pil", label="Upload Image"),outputs=gr.outputs.Image(type="pil", label="Most Similar Image"))

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860,debug=True)
