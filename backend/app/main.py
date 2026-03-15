from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
   return {"status":"ok"}

@app.get("/api/hello")
def hello():
   return {"message":"Hello hello from raspberry pi"}

