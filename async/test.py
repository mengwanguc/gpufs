import asyncio

async def funa():
    print("funa starts")
    await asyncio.sleep(5)  # Asynchronous sleep
    print("funa ends")

async def funb():
    print("funb starts")
    await asyncio.sleep(5)  # Asynchronous sleep
    print("funb ends")

async def main():
    # Running funa and waiting for it to finish
    await funa()

    # Perform any intermediate computations here, if needed

    # Running funb only after funa has completed
    await funb()

# Running the main coroutine
asyncio.run(main())
