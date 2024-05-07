import os
from typing import Optional
from urllib.parse import urlparse
import zipfile

# Thanks to https://bugs.chromium.org/p/chromium/issues/detail?id=1135492
# Latest changes required that the proxy is specified in the extension
# the --proxy-server flag is not enough anymore
# https://www.browserstack.com/guide/set-proxy-in-selenium

DEFAULT_MANIFEST = """
{
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
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

DEFAULT_BACKGROUND_JS_PROXY = """
const config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "%s",
            host: "%s",
            port: %s
        }
    }
}
chrome.proxy.settings.set({
    value: config,
    scope: 'regular'
}, () => {});
"""

DEFAULT_BACKGROUND_AUTO_AUTH = """
chrome.webRequest.onAuthRequired.addListener(
  (details, callback) => {
    const authCredentials = {
      username: "%s",
      password: "%s",
    };
    setTimeout(() => {
      callback({ authCredentials });
    }, 200);
  },
  { urls: ["<all_urls>"] },
  ["asyncBlocking"]
);

"""


class SeleniumExtensionGenerator:
    def generate_extension_zip(
        self,
        proxy_url: Optional[str] = None,
        plugin_file_path: Optional[str] = None,
    ) -> str:
        if not plugin_file_path:
            return

        if not os.path.isdir(plugin_file_path):
            os.makedirs(plugin_file_path)

        with open(os.path.join(plugin_file_path, "manifest.json"), "w") as f:
            f.write(DEFAULT_MANIFEST)
        with open(os.path.join(plugin_file_path, "background.js"), "w") as f:
            f.write(self._get_background_js(proxy_url))

        # make zip file
        with zipfile.ZipFile(f"{plugin_file_path}.zip", "w") as zipf:
            for root, _, files in os.walk(plugin_file_path):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file), plugin_file_path
                        ),
                    )

        return f"{plugin_file_path}.zip"

    def _get_background_js(self, proxy_url):
        urlparse_result = urlparse(proxy_url)
        scheme = urlparse_result.scheme
        port = urlparse_result.port
        username = urlparse_result.username
        password = urlparse_result.password
        if not port:
            if "https" in scheme:
                port = "443"
            else:
                port = "80"
        BACKGROUND_JS = DEFAULT_BACKGROUND_JS_PROXY % (
            scheme,
            urlparse_result.hostname,
            port,
        )
        if username and password:
            BACKGROUND_JS += DEFAULT_BACKGROUND_AUTO_AUTH % (
                username,
                password,
            )
        return BACKGROUND_JS
