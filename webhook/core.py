import requests
import json
import os

class DiscordWebhook:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()

    def send_message(self, content: str = "", username: str = None, avatar_url: str = None, embeds: list = None):
        data = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
            "embeds": embeds or []
        }

        response = self.session.post(self.url, json=data)
        return self._handle_response(response)

    def send_file(self, file_path: str, content: str = ""):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with open(file_path, 'rb') as f:
            files = {'file': f}
            payload = {'content': content}
            response = self.session.post(self.url, data=payload, files=files)
            return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 204 or response.status_code == 200:
            return {"success": True}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "response": response.text
            }
