import aiofiles
import asyncio

async def produce():
    fifo_path = "../Pipes/to_scheduler"

    print("Producer: Writing data to the existing FIFO...")

    async with aiofiles.open(fifo_path, "wb") as fifo:
        data = bytes([2,0])
        await fifo.write(data)
        print(f"Producer: Sent - {data}")

    print("Producer: Finished writing.")

if __name__ == "__main__":
    asyncio.run(produce())

