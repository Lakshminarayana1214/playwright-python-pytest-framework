import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def get(self, endpoint, params=None):
            response = self.session.get(f"{self.base_url}{endpoint}",params=params,timeout=15)
            return response

    def post(self, endpoint, data=None):
        response = self.session.post(f"{self.base_url}{endpoint}",json=data,timeout=15)
        return response
