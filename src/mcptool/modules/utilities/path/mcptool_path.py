import subprocess
import requests
import os

from loguru import logger


class MCPToolPath:
    def __init__(self) -> None:
        self.system: str = os.name
        self.urls: dict = self._get_urls()

    def get(self) -> str:
        """
        Method to get the path of the MCPTool folder
        and create it if it doesn't exist

        Returns:
            str: Path of the MCPTool folder
        """

        if self.system == 'nt':
            path = os.path.abspath(os.path.join(os.getenv('APPDATA'), 'MCPTool'))

        else:
            path = os.path.abspath(os.path.join(os.getenv('HOME'), '.config', 'mcptool'))

        if not os.path.exists(path):
            logger.info(f'Creating MCPTool folder in {path}')
            os.makedirs(os.path.join(path), exist_ok=True)

        return path
    
    def check_files(self) -> None:
        """
        Method to check if the files exist and 
        download them if they don't
        """

        for url in self.urls.values():
            if not os.path.exists(url['path']):
                logger.info(f'Downloading {url["path"]}')
                self.download_file(url['url'], url['path'])

        if not os.path.exists(os.path.join(self.get(), 'node_modules')):
            logger.info('Installing node modules')
            subprocess.run(f'cd {self.get()} && npm install', shell=True)

    def download_file(self, url: str, path: str) -> None:
        """
        Method to download the file

        Args:
            url (str): URL of the file
            path (str): Path to save the file
        """

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            response = requests.get(url)

            if response.status_code != 200:
                logger.error(f'Error downloading file: {response.status_code}')
                return

            with open(path, 'wb') as file:
                if response.content is None:
                    logger.error(f'Error downloading file: {response.content}')
                    return

                file.write(response.content)
        
        except Exception as e:
            logger.error(f'Error downloading file: {e}')

    def _get_urls(self) -> dict:
        """
        Method to get the URLs of the files

        Returns:
            dict: URLs of the files
        """
        
        return {
            'settings': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'settings.json'))
            },
            'language_en': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/languages/en.json',
                'path': os.path.abspath(os.path.join(self.get(), 'languages', 'en.json'))
            },
            'bot_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/bot.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'bot.mjs'))
            },
            'sever_response_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/server_response.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'server_response.mjs'))
            },
            "package": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/package.json",
                "path": os.path.abspath(os.path.join(self.get(), "package.json"))
            }
        }
