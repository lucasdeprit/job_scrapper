from fastapi import FastAPI, Query
from app.scraper.remoteok_scraper import search_wwr_jobs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS opcional si el frontend o backend en Node accede desde otro origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
def scrape_jobs(keywords: str = Query(..., description="Palabras clave para buscar empleos")):
    try:
        results = search_wwr_jobs(keywords)
        return {"status": "ok", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
