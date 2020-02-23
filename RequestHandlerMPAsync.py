#!/usr/bin/env python3
import asyncio as asy
import multiprocessing
import aiohttp
import time
import os

loop = None
apiUrl = None
maxConnectionLimit = None


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def getAPIDetails():
    global apiUrl
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,apiUrl)
        # print(html)

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    print(msg)


async def requestHandler(requests):
    global loop
    global maxConnectionLimit
    tasks = []
    requeststoProcess  = requests if requests <= maxConnectionLimit else maxConnectionLimit
    while requeststoProcess > 0:
        for taskItem in range(requeststoProcess):
            tasks.append(loop.create_task(getAPIDetails()))
        done, pending = await asy.wait(tasks, return_when = asy.FIRST_COMPLETED)
        requests = requests - requeststoProcess
        requeststoProcess  = requests if requests <= maxConnectionLimit else maxConnectionLimit


def initProcess():
    global loop
    global apiUrl
    global maxConnectionLimit
    if not loop:
        loop = asy.get_event_loop()
        apiUrl =  'http://localhost:3000/api/v1/apiDetails'
        maxConnectionLimit = int(1000 / os.cpu_count())


def processRequest(param):
    loop.set_exception_handler(handle_exception)
    loop.run_until_complete(requestHandler(param))
    loop.close()


def processRequestsMultiProcessing(requestCount):
    params = []
    with multiprocessing.Pool(initializer=initProcess) as pool:
        for index in range(os.cpu_count()):
            params.append(int(requestCount / os.cpu_count()))
        pool.map(processRequest,params)

def runBatch():
    requests = input("Enter the numer of Attempts to make : ")
    requests = int(requests)
    if requests == 0 :
        return  False
    start_time = time.time()
    processRequestsMultiProcessing(requests)
    duration = time.time() - start_time
    print('Total Process duration for {} count is  {} '.format(requests, duration))
    return  True

if __name__ == '__main__':
    while runBatch():
        pass
