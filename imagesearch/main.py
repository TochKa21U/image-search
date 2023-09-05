from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def entry_point():
    return JSONResponse(content={"Version":"0.0.1","status":"development"})

# WILL DO UPLOAD PICTURE
# FIND SIMILARITY