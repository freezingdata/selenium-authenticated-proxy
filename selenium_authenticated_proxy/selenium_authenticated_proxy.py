import os
import hashlib
import base64
from selenium_authenticated_proxy.selenium_extension_generator import SeleniumExtensionGenerator

class SeleniumAuthenticatedProxy:
    def __init__(self, proxy_url=None, tmp_folder=None):
        """Constructor for initializing proxy_url and tmp_folder."""
        self.proxy_url = proxy_url
        self.tmp_folder = tmp_folder or os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))

    def _get_zip_filename(self):
        input_string = f"{self.proxy_url}"
        
        hasher = hashlib.sha256()
        hasher.update(input_string.encode())
        
        # Get the digest (the hashed value)
        digest = hasher.digest()
        
        # Base64 encode the digest
        base64_digest = base64.b64encode(digest)
        
        return f"{base64_digest.decode()}.zip"

    def _get_zip_filepath(self):
        """Get the full file path for the ZIP file to be stored."""
        return os.path.join(self.tmp_folder, self._get_zip_filename())
    
    def _generate_plugin_file(self):
        """Generate the proxy authentication plugin ZIP file."""
        SeleniumExtensionGenerator().generate_extension_zip(self.proxy_url, self._get_zip_filepath())

    def get_or_generate_plugin_file(self):
        """
        Check if the plugin file already exists.
        If not, generate a new plugin file.
        """
        if not os.path.isfile(self._get_zip_filepath()):
            self._generate_plugin_file()

        # Return path to plugin file
        return self._get_zip_filepath()

    def enrich_chrome_options(self, chrome_options):
        """Add the generated extension to Chrome options."""
        chrome_options.add_extension(self.get_or_generate_plugin_file())
        return chrome_options
