from abc import ABC, abstractmethod
from urllib.parse import urljoin

import aiohttp
import lxml.html
from yarl import URL

HOME_URL = URL("https://www.linkedin.com/")
HEADERS = {"user-agent": "Mozilla/5.0"}


async def check_signed_in(session: aiohttp.ClientSession) -> bool:
    async with session.get(HOME_URL) as response:
        html = await response.text()
        return True if not ">Sign in</" in html else False


async def fetch_params(session: aiohttp.ClientSession) -> dict:
    login_url = urljoin(str(HOME_URL), "/login/")
    async with session.get(login_url, headers=HEADERS) as response:
        body = await response.text()

    html = lxml.html.fromstring(body)
    csrf = html.xpath("//input[@name='loginCsrfParam']/@value").pop()
    sIdString = html.xpath("//input[@name='sIdString']/@value").pop()
    parentPageKey = html.xpath("//input[@name='parentPageKey']/@value").pop()
    pageInstance = html.xpath("//input[@name='pageInstance']/@value").pop()
    loginCsrfParam = html.xpath("//input[@name='loginCsrfParam']/@value").pop()
    fp_data = html.xpath("//input[@name='fp_data']/@value").pop()
    _d = html.xpath("//input[@name='_d']/@value").pop()
    controlId = html.xpath("//input[@name='controlId']/@value").pop()

    return {
        "csrfToken": csrf,
        "ac": 0,
        "sIdString": sIdString,
        "parentPageKey": parentPageKey,
        "pageInstance": pageInstance,
        "trk": "",
        "authUUID": "",
        "session_redirect": "",
        "loginCsrfParam": loginCsrfParam,
        "fp_data": fp_data,
        "_d": _d,
        "controlId": controlId,
    }


async def fetch_login_cookies(session: aiohttp.ClientSession, data: dict = {}) -> None:
    url = urljoin(str(HOME_URL), "checkpoint/lg/login-submit")
    await session.post(url, data=data, headers=HEADERS)
    filtered = session.cookie_jar.filter_cookies(HOME_URL)
    if "liap" not in filtered.output():
        raise Exception("Chosen strategy does not work.")


class LoginStrategy(ABC):
    @abstractmethod
    async def __call__(self, session: aiohttp.ClientSession) -> None:
        """Implements a login strategy."""


class UsernamePasswordStrategy(LoginStrategy):
    def __init__(self, username: str, password: str):
        """
        Username password Strategy.

        Represent a main login strategy.

        Parameters
        ----------
        username : str
            Username used on linkedin learning.
        password : str
            Password used on linkedin learning.
        """
        self.username = username
        self.password = password

    async def __call__(self, session: aiohttp.ClientSession) -> None:
        """Implements a login strategy."""
        params = await fetch_params(session)
        params = {
            "session_key": self.username,
            "session_password": self.password,
        } | params
        await fetch_login_cookies(session, params)


class PicleStrategy(LoginStrategy):
    def __init__(self, path: str, backup_strategy: LoginStrategy):
        """
        Picle wrapper strategy.

        Represent a wrapper using picle capabilities to reuse cookies.

        Parameters
        ----------
        path : str
            File name with path to save the serialized state.
        backup_strategy : LoginStrategy
            Backup strategy, usually a Username/Password strategy.
        """
        self.path = path
        self.backup_strategy = backup_strategy

    async def __call__(self, session: aiohttp.ClientSession) -> None:

        try:
            session.cookie_jar.clear()
            session.cookie_jar.load(self.path)  # type: ignore
        except FileNotFoundError:
            print("File not found.")

        is_signed_in = await check_signed_in(session)
        print("Signed in:", is_signed_in)
        if not is_signed_in:
            print("Using backup_strategy.")
            await self.backup_strategy(session)

        session.cookie_jar.save(self.path)  # type: ignore
