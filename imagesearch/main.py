import imp
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from imagesearch.vectordb.config import delete_object_by_uuid, search_similar_to_uuid, add_pictures_to_db, delete_object_by_uuid, binary_data, CLASSNAME
from io import BytesIO
import threading

app = FastAPI(title="Image Similarty Search",description="Image search with Vector Database, using ResNet50 for Vector embeddings generation",version="0.1.0")

# To handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# The Upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), description: str = Form("")):
    # Convert the file to bytes
    contents = await file.read()

    # Then, add the image to the database
    add_pictures_to_db(contents, description)
    
    return {"filename": file.filename, "description": description}


# The Search endpoint
@app.post("/search/")
async def search_file(file: UploadFile = File(...), description: str = Form(""), fullresult: bool = Form(True)):
    # Convert the file to bytes
    contents = await file.read()

    tmpfile = add_pictures_to_db(contents, description)
    
    # similarity search
    results = search_similar_to_uuid(tmpfile)

    # delete after search is done
    delete_object_by_uuid(tmpfile)
    """
    IDEA
    Get File UUID as well
    Return it to here where file url will be displayed in the file uuid link
    """
    if 'errors' in results:
        return results
    # Filter unnecessary
    closest_result = results['data']['Get'][f"{CLASSNAME}"][-1]
    if not fullresult:
        return {"filename": file.filename, "similar_category": closest_result.get('text'),"image":f"/get-image/{closest_result.get('_additional').get('id')}"}
    # Return the results
    return {"filename": file.filename, "similar_category": closest_result.get('text'),"image":f"/get-image/{closest_result.get('_additional').get('id')}" ,"search_results": closest_result}

@app.get("/get-image/{image_id}")
async def get_image(image_id: str):
    found_image = search_similar_to_uuid(image_id)
    img_base64_format = found_image['data']['Get'][f"{CLASSNAME}"][-1].get('image')
    # Assuming `base64_string` is the fetched image in base64 format
    bin_image = binary_data(img_base64_format)
    
    return StreamingResponse(BytesIO(bin_image), media_type="image/jpeg")

@app.get("/")
def entry_point():
    return JSONResponse(content={"Version":"0.1.0","status":"development","docs/swagger":"/docs"})

# GRADIO WILL BE HOSTED ON DIFFERENT CONTAINER
# will also add detailed description about how to run and architecture