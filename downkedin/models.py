from __future__ import annotations

from typing import List, Protocol

import aiohttp
from attr import dataclass

from .fetcher import Fetcher


class Downloadable(Protocol):
    async def download(self, session: aiohttp.ClientSession) -> None:
        """
        Download protocol.

        Implement the download protocol.

        Parameters
        ----------
        session : aiohttp.ClientSession
            Session object from aiohttp.

        Returns
        -------
        None:

        """
        pass


class BaseModel:
    def __init__(self, title: str):
        """
        BaseModel class.

        Implements a double association strategy.

        Parameters
        ----------
        title : str
            Title of the associated object.
        """
        self.parent: BaseModel | None = None
        self.children: List[BaseModel] = []
        self.title = title

    def _set_parent(self, parent: BaseModel):
        self.parent = parent

    def add_child(self, child: BaseModel) -> BaseModel:
        child._set_parent(self)
        self.children.append(child)
        return self

    def __str__(self):
        return f"({self.__class__.__name__}, {self.title})"

    def print(self, indent=0):
        print("  " * indent + self.__str__())
        for child in self.children:
            child.print(indent + 2)

    def download(self, directory: str = "downloads"):
        for child in self.children:
            yield from child.download(directory)


class Video(BaseModel):
    def __init__(self, title: str, slug: str, fetcher: Fetcher):
        """
        Video class model.

        Represent a video object.

        Parameters
        ----------
        title : str
            Title of the video.
        slug : str
            Slug of the video.
        fetcher : Fetcher
            Fetcher object used to download the video's content.
        """
        super().__init__(title)
        self.slug = slug
        self.fetcher = fetcher
        self.parent: Chapter

    async def _download(self, directory: str):
        course_slug = self.parent.parent.slug
        video_slug = self.slug
        url = await self.fetcher.fetch_download_link(course_slug, video_slug)
        await self.fetcher.download_file(
            url,
            f"{self.title}.mp4",
            f"{directory}/{self.parent.parent.title}/{self.parent.title}/",
        )

    def download(self, directory: str = "downloads"):
        yield self._download(directory)


class Chapter(BaseModel):
    def __init__(self, title: str):
        """
        Chapter class model.

        Represent a chapter object.

        Parameters
        ----------
        title : str
            Title of the chapter.
        """
        super().__init__(title)
        self.parent: Course


class Course(BaseModel):
    def __init__(self, title: str, slug: str):
        """
        Course class model.

        Represent a course object.

        Parameters
        ----------
        title : str
            Title of the course.
        slug : str
            Slug of the course.
        """
        super().__init__(title)
        self.slug = slug


class CoursePath(BaseModel):
    def __init__(self, title: str, slug: str):
        """
        Course path class model.

        Represent a course path object.

        Parameters
        ----------
        title : str
            Title of the course path.
        slug : str
            Slug of the course path.
        """
        super().__init__(title)
        self.slug = slug


@dataclass
class Author:
    first_name: str
    last_name: str
