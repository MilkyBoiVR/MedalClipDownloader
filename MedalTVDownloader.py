# THIS PROJECT WAS MADE BY @MILKYBOIVR

import customtkinter as ctk
from tkinter import filedialog
import os
import threading
import time
import cv2
import pyautogui
import numpy as np
import pyperclip
import requests
from bs4 import BeautifulSoup
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

MAX_WORKERS = 10
RETRY_LIMIT = 10

class DownloadTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MedalTVDownloader")
        self.geometry("400x300")
        self.resizable(False, False)

        self.total_clips = 0
        self.clips_downloaded = 0
        self.download_thread = None
        self.running = False
        self.download_path = ""

        self.create_widgets()

    def create_widgets(self):
        self.directory_label = ctk.CTkLabel(self, text="Save Directory:")
        self.directory_label.pack(pady=10)

        self.directory_entry = ctk.CTkEntry(self, placeholder_text="Select directory")
        self.directory_entry.pack(pady=5, padx=20, fill='x')

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)

        self.view_button = ctk.CTkButton(self, text="View Videos", command=self.view_videos)
        self.view_button.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Download", command=self.start_download)
        self.start_button.pack(pady=10)

        self.progress_label = ctk.CTkLabel(self, text="0 Clips Downloaded out of 0")
        self.progress_label.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, ctk.END)
            self.directory_entry.insert(0, directory)
            self.download_path = directory

    def view_videos(self):
        if os.path.isdir(self.download_path):
            os.startfile(self.download_path)
        else:
            ctk.CTkMessageBox.show_error("Error", "Invalid directory")

    def start_download(self):
        if not os.path.isdir(self.download_path):
            ctk.CTkMessageBox.show_error("Error", "Invalid directory")
            return

        if self.running:
            ctk.CTkMessageBox.show_info("Info", "Download already in progress")
            return

        button_img_path = 'button.png'
        if not os.path.exists(button_img_path):
            ctk.CTkMessageBox.show_error("Error", "Button image not found")
            return

        button_img = cv2.imread(button_img_path, cv2.IMREAD_GRAYSCALE)
        self.total_clips = 0
        self.clips_downloaded = 0
        self.running = True

        self.download_thread = threading.Thread(target=self.run_download, args=(button_img,))
        self.download_thread.start()

    def run_download(self, button_img):
        links = self.auto_scroll_and_detect(button_img)
        self.total_clips = len(links)
        if self.total_clips > 0:
            self.download_videos_concurrently(links)

    def auto_scroll_and_detect(self, button_img):
        screen_width, screen_height = pyautogui.size()
        links = []
        
        pyautogui.scroll(-int(screen_height / 1.5))
        time.sleep(0.5)
        
        while True:
            screen = np.array(pyautogui.screenshot())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            if self.is_button_present(screen_gray, button_img):
                result = cv2.matchTemplate(screen_gray, button_img, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                locations = np.where(result >= threshold)
                
                for pt in zip(*locations[::-1]):
                    click_position = (pt[0], pt[1])
                    
                    pyautogui.click(click_position)
                    
                    link_text = pyperclip.paste()
                    if link_text and link_text not in links:
                        links.append(link_text)
                        self.update_progress()
                
                pyautogui.scroll(-int(screen_height / 1.5))
                time.sleep(0.1)
            
            else:
                break
        
        return links

    def is_button_present(self, screen_gray, button_img):
        result = cv2.matchTemplate(screen_gray, button_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)
        return len(locations[0]) > 0

    def get_medal_tv_title(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.show_error_message(f"Error fetching title: {e}")
            return "Error: Unable to fetch the page"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        
        if title_tag:
            title_text = title_tag.text.strip()
            if '- Clipped with Medal.tv' in title_text:
                title_text = title_text.replace('- Clipped with Medal.tv', '').strip()
            return title_text
        else:
            return "Error: Title not found"

    def sanitize_filename(self, filename):
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return filename.rstrip()

    def get_unique_filename(self, base_path, base_filename):
        counter = 1
        filename = f"{base_filename}.mp4"
        full_path = os.path.join(base_path, filename)
        
        while os.path.exists(full_path):
            filename = f"{base_filename}_{counter}.mp4"
            full_path = os.path.join(base_path, filename)
            counter += 1
        
        return filename

    def download_video(self, url, filename, attempt=1):
        if not url or 'medal' not in url:
            self.show_error_message(f'Invalid URL: {url}')
            return

        url = url.replace('?theater=true', '')
        try:
            html = requests.get(url, timeout=10).text
            file_url = html.split('"contentUrl":"')[1].split('","')[0] if '"contentUrl":"' in html else None

            if file_url:
                filename = os.path.join(self.download_path, self.get_unique_filename(self.download_path, self.sanitize_filename(filename)))
                with requests.get(file_url, stream=True, timeout=10) as response:
                    response.raise_for_status()
                    total_length = int(response.headers.get('content-length', 0))
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            f.write(chunk)
                            self.update_progress()

                self.clips_downloaded += 1
                self.update_progress()
            else:
                self.show_error_message('Error: Most likely, direct link download does not exist')
        except requests.RequestException as e:
            if attempt < RETRY_LIMIT:
                wait_time = random.uniform(1, 3)
                time.sleep(wait_time)
                self.download_video(url, filename, attempt + 1)
            else:
                self.show_error_message(f'Error: {e}')

    def download_videos_concurrently(self, links):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_link = {}
            for link in links:
                title = self.get_medal_tv_title(link)
                if not title.startswith("Error"):
                    future = executor.submit(self.download_video, link, title)
                    future_to_link[future] = link
                else:
                    self.show_error_message(title)
            
            for future in as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    future.result()
                except Exception as exc:
                    self.show_error_message(f'Error downloading {link}: {exc}')
        
        self.running = False
        self.update_progress()

    def update_progress(self):
        self.progress_label.configure(text=f"{self.clips_downloaded} Clips Downloaded out of {self.total_clips}")

    def show_error_message(self, message):
        ctk.CTkMessageBox.show_error("Error", message)

if __name__ == '__main__':
    app = DownloadTool()
    app.mainloop()

# THIS PROJECT WAS MADE BY @MILKYBOIVR