import asyncio
import time

async def run_event_loop(times):
    for _ in range(times):
        await asyncio.sleep(0)


loop = asyncio.get_event_loop()
t0 = time.time()
loop.run_until_complete(run_event_loop(800))
t1 = time.time()

print(t1 - t0)  # 0.008831262588500977