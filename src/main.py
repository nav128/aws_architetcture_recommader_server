from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, List
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
import os
import json
from mongo_client import db

load_dotenv()



app = FastAPI()

# class Architecture(BaseModel):
#     name: str
#     use_case: Literal["web_application", "public_api", "ecommerce", "real_time_analytics",
#                      "batch_processing", "event_processing", "media_delivery", "internal_tool",
#                      "iot_ingestion", "ml_inference"]
#     scale: Literal["small", "medium", "large"]
#     traffic_pattern: Literal["steady", "bursty", "spiky", "scheduled", "unpredictable"]
#     latency_sensitivity: Literal["low", "medium", "high"]
#     processing_style: Literal["request_response", "event_driven", "batch", "streaming"]
#     data_intensity: Literal["low", "medium", "high"]
#     availability_requirement: Literal["standard", "high", "critical"]
#     ops_preference: Literal["managed_services", "balanced", "self_managed_ok"]
#     budget_sensitivity: Literal["low", "medium", "high"]
#     actual_architecture: str

# async def scrape_readme(url: str) -> str:
#     response = requests.get(url)
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail=f"Failed to fetch {url}")
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # Assuming README is in a div with class 'markdown-body' or similar
#     content = soup.find('article', class_='markdown-body') or soup.find('div', class_='markdown-body')
#     if content:
#         return content.get_text()
#     else:
#         return soup.get_text()  # fallback

# async def extract_architectures(content: str) -> List[Architecture]:
#     prompt = f"""
# Extract AWS architectures from the following content. For each architecture found, provide:
# - name: A short name for the architecture
# - use_case: One of {["web_application", "public_api", "ecommerce", "real_time_analytics", "batch_processing", "event_processing", "media_delivery", "internal_tool", "iot_ingestion", "ml_inference"]}
# - scale: One of {["small", "medium", "large"]}
# - traffic_pattern: One of {["steady", "bursty", "spiky", "scheduled", "unpredictable"]}
# - latency_sensitivity: One of {["low", "medium", "high"]}
# - processing_style: One of {["request_response", "event_driven", "batch", "streaming"]}
# - data_intensity: One of {["low", "medium", "high"]}
# - availability_requirement: One of {["standard", "high", "critical"]}
# - ops_preference: One of {["managed_services", "balanced", "self_managed_ok"]}
# - budget_sensitivity: One of {["low", "medium", "high"]}
# - actual_architecture: A description of the architecture

# Return as a JSON array of objects.

# Content:
# {content[:4000]}  # limit content
# """
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=2000
#     )
#     result = response.choices[0].message.content
#     try:
#         architectures = json.loads(result)
#         return [Architecture(**arch) for arch in architectures]
#     except:
#         return []

@app.post("/scrape-and-save")
async def scrape_and_save():
    urls = [
        "https://raw.githubusercontent.com/donnemartin/awesome-aws/master/README.md",
        "https://raw.githubusercontent.com/aws-samples/aws-architecture-diagrams/master/README.md"
    ]
    all_architectures = []
    for url in urls:
        content = await scrape_readme(url)
        architectures = await extract_architectures(content)
        all_architectures.extend(architectures)
    
    collection = db.architectures
    for arch in all_architectures:
        await collection.insert_one(arch.dict())
    
    return {"message": f"Saved {len(all_architectures)} architectures"}

@app.get("/architectures")
async def get_architectures():
    collection = db.architectures
    architectures = await collection.find().to_list(None)
    return architectures