from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# In-memory store for data (for demo purposes)
stored_data = []

# Serve static files (index.html)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.get("/api/data")
async def get_data():
    return JSONResponse(content={"message": stored_data})

@app.post("/api/data")
async def post_data(request: Request):
    data = await request.json()
    stored_data.append(data.get("data"))
    return JSONResponse(content={"message": "Data added successfully"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        stored_data.append(data)
        await websocket.send_text(f"Received: {data}")
