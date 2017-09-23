# coding=utf-8
"""
README GENERATOR
Readme content variables
Autor: Pablo Pizarro R. @ ppizarror.com
Licencia:
    The MIT License (MIT)
    Copyright 2017 Pablo Pizarro R.
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the Software
    is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

CONTENT_HEADER_URL_IMAGE = """<h1 align="center">
  <a href="{0}" title="{1}">
    <img alt="{2}" src="{3}" width="{5}px" height="{6}px" />
  </a>
  <br /><br />
  {4}
</h1>
"""

CONTENT_HEADER_NO_URL_IMAGE = """<h1 align="center">
  <img alt="{0}" src="{1}" width="{3}px" height="{4}px" />
  <br /><br />
  {2}
</h1>
"""

CONTENT_HEADER_URL_NO_IMAGE = """<h1 align="center">
  <a href="{0}" title="{1}">
    {2}
  </a>
</h1>
"""

CONTENT_HEADER_NO_URL_NO_IMAGE = """<h1 align="center">
  {0}
</h1>
"""

CONTENT_DESCRIPTION = """<p align="center">{0}</p>
"""

CONTENT_BADGES = """<div align="center">{0}</div>
<br />
"""

CONTENT_BADGE_ITEM = """
  <a href="{0}">
    <img alt="{1}" src="{2}" />
  </a>
"""

CONTENT_AUTHOR_SECTION_URL_DATE = """\n
## {0}
<a href="{1}" title="{2}">{3}</a> | {4}
"""

CONTENT_AUTHOR_SECTION_NO_URL_DATE = """\n
## {0}
{1} | {2}
"""

CONTENT_AUTHOR_SECTION_URL_NO_DATE = """\n
## {0}
<a href="{1}" title="{2}">{3}</a>
"""

CONTENT_AUTHOR_SECTION_NO_URL_NO_DATE = """\n
## {0}
{1}
"""
