import requests

class GitError(Exception):
    def __init__(self, status_code, *args):
        super().__init__(*args)
        self.status_code = status_code

def get_public_link():
    return f"https://github.com/JediKnightChan/" # To be completed with the actual release page link

def save_response_content(response, destination, chunk_size):
    with open(destination, "ab") as f:
        for i, chunk in enumerate(response.iter_content(chunk_size)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                yield i, chunk_size

def download_file_from_git(destination, chunk_size=32768):
    url_base = get_public_link()

    session = requests.Session()
    params = {}
    response = session.get(url_base + "download/TAG/ECR1.zip", params=params, stream=True) # Need to be changed to correct complementary path

    if response.status_code != 200:
        raise GitError(response.status_code,
                        f"Downloading git release failed, status {response.status_code}")

    for i, chunk_size_ in save_response_content(response, destination, chunk_size):
        yield i, chunk_size_
        
    # Those blocks can be chained to extend the destination file and merge several downloads, I think  
        
    # response = session.get(url_base + "download/TAG/ECR2.zip", params=params, stream=True)

    # if response.status_code != 200:
        # raise GoogleDriveError(response.status_code,
                        # f"Downloading google drive file {file_id} failed, status {response.status_code}")

    # for i, chunk_size_ in save_response_content(response, destination, chunk_size):
        # yield i, chunk_size_
