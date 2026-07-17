from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Library Management API")

@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API!"}

uvicorn.run("app.main:app" , host="0.0.0.0", port=8000 , reload=True)