# Assets Browser

**Assets Browser** is a Python app that are designed to manage assets for 3DCG/VFX pipeline.

This is still an ongoing progress and minor bugs are expected.

Feel free to fork out as I wrote this with Python 2.7 and PyQt4 which has compatibility issue
with Python 3.0+ and PyQt5 environment.

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

## Requirements
* **Python 2.7**
* **PyQt4**

_While this codes has been tested in a Windows environment only, it should work without any
issues on Linux/OSX environment._

## Features
* Navigate assets based on projects from a dropdown list.
* Create new assets using dialog with options.
* _IN PROGRESS:_ Integrated help file for assets as reference for artists.