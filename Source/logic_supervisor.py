import json
import os
import hashlib
import shutil
import threading
import time
import webbrowser

import requests
import zipfile

from PIL import Image
from io import BytesIO
from PyQt6.QtCore import pyqtSignal, QObject

from git_downloader import download_file_from_git, GitError
from gdrive_downloader import get_public_gdrive_link
from ecr_logging import log
from detached_process_launcher import run_detached_process


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class LogicSupervisor(QObject):
    can_play_changed = pyqtSignal()
    status_changed = pyqtSignal()
    progress_changed = pyqtSignal()
    launcher_update_needed = pyqtSignal()
    want_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.api_root = "https://ecr-service.website.yandexcloud.net/api/ecr/"
        self.game_platform = "Windows"
        self.current_launcher_version = "1.0.1"

        self.__branch = None
        self.__game_version = None
        self.__can_play = False
        self.__status = ""
        self.__status_speed = ""
        self.__progress = 0
        self.stop_requested = False
        self.discord_link = None
        self.site_link = None

        self.game_folder = "ecr"
        self.threads = []

    # API requests

    def __make_api_get_request(self, url, default_list=False):
        try:
            r = requests.get(url)
            result = r.json()
        except Exception as e:
            log(e)
            if default_list:
                result = []
            else:
                result = {}
        return result

    def get_patch_notes(self):
        return self.__make_api_get_request(self.api_root + "patch_notes.json", default_list=True)

    def get_news(self):
        news_raw = self.__make_api_get_request(self.api_root + "news.json", default_list=True)
        news_handled = []
        for raw_el in news_raw:
            image = raw_el["image"]
            image = self.api_root + image
            if image.startswith("https://") or image.startswith("http://"):
                r = requests.get(image)
                if not r.status_code == 200:
                    log(f"Couldn't load image {image}, {r.status_code}")
                    continue
                img = Image.open(BytesIO(r.content))
                raw_el["image"] = img
            else:
                continue

            news_handled.append(raw_el)
        return news_handled

    def get_versioning_data(self):
        return self.__make_api_get_request(self.api_root + "versioning_data.json").get(self.get_current_branch(), {})

    def get_game_data(self):
        return self.__make_api_get_request(self.api_root + "game_data.json").get(self.get_current_branch(), {})

    # Settings

    def __load_setting_from_file(self, setting, default_value=None):
        if not os.path.exists("settings.json"):
            return default_value

        with open("settings.json", "rb") as f:
            try:
                data = json.load(f)
            except:
                return default_value

            if setting in data:
                return data[setting]
            else:
                return default_value

    def get_current_game_version(self):
        self.__game_version = self.__load_setting_from_file("version")
        return self.__game_version

    def set_current_game_version(self, version):
        self.__game_version = version
        self.save_settings()

    def get_allowed_branches(self):
        return ["branch_prod", "branch_dev"]

    def get_default_branch(self):
        return self.get_allowed_branches()[0]

    def get_current_branch(self):
        self.__branch = self.__load_setting_from_file("branch", default_value=self.get_default_branch())
        if self.__branch not in self.get_allowed_branches():
            self.__branch = self.get_default_branch()
        return self.__branch

    def get_latest_game_version(self):
        r = self.__make_api_get_request(self.api_root + "game_data.json")
        return r.get(self.get_current_branch(), {}).get("version", None)

    def save_settings(self):
        settings = {"version": self.__game_version}
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    # Getters and setters

    def set_can_play(self, can_play):
        self.__can_play = can_play
        self.can_play_changed.emit()

    def get_can_play(self):
        return self.__can_play

    def set_status(self, status):
        self.__status = status
        self.status_changed.emit()

    def get_status(self):
        return self.__status

    def set_status_speed(self, status_speed):
        self.__status_speed = status_speed
        self.status_changed.emit()

    def get_status_speed(self):
        return self.__status_speed

    def set_progress(self, value):
        self.__progress = value
        self.progress_changed.emit()

    def get_progress(self):
        return self.__progress

    # Functionality

    @staticmethod
    def open_internet_link(url):
        webbrowser.open(url, new=2)

    def get_can_exit(self):
        can_exit = True
        for t in self.threads:
            if t.is_alive():
                can_exit = False
        return can_exit

    def check_for_launcher_updates(self):
        launcher_data = self.__make_api_get_request(self.api_root + "launcher_data.json")
        latest_version = launcher_data.get("version", None)

        self.discord_link = launcher_data.get("discord_link", None)
        self.site_link = launcher_data.get("site_link", None)

        if not latest_version:
            # No internet or corrupt server data
            self.set_status("No Internet connection...")
            return None

        if latest_version == self.current_launcher_version:
            # Launcher is of latest version
            return False

        # Launcher not the latest version, download update

        platform_data = launcher_data.get("complete_archives", {}).get(self.game_platform, {})
        gdrive_id = platform_data.get("gdrive_id", None)
        github_chunk_urls = platform_data.get("github_chunk_urls", [])
        size = platform_data.get("size", None)
        real_hash = platform_data.get("hash", "")

        if gdrive_id is None or size is None:
            # Server corrupt data
            self.set_status("Error updating launcher... Please, contact support")
            return None

        zip_destination = "launcher.zip"
        if os.path.exists(zip_destination) and md5(zip_destination) == real_hash:
            # Already downloaded
            return True

        status_format_string = f"Downloading launcher update {latest_version}..." + \
                               " {remaining_gb:.2f} GB remaining"
        download_success, status_code = self.download_github_release(status_format_string, github_chunk_urls, size,
                                                                     zip_destination)
        if not download_success:
            if status_code == 429:
                self.open_internet_link(get_public_gdrive_link(gdrive_id))
                self.set_status(
                    "Failed downloading launcher update. Please, download launcher.zip manually and extract it to the launcher folder")
            else:
                self.set_status("Error downloading launcher update... Please, contact support")
            return None

        return True

    def install_latest_patches(self, current_game_version):
        versioning_data = self.get_versioning_data()

        later_versions_data = []
        met_current_game_version = False
        for k, v in versioning_data.items():
            if met_current_game_version:
                later_versions_data.append((k, v))
            if k == current_game_version:
                met_current_game_version = True

        patch_amount = len(later_versions_data)
        for i, tuple_ in enumerate(later_versions_data):
            version, version_data = tuple_
            success = self.install_patch(version, version_data, i, patch_amount)
            if not success:
                self.set_status(
                    "Installing patch failed. If problem persists after restart, delete settings.json and restart to reinstall whole game")
                return

        # Check integrity
        game_broken = self.verify_game_version_hashes()
        if game_broken:
            self.set_status(
                "Game integrity is violated. Delete settings.json to reinstall whole game")
        else:
            self.set_status("")
            self.set_can_play(True)

    def install_patch(self, version, version_data, i, patch_amount):
        platform_data = version_data.get(self.game_platform, {})
        gdrive_id = platform_data.get("gdrive_id", None)
        github_chunk_urls = platform_data.get("github_chunk_urls", [])
        size = platform_data.get("size", None)

        if not gdrive_id or not size:
            return False

        zip_destination = "patch.zip"
        if os.path.exists(zip_destination):
            os.remove(zip_destination)

        status_format_string = f"Downloading patch {version} ({i + 1}/{patch_amount})..." + \
                               " {remaining_gb:.2f} GB remaining"

        download_success, _ = self.download_github_release(status_format_string, github_chunk_urls, size,
                                                           zip_destination)
        if not download_success:
            return False

        self.set_progress(0)
        self.set_status_speed("")
        self.set_status(f"Installing patch {version} ({i + 1} / {patch_amount})")

        os.makedirs(self.game_folder, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_destination, 'r') as zip_ref:
                zip_ref.extractall(self.game_folder)
        except Exception as e:
            log(e)
            os.remove(zip_destination)
            return False

        os.remove(zip_destination)

        self.set_status("")
        self.set_current_game_version(version)

        return True

    def verify_and_check_for_updates(self):
        t = threading.Thread(target=self.__verify_and_check_for_updates_implementation)
        t.start()
        self.threads.append(t)

    def __verify_and_check_for_updates_implementation(self):
        self.set_status("Preparing...")

        launcher_updates_result = self.check_for_launcher_updates()
        if launcher_updates_result is None:
            return
        elif launcher_updates_result is True:
            # Launcher update downloaded
            self.launcher_update_needed.emit()
            return

        latest_game_version = self.get_latest_game_version()
        if not latest_game_version:
            # No internet or corrupt server data
            self.set_status("No Internet connection...")
            return

        current_game_version = self.get_current_game_version()
        if current_game_version is None:
            # Current version is unknown, install from scratch
            return self.download_and_install_game_full()
        else:
            # Current version is known
            versioning_data = self.get_versioning_data()
            if versioning_data == {}:
                # No internet or corrupt server data
                self.set_status("No Internet connection...")
                return
            if current_game_version not in versioning_data:
                # Current version is not supported anymore, install from scratch
                return self.download_and_install_game_full(reinstalling=True)
            else:
                # Current version is supported
                if current_game_version != latest_game_version:
                    # Need update, current version != latest
                    return self.install_latest_patches(current_game_version)
                else:
                    # Latest version is same as current, check integrity
                    game_broken = self.verify_game_version_hashes()

                    if game_broken:
                        return self.download_and_install_game_full(True)
                    else:
                        self.set_status("")
                        self.set_can_play(True)
                        return

    def verify_game_version_hashes(self):
        self.set_status("Verifying...")

        data = self.get_game_data()
        verify_files_data = data.get("complete_archives", {}).get(self.game_platform, {}).get("verify_files", {})

        game_broken = False
        for file, file_hash in verify_files_data.items():
            fp = os.path.join(self.game_folder, self.game_platform, file)
            if not os.path.exists(fp):
                game_broken = True
                log(f"Verifying game integrity: {fp} doesn't exist")
                break
            current_hash = md5(fp)
            if current_hash != file_hash:
                log(f"Verifying game integrity: {fp} hash {current_hash} doesn't match expected {file_hash}")
                game_broken = True
        return game_broken

    def download_and_install_game_full(self, reinstalling=False):
        if reinstalling:
            base_status_text = "Reinstalling game..."
        else:
            base_status_text = "Downloading game..."

        self.set_status(base_status_text)

        zip_destination = "game.zip"

        # Deleting folder contents and recreating it
        if os.path.exists(self.game_folder):
            shutil.rmtree(self.game_folder)
        os.makedirs(self.game_folder, exist_ok=True)

        data = self.get_game_data()
        version = data.get("version", None)
        platform_data = data.get("complete_archives", {}).get(self.game_platform, {})
        gdrive_id = platform_data.get("gdrive_id", None)
        github_chunk_urls = platform_data.get("github_chunk_urls", [])
        size = platform_data.get("size", None)
        complete_archive_hash = platform_data.get("hash", None)

        if version is None or gdrive_id is None or size is None:
            log(f"Installing full game, got None in version {version}, gdrive {gdrive_id}, size {size}")
            self.set_status("No internet connection...")
            return

        skip_downloading = False
        if os.path.exists(zip_destination):
            calculated_hash = md5(zip_destination)
            if calculated_hash == complete_archive_hash:
                log(f"Installing full game, found {zip_destination}, md5 {complete_archive_hash} matched")
                skip_downloading = True
            else:
                log(f"Installing full game, found {zip_destination}, md5 {calculated_hash} didn't match expected {complete_archive_hash}")
                os.remove(zip_destination)

        if not skip_downloading:
            status_format_string = base_status_text + " {remaining_gb:.2f} GB remaining"
            download_success, status_code = self.download_github_release(status_format_string, github_chunk_urls, size,
                                                                         zip_destination)
            if not download_success:
                if status_code == 429:
                    self.open_internet_link(get_public_gdrive_link(gdrive_id))
                    self.set_status(
                        "Failed downloading game. Please, download game.zip manually, copy it into the launcher folder and restart")
                else:
                    self.set_status(
                        "Failed downloading game. Please, restart launcher, and if problem persists, contact support")
                return

        self.set_status_speed("")
        self.set_progress(0)
        self.set_status("Installing game...")

        try:
            with zipfile.ZipFile(zip_destination, 'r') as zip_ref:
                zip_ref.extractall(self.game_folder)
        except Exception as e:
            log(e)
            os.remove(zip_destination)
            self.set_status(
                "Error occurred while installing game. Please, restart launcher, and if problem persists, contact support")
            return

        os.remove(zip_destination)

        self.set_current_game_version(version)

        game_broken = self.verify_game_version_hashes()
        if game_broken:
            self.set_status(
                "Game integrity is violated. Please, restart launcher, and if problem persists, contact support")
        else:
            self.set_status("")
            self.set_can_play(True)

    def download_github_release(self, status_format_string, release_chunks_urls, size, zip_destination):
        self.set_progress(0)

        n_seconds = 10
        downloaded_this_n_seconds = 0
        last_time = time.time()

        try:
            with open(zip_destination, "wb") as f:
                f.write(b"")

            downloaded = 0
            for chunk_url in release_chunks_urls:
                for i, chunk_size in download_file_from_git(chunk_url, zip_destination):
                    if self.stop_requested:
                        return False, 0
                    downloaded += chunk_size

                    progress_percent = downloaded / size * 100
                    remaining = max(size - downloaded, 0)
                    gb = 1_000_000_000

                    new_time = time.time()
                    if new_time - last_time <= n_seconds:
                        if new_time - last_time != 0:
                            downloaded_this_n_seconds += chunk_size
                            speed_mb = downloaded_this_n_seconds / (new_time - last_time) / 1_000_000
                            self.set_status_speed(f"{int(speed_mb)} MB/s")
                    else:
                        downloaded_this_n_seconds = chunk_size
                        last_time = new_time
                        self.set_status_speed(f"0 MB/s")

                    self.set_status(status_format_string.format(remaining_gb=remaining / gb))
                    self.set_progress(int(progress_percent))

            self.set_progress(100)
            return True, 0
        except GitError as e:
            log(e)
            self.set_status_speed("")
            return False, e.status_code
        except Exception as e:
            log(e)
            self.set_status_speed("")
            return False, 1

    @staticmethod
    def run_detached_process(cmd):
        run_detached_process(cmd)

    def launch_game(self):
        self.set_can_play(False)

        t = threading.Thread(target=self.__launch_game_implementation)
        t.start()
        self.threads.append(t)

    def __launch_game_implementation(self):
        if self.game_platform == "Windows":
            cmd = f"ecr/{self.game_platform}/ECR.exe"
        else:
            cmd = None

        if cmd:
            self.run_detached_process(cmd)

        time.sleep(5)
        self.want_close.emit()
