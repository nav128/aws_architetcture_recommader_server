from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
import json
from ingest.ingest import ingest
from mongo_client import db

load_dotenv()



app = FastAPI(title="Aws Architecture Recomendations")


@app.get("/")
def root():
	return HTMLResponse(content="WhoThat?\n", status_code=200)

@app.get("/healthz")
def healthz():
	return HTMLResponse(content="Service is healthy\n", status_code=200)

@app.post("/scrape-and-save")
async def scrape_and_save():
	try:
		n_scraped = ingest()
		return HTMLResponse(content=f"Saved {len(n_scraped)} architectures", status_code=200)
	except Exception as exc:
		raise HTTPException(status_code=500, detail=str(exc)) from exc
		
@app.get("/architectures")
async def get_architectures():
    collection = db.architectures
    architectures = await collection.find().to_list(None)
    return architectures