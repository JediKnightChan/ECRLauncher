import requests


class GitError(Exception):
    def __init__(self, status_code, *args):
        super().__init__(*args)
        self.status_code = status_code


def save_response_content(response, destination, chunk_size):
    with open(destination, "ab") as f:
        for i, chunk in enumerate(response.iter_content(chunk_size)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                yield i, chunk_size


def download_file_from_git(git_url, destination, chunk_size=32768):
    session = requests.Session()
    params = {}
    response = session.get(git_url, params=params, stream=True)

    if response.status_code != 200:
        raise GitError(response.status_code,
                       f"Downloading git release failed, status {response.status_code}")

    for i, chunk_size_ in save_response_content(response, destination, chunk_size):
        yield i, chunk_size_
