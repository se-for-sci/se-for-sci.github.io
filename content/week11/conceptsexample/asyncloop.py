import asyncio


async def sleep(t):
    await asyncio.sleep(t)
    return f"Sleep {t} over"


async def main():
    results = await asyncio.gather(sleep(3), sleep(2), sleep(1), sleep(4))
    print(results)


asyncio.run(main())
