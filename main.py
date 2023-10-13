import os
import pymongo
import requests

mongo_host = os.environ.get("MONGO_HOST")
mongo_port = os.environ.get("MONGO_PORT")
mongo_db = os.environ.get("MONGO_DB_NAME")
mongo_user = os.environ.get("MONGO_USER")
mongo_password = os.environ.get("MONGO_PASSWORD")

pictrs_protocol = os.environ.get("PICTRS_PROTOCOL")
pictrs_host = os.environ.get("PICTRS_HOST")
pictrs_port = os.environ.get("PICTRS_PORT")

# Connect to MongoDB
if mongo_user and mongo_password:
    client = pymongo.MongoClient(f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}")
else:
    client = pymongo.MongoClient(f"mongodb://{mongo_host}:{mongo_port}")

db = client[mongo_db]
collection = db["images"]

for image in collection.find():
    musicbrainzid = image["musicbrainzid"]
    image_name = image["image"]
    image_extension = image_name.split(".")[-1]
    pictrs_url = f"{pictrs_protocol}://{pictrs_host}:{pictrs_port}/image/original/{image_name}"
    
    if not os.path.exists("images"):
        os.mkdir("images")

    # download image and save it to disk
    response = requests.get(pictrs_url)
    with open(f"images/{musicbrainzid}.{image_extension}", "wb") as f:
        f.write(response.content)

    print(f"Downloaded {musicbrainzid}.{image_extension}")
