import asyncio
import errno
import os

import aiofiles
import aiohttp
from tqdm import tqdm

from .login import HOME_URL

HEADERS = {"Content-Type": "application/json", "user-agent": "Mozilla/5.0"}


def check_path_exists(filename: str):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


class Fetcher:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _fetch_url(self, url: str) -> dict:
        cookies = self.session.cookie_jar.filter_cookies(HOME_URL)
        csrf_token = cookies["JSESSIONID"].value
        headers = HEADERS | {"Csrf-Token": csrf_token}
        async with self.session.get(url, headers=headers) as response:
            ret_json = await response.json()
        return ret_json

    async def fetch_course_path_data(self, slug: str):
        url = (
            f"https://www.linkedin.com/learning-api/detailedLearningPaths"
            f"?learningPathSlug={slug}&q=slug&version=2"
        )
        data = (await self._fetch_url(url))["elements"][0]

        course_slugs = []
        for section in data["sections"]:
            for item in section["items"]:
                content = item["content"]
                slug = content[list(content.keys())[0]]["slug"]
                course_slugs.append(slug)

        courses_data = await asyncio.gather(
            *[self.fetch_course_data(slug) for slug in course_slugs]
        )

        return data, courses_data

    async def fetch_course_data(self, slug: str) -> dict:
        url = (
            f"https://www.linkedin.com/learning-api/detailedCourses"
            f"??fields=fullCourseUnlocked,releasedOn,exerciseFileUrls,exerciseFiles&"
            f"addParagraphsToTranscript=true&courseSlug={slug}&q=slugs"
        )
        return (await self._fetch_url(url))["elements"][0]

    async def fetch_download_link(self, course_slug, video_slug) -> str:
        url = (
            f"https://www.linkedin.com/learning-api/detailedCourses?"
            f"addParagraphsToTranscript=false&courseSlug="
            f"{course_slug}&q=slugs&resolution=_720&videoSlug={video_slug}"
        )
        data = await self._fetch_url(url)
        return data["elements"][0]["selectedVideo"]["url"]["progressiveUrl"]

    async def download_file(
        self, url: str, filename: str, path: str, chunk_size=32 * 1024
    ) -> None:
        check_path_exists(path + filename)
        options = {
            "unit": "B",
            "unit_scale": True,
            "unit_divisor": 1024,
            "desc": filename,
            "initial": 0,
            "ascii": True,
            "miniters": 1,
            "leave": False,
        }
        async with aiofiles.open(path + filename, mode="wb") as f:
            async with self.session.get(url) as response:
                fsize = response.content_length
                with tqdm(**options, total=fsize) as pbar:
                    async for data in response.content.iter_chunked(chunk_size):
                        pbar.update(len(data))
                        await f.write(data)

        # url = f"https://www.linkedin.com/learning-api/detailedLearningPaths?learningPathSlug=advance-your-skills-in-python-8969631&q=slug&version=2"
