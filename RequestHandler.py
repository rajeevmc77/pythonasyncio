#!/usr/bin/env python3
import asyncio as asy
import multiprocessing
import aiohttp
import time


loop = None
apiUrl = None


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def getAPIDetails(count):
    for index in range(count):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session,apiUrl)
            print(html)


async def requestHandler():
    global loop
    divs1 = loop.create_task(getAPIDetails(20))
    divs2 = loop.create_task(getAPIDetails(20))
    divs3 = loop.create_task(getAPIDetails(20))
    await asy.wait([divs1,divs2,divs3])


def processRequest(processorId):
    loop.run_until_complete(requestHandler())
    loop.close()


def initProcess():
    global loop
    global apiUrl
    if not loop:
        loop = asy.get_event_loop()
        apiUrl =  'http://localhost:3000/api/v1/apiDetails'


def processRequestsMultiProcessing():
    with multiprocessing.Pool(initializer=initProcess) as pool:
        params = [1,2,3,4]
        pool.map(processRequest,params)


if __name__ == '__main__':
    start_time = time.time()
    processRequestsMultiProcessing()
    duration = time.time() - start_time
    print('Total Process duration is  {} '.format( duration))
