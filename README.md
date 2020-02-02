# Assets Browser

**Assets Browser** is a Python app that are designed to manage and browse assets for 3DCG/VFX pipeline.

This is still an ongoing progress and minor bugs are expected.

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
* Configurable assets' folder structure template via INI.
* _IN PROGRESS:_ Integrated assets' help file for artists' reference.

## Usage
Requirements
* **[Python  3.6.xx](https://www.python.org/)** - Tested on 3.6.7 x64
* **[PyQt5](https://riverbankcomputing.com/software/pyqt/intro)** - Tested on 5.11.3 for Python 3 x64

> Currently develop on Windows 7 and verify manually on Ubuntu 16.10. macOS support are not guaranteed
> as I do not have access to macOS devices.

1. Clone or download the repository.
2. Extract to your chosen destination.
3. Run `assetsbrowser.py`


## Tests
```python
# Run every tests
python -m pytest

# Run specific module tests
python -m pytest <module_name>/tests
```
