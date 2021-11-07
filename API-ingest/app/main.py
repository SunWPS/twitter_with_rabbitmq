import json
from pydantic import BaseModel

from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue="tweet")

class Tweet(BaseModel):
    id: str
    created_at: str
    text: str
    username: str
    followers: int
    retweets: int
    favorites: int

app = FastAPI()

# Base
@app.get("/")
async def root():
    return "Hello, world!"

@app.post("/posttweet")
async def post_tweet(item: Tweet):
    print("Message Received")
    
    # Parse back to JSON
    json_item = jsonable_encoder(item)
    
    # Dump JSON to string
    json_str = json.dumps(json_item)
    # print(json_str)
    produce_rabbit_message(json_str)
    
    
    
def produce_rabbit_message(json_str):
    channel.basic_publish(exchange="",
                          routing_key="tweet",
                          body=json.dumps(json_str))
    print("[tweet] to rabbit")
