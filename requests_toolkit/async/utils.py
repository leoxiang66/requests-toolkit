import asyncio
from asyncio import Task

def create_dumi_tasks(n: int):
    async def dumi():
        await asyncio.sleep(2)

    loop = asyncio.get_event_loop()
    
    return [loop.create_task(dumi()) for _ in range(n)]



async def yield_done(tasks):
    """Async generator that yields completed tasks from a list of tasks."""
    completed = set()
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done - completed:
            completed.add(task)
            yield task





if __name__ == "__main__":
    print(create_dumi_tasks(1))