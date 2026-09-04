from fastapi import FastAPI
from pydantic import BaseModel

from agent.brain import process_command

app = FastAPI(title="Desktop Girlfriend Agent", version="0.1")


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def home():
    return {"status": "online", "version": "0.1"}


@app.post("/command")
def command(request: CommandRequest):

    result = process_command(request.command)

    return {"command": request.command, "result": result}
