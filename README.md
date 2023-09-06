# image-search
## Image Search For Similarities

This project is for searching similar images in given dataset for user input.

User input will be PNG or JPG/JPEG images.


## Stack

API will be served on FastAPI by default on 8888 port
Weaviate Vector DB will be used for storing vector embeddings
PyTorch based model will be responsible for Vector Embeddings(Resnet50) / VIT
Both Outcome will be tested and fastest and acceptable enough will be deployed
Cross Product will be used to compute the similarities

All this application will be also wrapped in Gradio as well for frontend display


## Other
This application might be hosted on HuggingFace Spaces as well for quick showcase demo
Example dataset might be linked somewhere in here in readme file
Explanation or Quick start part will be written

## Documentation
Please visit /docs the see Swagger documentation