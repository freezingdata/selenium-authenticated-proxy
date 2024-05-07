import hashlib
import os
from urllib.parse import urlparse

from selenium_authenticated_proxy.selenium_extension_generator import (
    SeleniumExtensionGenerator,
)


class SeleniumAuthenticatedProxy:
    def __init__(self, proxy_url=None, tmp_folder=None):
        """Constructor for initializing proxy_url and tmp_folder."""
        self.proxy_url = proxy_url
        self.tmp_folder = tmp_folder or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "tmp")
        )

    def _get_zip_filename(self):
        input_string = f"{self.proxy_url}"

        hasher = hashlib.sha256()
        hasher.update(input_string.encode())

        # Get the digest (the hashed value)
        digest = hasher.digest()

        # Hex encode the digest
        hex_digest = digest.hex()

        return f"{hex_digest}"

    def _get_zip_filepath(self):
        """Get the full file path for the ZIP file to be stored."""
        if not os.path.exists(self.tmp_folder):
            os.mkdir(self.tmp_folder)
        return os.path.join(self.tmp_folder, self._get_zip_filename())

    def _generate_plugin_file(self) -> str:
        """Generate the proxy authentication plugin ZIP file."""
        return SeleniumExtensionGenerator().generate_extension_zip(
            self.proxy_url, self._get_zip_filepath()
        )

    def _get_unauthenticated_url(self):
        result = urlparse(self.proxy_url)
        return f"{result.hostname}:{result.port}"

    def _get_scheme(self):
        result = urlparse(self.proxy_url)
        return result.scheme

    def _is_authenticated_url(self):
        result = urlparse(self.proxy_url)
        return result.username is not None

    def enrich_chrome_options(self, chrome_options):
        """Add the generated extension to Chrome options."""
        if not self.proxy_url:
            return chrome_options
        if self._is_authenticated_url():
            chrome_options.add_extension(self._generate_plugin_file())
        chrome_options.add_argument(
            f"--proxy-server={self._get_unauthenticated_url()}"
        )
        return chrome_options
