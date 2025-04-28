from fastapi import FastAPI
app = FastAPI()

@app.post("/process_task/")
async def process_task(task: dict):
    complexity = task.get("complexity",0)
    if complexity>80:
        return {"mode":"quantum","detail":"Routed to quantum backend"}
    return {"mode":"classical","detail":"Processed classically"}
