# Assets Browser

**Assets Browser** is a Python app that are designed to manage and browse assets for 3DCG/VFX pipeline.

This is still an ongoing progress and minor bugs are expected.

Feel free to fork out as I wrote this with Python 2.7 and PyQt5 which has compatibility issue
with Python 3.0+ and PyQt4 environment.

## Goals
During my time working for a small 3DCG studio, the creation of new assets are tedious since
it is created manually by hand using Windows Explorer.

Furthermore, there are issues with user permission problem that requires the artist to refer
to their team leader or project manager to help them create the assets which affect productivity.

Plus navigating the various assets on the server are not friendly using Windows Explorer.

For reasons above, I decided to write this Python app which helps to minimise the effort of
creating new assets with parameters that meets the studio's pipeline (which can be customised
to fit your pipeline environment) and greatly speed up the navigation of the available assets
based on the project.

Since this code is written in Python, it can be easily deployed to any workstations provided
the necessary dependencies has been installed.

## Features
* Navigate assets based on projects from a dropdown list.
* Create new assets using dialog with options.
* _IN PROGRESS:_ Integrated help file for assets as reference for artists.

## Usage
Requirements
* **[Python  2.7.xx](https://www.python.org/)** - Tested on 2.7.14 x64
* **[PyQt5](https://riverbankcomputing.com/software/pyqt/intro)** - Tested on 5.9.1 for Python 2.7 x64

_The codes has been tested on Windows 7, macOS Sierra and Lubuntu 17.04 for cross-platform compatibility._

**2017/11/09: JPEG and GIF are supported through plugins with the appropriate dylib on macOS/OSX.**

**2017/11/08: Migrated PyQt4 to PyQt5 to comply with VFX Reference Platform CY 2017.**

**2017/09/11: ~~After numerous attempt, looks like PyQt4 for macOS/OSX has broken support for JPEG and GIF format. Broken image format are now omitted from thumbnail preview.~~**

**2017/08/13: ~~Looks like there are known issues with JPEG preview and the UI layout on macOS which will be resolve in future update.~~**

1. Clone or download the repository.
2. Extract to your chosen destination.
3. Run `main.py`

## License

The MIT License (MIT)

Copyright (c) 2017 Huey Yeng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
