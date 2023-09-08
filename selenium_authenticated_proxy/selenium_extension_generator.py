
from urllib.parse import urlparse
import os

# Thanks to https://bugs.chromium.org/p/chromium/issues/detail?id=1135492

DEFAULT_MANIFEST = """
{
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "Chrome Proxy",
    "permissions": [
        "webRequest",
        "webRequestAuthProvider"
    ],
    "background": {
        "service_worker": "background.js"
    },
    "host_permissions": [
        "<all_urls>"
    ],
    "minimum_chrome_version":"22.0.0"
}
"""

DEFAULT_BACKGROUND_JS = """
chrome.webRequest.onAuthRequired.addListener(
  (details, callback) => {
    const authCredentials = {
      username: "%s",
      password: "%s",
    };
    setTimeout(() => {
      callback({ authCredentials });
    }, 20);
  },
  { urls: ["<all_urls>"] },
  ["asyncBlocking"]
);

"""



class SeleniumExtensionGenerator:
    @classmethod
    def generate_extension_zip(self, proxy_url=None, plugin_file_path=None):
        os.mkdir(plugin_file_path)
        with open(os.path.join(plugin_file_path, "manifest.json"), 'w') as f:
            f.write(DEFAULT_MANIFEST)
        with open(os.path.join(plugin_file_path, "background.js"), "w") as f:
            f.write(self._get_background_js(proxy_url))

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
        return DEFAULT_BACKGROUND_JS % (username, password)
