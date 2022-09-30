import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.common.main:app", host="localhost", port=8000)