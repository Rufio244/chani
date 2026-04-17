from app.agents.planner import create_plan
from app.agents.executor import execute_task

async def run_agent(goal: str):
    plan = await create_plan(goal)

    results = []

    for step in plan:
        result = await execute_task(step)
        results.append({
            "step": step,
            "result": result
        })

    return {
        "goal": goal,
        "steps": results
    }
