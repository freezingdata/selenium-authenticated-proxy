import hashlib
import os
import shutil
from urllib.parse import urlparse

from selenium_authenticated_proxy.selenium_extension_generator import \
    SeleniumExtensionGenerator


class SeleniumAuthenticatedProxy:
    def __init__(self, proxy_url=None, tmp_folder=None, disable_caching=False):
        """Constructor for initializing proxy_url and tmp_folder."""
        self.proxy_url = proxy_url
        self.disable_caching = disable_caching
        self.tmp_folder = tmp_folder or os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))

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
    
    def _generate_plugin_file(self):
        """Generate the proxy authentication plugin ZIP file."""
        SeleniumExtensionGenerator().generate_extension_zip(self.proxy_url, self._get_zip_filepath())

    def get_or_generate_plugin_file(self):
        """
        Check if the plugin file already exists.
        If not, generate a new plugin file.
        """
        if self.disable_caching and os.path.exists(self._get_zip_filepath()):
            # remove the folder at the path
            shutil.rmtree(self._get_zip_filepath())

        if not os.path.exists(self._get_zip_filepath()):
            self._generate_plugin_file()

        # Return path to plugin file
        return self._get_zip_filepath()

    def _get_unauthenticated_url(self):
        result = urlparse(self.proxy_url)
        return f'{result.scheme}://{result.hostname}:{result.port}'
    
    def _is_authenticated_url(self):
        result = urlparse(self.proxy_url)
        return result.username is not None

    def enrich_chrome_options(self, chrome_options):
        """Add the generated extension to Chrome options."""
        if self._is_authenticated_url():
            chrome_options.add_argument(f"--load-extension={self.get_or_generate_plugin_file()}")
        chrome_options.add_argument(f"--proxy-server={self._get_unauthenticated_url()}")
        return chrome_options
