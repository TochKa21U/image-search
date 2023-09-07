# This file will contain config and initiation of vector db
import weaviate
import base64
from weaviate.util import generate_uuid5
from os import environ,getenv

WEAVIATEADDR=getenv("VECTORDBADDR","weaviate")
print(f"Weaviate Address : {WEAVIATEADDR}")
client_db = weaviate.Client(f"http://{WEAVIATEADDR}:8080")

# Test connection
client_db.schema.get()

CLASSNAME = "Clothes"

db_schema = {
    "classes": [
        {
            "class": CLASSNAME,
            "vectorizer": "img2vec-neural",
            "vectorIndexType": "hnsw",
            "moduleConfig": {
                "img2vec-neural": {
                    "imageFields": [
                        'image'
                    ]
                }
            },
            "properties": [
                {
                    "name": "image",
                    "dataType": ["blob"]
                },
                {
                    "name": "text",
                    "dataType": ["string"]
                }
            ]
        }
    ]
}


# Check if class already exists
def class_exists(class_name):
    schema = client_db.schema.get()
    for cls in schema.get('classes', []):
        if cls['class'] == class_name:
            return True
    return False

# Apply a database schema only if it doesn't exist
if not class_exists(CLASSNAME):
    client_db.schema.create(db_schema)
else:
    print(f"Class '{CLASSNAME}' already exists.")


# Will be used for encoding images to base64
base64encoder = lambda x : base64.b64encode(x).decode("utf-8")
# Base 64 decoder
binary_data = lambda x : base64.b64decode(x)

def  add_pictures_to_db(input_image,image_description=""):
    img_b64 = base64encoder(input_image)
    payload = {
        "image":img_b64,
        "text": image_description
    }
    uuid_value = generate_uuid5(payload, CLASSNAME)
    with client_db.batch as batch:
        batch.add_data_object(
            class_name=CLASSNAME,
            data_object=payload,
            uuid= uuid_value
        )
    return uuid_value

def delete_object_by_uuid(uuid_value):
    client_db.data_object.delete(uuid=uuid_value)


def search_similar_to_uuid(uuid_value):
    # Get only two for a purpose
    results = client_db.query.get(
        class_name=CLASSNAME,
        properties=["image", "text"],
    ).with_near_object({
        "id": uuid_value
    }).with_limit(2).with_additional(["id","distance"]).do()
    # First item is itself, second item is closest one
    return results # Only return closest item