import asyncio


async def main():
    print("hi")
    loop = asyncio.get_running_loop()
    print(loop)



if __name__ == "__main__":
    asyncio.run(main())

