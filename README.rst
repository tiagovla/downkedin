
|PyPI License| |PyPI PyVersions| |PyPI Version| |Build Status| |DeepSource| |Codecov| |Documentation Status|



================
Linkedin Learning Downloader
================

Quick example:
##############

.. code-block:: python


  import asyncio

  from tqdm.asyncio import tqdm

  from downkedin.downloader import Downloader
  from downkedin.login import PicleStrategy, UsernamePasswordStrategy


  async def main():
      """Run the main downloader application."""
      username = "username"
      password = "password"

      backup_strat = UsernamePasswordStrategy(username, password)
      # this wrapper will save your cookies in a cookies.bin file.
      login_strat = PicleStrategy("cookies.bin", backup_strat)

      async with Downloader(login_strat) as dl:
          await dl.login()

          slug = "advance-your-skills-in-python-8969631"
          course_path = await dl.fetch_course_path(slug)
          course_path.print()

          for course in course_path.children:
              tasks = [down for down in course.download()]
              for coro in tqdm.as_completed(tasks, total=len(tasks)):
                  await coro


  if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main())



.. |PyPI License| image:: https://img.shields.io/pypi/l/downkedin.svg
  :target: https://pypi.python.org/pypi/downkedin

.. |PyPI PyVersions| image:: https://img.shields.io/pypi/pyversions/downkedin.svg
  :target: https://pypi.python.org/pypi/downkedin

.. |PyPI Version| image:: https://img.shields.io/pypi/v/downkedin.svg
  :target: https://pypi.python.org/pypi/downkedin

.. |Build Status| image:: https://travis-ci.com/tiagovla/downkedin.svg?branch=master
  :target: https://travis-ci.com/tiagovla/downkedin

.. |DeepSource| image:: https://deepsource.io/gh/tiagovla/downkedin.svg/?label=active+issues
  :target: https://deepsource.io/gh/tiagovla/downkedin/?ref=repository-badge

.. |Codecov| image:: https://codecov.io/gh/tiagovla/downkedin/branch/master/graph/badge.svg?token=QR1RMTPX0H
  :target: https://codecov.io/gh/tiagovla/downkedin

.. |Documentation Status| image:: https://readthedocs.org/projects/downkedin/badge/?version=latest
  :target: https://downkedin.readthedocs.io/en/latest/?badge=latest
