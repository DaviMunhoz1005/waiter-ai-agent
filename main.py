from agents.waiter_agent import create_waiter_agent
from fastapi import FastAPI
from pydantic import BaseModel

waiter_agent = create_waiter_agent()

app = FastAPI()

class Body(BaseModel):
    message: str

@app.post("/run")
async def run(body: Body):
    response = waiter_agent.run(body.message)
    return {"response": response.content}
