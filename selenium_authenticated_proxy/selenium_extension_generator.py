
from urllib.parse import urlparse
import zipfile


DEFAULT_MANIFEST = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

DEFAULT_BACKGROUND_JS = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "%s",
            host: "%s",
            port: %s
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, () => {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""



class SeleniumExtensionGenerator:
    @classmethod
    def generate_extension_zip(self, proxy_url=None, plugin_file_path=None):
        with zipfile.ZipFile(plugin_file_path, 'w') as zp:
            zp.writestr("manifest.json", DEFAULT_MANIFEST)
            zp.writestr("background.js", self._get_background_js(proxy_url))

    @classmethod
    def _get_background_js(self, proxy_url):
        urlparse_result = urlparse(proxy_url)
        scheme = urlparse_result.scheme
        host = urlparse_result.hostname
        port = urlparse_result.port
        username = urlparse_result.username
        password = urlparse_result.password
        if not port:
            if 'https' in scheme:
                port = '443'
            else:
                port = '80'
        return DEFAULT_BACKGROUND_JS % (scheme, host, int(port), username, password)
