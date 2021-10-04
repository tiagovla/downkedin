import asyncio

from tqdm.asyncio import tqdm

from downkedin.downloader import Downloader
from downkedin.login import PicleStrategy, UsernamePasswordStrategy


async def main():
    """Run the main downloader application."""
    username = "***REMOVED***"
    password = "***REMOVED***"

    backup_strat = UsernamePasswordStrategy(username, password)
    # this wrapper will save your cookies in a cookies.bin file.
    login_strat = PicleStrategy("cookies.bin", backup_strat)

    async with Downloader(login_strat) as dl:
        await dl.login()

        slug = "advance-your-skills-in-python-8969631"
        course_path = await dl.fetch_course_path(slug)
        course_path.print()

        # for course in course_path.children:
        #     tasks = [down for down in course.download()]
        #     for coro in tqdm.as_completed(tasks, total=len(tasks)):
        #         await coro


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
