import requests


class GoogleDriveError(Exception):
    def __init__(self, status_code, *args):
        super().__init__(*args)
        self.status_code = status_code


def get_public_gdrive_link(gdrive_id):
    return f"https://drive.google.com/file/d/{gdrive_id}/view?usp=share_link"


def download_file_from_google_drive(file_id, destination, chunk_size=32768):
    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    params = {'id': file_id, 'confirm': 1}
    response = session.get(url, params=params, stream=True)

    if response.status_code != 200:
        raise GoogleDriveError(response.status_code,
                               f"Downloading google drive file {file_id} failed, status {response.status_code}")

    for i, chunk_size_ in save_response_content(response, destination, chunk_size):
        yield i, chunk_size_


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination, chunk_size):
    with open(destination, "wb") as f:
        for i, chunk in enumerate(response.iter_content(chunk_size)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                yield i, chunk_size


if __name__ == '__main__':
    file_id = '1X5NtVseRWdsqItahMAwUBwneZhfWxEXA'
    destination = '/home/jediknight/Documents/SmallPythons/ECLauncher/Source/ecr.zip'
    for i, chunk_size in download_file_from_google_drive(file_id, destination):
        print(i, chunk_size)
