import imp
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from imagesearch.vectordb.config import delete_object_by_uuid, search_similar_to_uuid, add_pictures_to_db, delete_object_by_uuid
from io import BytesIO

app = FastAPI()

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
async def search_file(file: UploadFile = File(...), description: str = Form("")):
    # Convert the file to bytes
    contents = await file.read()

    tmpfile = add_pictures_to_db(contents, description)
    
    # similarity search
    results = search_similar_to_uuid(tmpfile)

    # delete after search is done
    delete_object_by_uuid(tmpfile)
    
    # Return the results
    return {"filename": file.filename, "description": description, "search_results": results}

@app.get("/")
def entry_point():
    return JSONResponse(content={"Version":"0.0.1","status":"development"})

# WILL DO UPLOAD PICTURE
# FIND SIMILARITY