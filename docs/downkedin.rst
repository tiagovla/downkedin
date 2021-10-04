.. currentmodule:: downkedin

API Reference
===============

The following section outlines the API of downkedin.

Downloader Module
---------------------------

.. automodule:: downkedin.downloader
   :members:
   :undoc-members:
   :show-inheritance:

Login Module
----------------------

Main Login Strategies
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.login.UsernamePasswordStrategy
   :members:
   :undoc-members:
   :show-inheritance:

Wrapper Login Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.login.PicleStrategy
   :members:
   :undoc-members:
   :show-inheritance:

This should be used with a main strategy as backup.

.. code-block:: python

   PicleStrategy("cookies.bin", UsernamePasswordStrategy("username", "password"))

Models Module
-----------------------

Video
~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.models.Video
   :members:
   :undoc-members:
   :show-inheritance:

Chapter
~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.models.Chapter
   :members:
   :undoc-members:
   :show-inheritance:

Course
~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.models.Course
   :members:
   :undoc-members:
   :show-inheritance:

CoursePath
~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.models.CoursePath
   :members:
   :undoc-members:
   :show-inheritance:

Author
~~~~~~~~~~~~~~~~~~~

.. autoclass:: downkedin.models.Author
   :members:
   :undoc-members:
   :show-inheritance:


Fetcher Module
------------------------

.. automodule:: downkedin.fetcher
   :members:
   :undoc-members:
   :show-inheritance:

File Manager Module
----------------------------

.. automodule:: downkedin.filemanager
   :members:
   :undoc-members:
   :show-inheritance:



Parser Module
-----------------------

.. automodule:: downkedin.parser
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
---------------------------

.. automodule:: downkedin.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
