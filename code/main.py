from fastapi import FastAPI

app = FastAPI(title="Car Rental API")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Hello World"}