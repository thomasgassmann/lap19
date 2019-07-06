import asyncio
import aiohttp
import os

photo_range = range(1, 118)
out_dir = './photos'
file_descriptor = 'CN-LAP19-JOB026-{0:0=3d}.jpg'
main_url = 'http://www.lap.auraonline.ch/actions/file_download.php?path=../albums%2F26_5_Juli_SPZ-Nottwil_1330&filename={}&user=MEDIA'
session_id = '45atjuhbbcv1ndlmtvqrbd60b1'


async def download_photo(session: aiohttp.ClientSession, url: int, filename: str):
    async with session.get(url) as response:
        with open(filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                
                f.write(chunk)


async def main():
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    headers = {'Cookie': f'PHPSESSID={session_id}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        futures = []
        for i in photo_range:
            file_name = file_descriptor.format(i)
            url = main_url.format(file_name)
            futures.append(download_photo(session, url, os.path.join(out_dir, file_name)))
        await asyncio.wait(futures)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
