from fastapi import FastAPI

app = FastAPI(title="admin-core")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": True}
