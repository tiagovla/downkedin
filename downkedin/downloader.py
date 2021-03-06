from __future__ import annotations

import aiohttp

from .fetcher import Fetcher
from .login import LoginStrategy
from .models import Course, CoursePath
from .parser import ModelParser


class Downloader:
    def __init__(self, login_strategy: LoginStrategy):
        self.login_strategy = login_strategy
        self.parser: ModelParser
        self.session: aiohttp.ClientSession
        self.fetcher: Fetcher

    async def login(self):
        """
        Login function.

        Used the registered Downloader's login strategy to login.

        Raises
        ------
        Exception:
            If no session is found, raises an exception.
        """
        if self.session:
            await self.login_strategy(self.session)
        else:
            raise Exception("No session found.")

    async def start(self):
        self.session = aiohttp.ClientSession()
        self.fetcher = Fetcher(self.session)
        self.parser = ModelParser(self.fetcher)

    async def close(self):
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def fetch_course(self, slug: str) -> Course:
        data = await self.fetcher.fetch_course_data(slug)
        return self.parser.course(data)

    async def fetch_course_path(self, slug: str) -> CoursePath:
        data, courses_data = await self.fetcher.fetch_course_path_data(slug)
        return self.parser.course_path(data, courses_data)
