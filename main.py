# This is where the server file will be initiated
import os
import uvicorn
# from dotenv import load_dotenv


# load_dotenv() # Load dot env variables

PORT = 8888

if __name__ == '__main__':
    uvicorn.run("imagesearch.main:app",port=PORT,log_level="info",reload=True) 