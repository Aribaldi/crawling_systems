import os
import tempfile
import requests


# def check_if_on_network(path: str):
#     supported_protocols = ['http', 'https', 'ftp']
#     for protocol in supported_protocols:
#         if path.startswith(protocol):
#             return True
#     return False

def download_file(url: str) -> str:
    filename = url.split('/')[-1]
    filepath = os.path.join(tempfile.gettempdir(), filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        #file = tempfile.NamedTemporaryFile(mode='wb')
        with open(filepath, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                file.write(chunk)

    return filepath
