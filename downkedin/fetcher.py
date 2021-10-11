import asyncio
import errno
import os

import aiofiles
import aiohttp
from tqdm import tqdm

from .login import HOME_URL

HEADERS = {"Content-Type": "application/json", "user-agent": "Mozilla/5.0"}


def check_path_exists(filename: str):
    """
    Function to check whether a path exists.

    If it does not exist, it creates it.

    Parameters
    ----------
    filename : str
        Path to be created if it does not already exist.

    Raises
    ------
    Exception:
        Race condition exception.
    """
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise Exception("Race condition.")


class Fetcher:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _fetch_url(self, url: str) -> dict:
        """
        Private fetch url function.

        Parameters
        ----------
        url : str
            String url to be fetched by a get request.

        Returns
        -------
        dict:
            Dictionary containing the json result of the request.
        """
        cookies = self.session.cookie_jar.filter_cookies(HOME_URL)
        csrf_token = cookies["JSESSIONID"].value
        headers = HEADERS | {"Csrf-Token": csrf_token}
        async with self.session.get(url, headers=headers) as response:
            ret_json = await response.json()
        return ret_json

    async def fetch_course_path_data(self, slug: str) -> tuple[dict, list[dict]]:
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

        courses_data = list(
            await asyncio.gather(
                *[self.fetch_course_data(slug) for slug in course_slugs]
            )
        )

        return data, courses_data

    async def fetch_course_data(self, slug: str) -> dict:
        url = (
            f"https://www.linkedin.com/learning-api/detailedCourses"
            f"??fields=fullCourseUnlocked,releasedOn,exerciseFileUrls,exerciseFiles&"
            f"addParagraphsToTranscript=true&courseSlug={slug}&q=slugs"
        )
        return (await self._fetch_url(url))["elements"][0]

    async def fetch_download_link(self, course_slug: str, video_slug: str) -> str:
        url = (
            f"https://www.linkedin.com/learning-api/detailedCourses?"
            f"addParagraphsToTranscript=false&courseSlug="
            f"{course_slug}&q=slugs&resolution=_720&videoSlug={video_slug}"
        )
        data = await self._fetch_url(url)
        return data["elements"][0]["selectedVideo"]["url"]["progressiveUrl"]

    async def download_file(
        self, url: str, filename: str, path: str, chunk_size: int = 32 * 1024
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
