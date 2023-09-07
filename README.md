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
pip install selenium-authenticated-proxy-helper
```

## Usage

### Basic Usage

Here is how you can set up the authenticated proxy for Selenium's Chrome WebDriver:

```python
from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

# Initialize SeleniumAuthenticatedProxy
proxy_helper = SeleniumAuthenticatedProxy(proxy_url="http://username:password@proxy-server.com")

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()

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

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

