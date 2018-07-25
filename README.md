# InstaPython App

InstaPython App is a graphical interface wrapped around my python package [InstaPython](https://github.com/t0xic-m/instapython). It provides basic functions to access and deal with Instagram data and two of my other Projects: [InstaBot](https://github.com/t0xic-m/instagram_watchdog) and [InstaView](https://github.com/t0xic-m/instagram_data_download_viewer). InstaPython App was built with [Electron](https://electronjs.org/) and [Bootstrap](https://getbootstrap.com/).

Alternatively there is also a version that runs natively in Python 3.6 and uses Tkinter for the interface!

## Features

- Retrieve User ID
- Retrieve Username
- Retrieve Media Count
- Retrieve Profile Picture (direct link)
- Retrieve Newest Post (direct links)
- Retrieve Stories (direct links)
- Retrieve Privacy Setting
- Download Profile Picture
- Download Newest Post
- Download Stories
- Download Post Media (Picture/Video/Album)
- InstaBot: A watchdog to observe public Instagram profiles. [see here!](https://github.com/t0xic-m/instagram_watchdog)
- InstaView: A script to create nicely structured R Markdown/PDF files from Instagram data.  [see here!](https://github.com/t0xic-m/instagram_data_download_viewer)

## Requirements

**Platform: Windows**

[Python](https://www.python.org/) and [Node.js](https://nodejs.org) (with [npm](https://www.npmjs.com/)) are prerequesits!

To be more specific:
- Python 3.6 (with python added to PATH)
- Python Packages:
  - lxml
    ```bash
    pip install lxml
    ```
  - requests
    ```bash
    pip install requests
    ```
- Node.js with npm (with both added to PATH)

## Getting Started

```bash
# Clone this repository with git (or download it manually via this link: https://github.com/t0xic-m/instapython-app/archive/master.zip)
git clone https://github.com/t0xic-m/instapython-app.git
# Go into the repository
cd instapython-app/app
# Install dependencies
npm install
# Run the app
npm start
```
## Native Python GUI with Tkinter

**Platform: All Platforms**

Requires Python 3.6 and the following packages:

```python
import urllib.request as ur
import urllib.parse as up
from lxml import html
import tkinter as tk
from tkinter import scrolledtext as st
import platform
import webbrowser
import datetime
import requests
import json
import time
import sys
import os
```

Getting started:

```bash
# Clone this repository with git (or download it manually via this link: https://github.com/t0xic-m/instapython-app/archive/master.zip)
git clone https://github.com/t0xic-m/instapython-app.git
# Go into the repository
cd instapython-app/app-tkinter
# Install dependencies
pip install lxml
pip install requests
...
# Run the app on Windows
python instapython-app.py
# Run the app on any other platform
python3 instapython-app.py
```
The standalone tkinter version will be further developed [here](https://github.com/t0xic-m/instapython)!

## Credits

- Copyright (c) 2018 Micha Birklbauer
- Copyright (c) 2018 Hannelore Bodocian
- Copyright (c) 2013-2018 GitHub Inc.
- Copyright (c) 2011-2018 Twitter, Inc.
- Copyright (c) 2011-2018 The Bootstrap Authors

## License

[MIT License](https://github.com/t0xic-m/instapython-app/blob/master/LICENSE.md)

## Contact

- [Website](https://sites.google.com/site/michabirklbauer)
- [GitHub Profile](https://github.com/t0xic-m)
- [GitHub Page](https://t0xic-m.github.io/)
- [Mail](micha.birklbauer@gmail.com)
- [Telegram](https://telegram.me/micha_birklbauer)
