from .fetcher import Fetcher
from .models import Chapter, Course, CoursePath, Video


class ModelParser:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    def video(self, data: dict) -> Video:
        pdata = {"title": data["title"], "slug": data["slug"], "fetcher": self.fetcher}
        video = Video(**pdata)
        return video

    def chapter(self, data: dict) -> Chapter:
        title = data["title"]
        chapter = Chapter(title=title)
        for vdata in data["videos"]:
            video = self.video(vdata)
            chapter.add_child(video)
        return chapter

    def course(self, data: dict) -> Course:
        cdata = {"slug": data["slug"], "title": data["title"]}
        course = Course(**cdata)
        for cdata in data["chapters"]:
            chapter = self.chapter(cdata)
            course.add_child(chapter)
        return course

    def course_path(self, data: dict, courses_data: list[dict]) -> CoursePath:
        cpdata = {"slug": data["slug"], "title": data["title"]}
        course_path = CoursePath(**cpdata)
        for cdata in courses_data:
            course = self.course(cdata)
            course_path.add_child(course)
        return course_path
