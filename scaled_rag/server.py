from fastapi import Query
from fastapi import FastAPI
from .client.rq_client import queue


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(query: str = Query(..., description="query from your documents")):
    job = queue.enqueue("scaled_rag.queue.worker.process_query", query)
    return {"status": "queued", "job_id": job.id, "query": query}