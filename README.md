# Selenium Authenticated Proxy Helper

## Overview

The Selenium Authenticated Proxy Helper is a Python utility designed to seamlessly handle proxy authentication when using Selenium WebDriver. This package generates a Chrome extension that takes care of proxy authentication, allowing you to focus more on web scraping or automation tasks, without worrying about the intricacies of proxy setup.

## Features

- **Proxy Authentication**: Supports username and password authentication for proxy servers.
- **Unique Identification**: Generates a unique Chrome extension for each different set of proxy credentials.
- **Ease of Use**: Simple API to generate and use the extension with your existing Selenium Chrome WebDriver setup.
- **Temporary Storage**: Optionally, specify a folder for temporary storage of generated Chrome extensions.

## Requirements

- Python 3.6 or higher
- Selenium WebDriver

## Installation

You can install this package via pip:

```bash
pip install selenium-authenticated-proxy
```

## Usage

### Basic Usage

Here is how you can set up the authenticated proxy for Selenium's Chrome WebDriver:

```python
from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()

# Initialize SeleniumAuthenticatedProxy
proxy_helper = SeleniumAuthenticatedProxy(proxy_url="http://username:password@proxy-server.com")

# Enrich Chrome options with proxy authentication
proxy_helper.enrich_chrome_options(chrome_options)

# Start WebDriver with enriched options
driver = webdriver.Chrome(chrome_options=chrome_options)

# Your automation or scraping code here
```

### Custom Temporary Folder

You can specify a custom folder for temporary storage of generated Chrome extensions.

```python
proxy_helper = SeleniumAuthenticatedProxy(proxy_url="http://username:password@proxy-server.com", tmp_folder="/path/to/tmp/folder")
```

To enable the authentication to work properly a chrome extension is being generated (Thanks to [itsmnthn](https://stackoverflow.com/a/55582859/3691763) with an [improvement for manifest v3](https://bugs.chromium.org/p/chromium/issues/detail?id=1135492)).
If the URl doesn't change the extension will not be regenerated. The URL is hashed so that only when the URL has changed (or the tmp folder has changed) a new zip file will be generated.

### Specific issues with headless chrome

If you want to use headless chrome, this functionality only works if you use the following method:

```python
ops.add_argument('--headless=new')
```

The `--headless` method or also the `--headless=chrome` method does not work anymore!

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
