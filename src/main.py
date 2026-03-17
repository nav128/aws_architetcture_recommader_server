from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from ingestor import ingest
from models.arch import ArchitectureRequest
from recommander import recommander
from services.db_service import db
import traceback

load_dotenv()

app = FastAPI(title="Aws Architecture Recomendations")


@app.get("/")
def root():
	return HTMLResponse(content="WhoThat?\n", status_code=200)

@app.get("/healthz")
def healthz():
	return HTMLResponse(content="Service is healthy\n", status_code=200)

@app.get("/scrape-and-save")
async def scrape_and_save():
	try:
		n_scraped = ingest()
		return HTMLResponse(content=f"Saved {len(n_scraped)} architectures", status_code=200)
	except Exception as exc:
		traceback.print_exc()
		raise HTTPException(status_code=500, detail="internal server error\n" + str(exc)) from exc

@app.get("/architectures")
async def get_architectures():
    return db.local_table

@app.post("/recommendations")
async def get_recommendations(requirements: ArchitectureRequest):
	try:
		return recommander(requirements)
	except Exception as exc:
		traceback.print_exc()
		raise HTTPException(status_code=500, detail="internal server error\n" + str(exc)) from exc	