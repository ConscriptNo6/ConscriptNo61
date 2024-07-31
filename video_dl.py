# coding=utf-8
# date=2024.07.04

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

class VideoDl():
    def __init__(self, jsonl_path, num_needed) -> None:
        # self.video_name = video_name
        # self.video_url = video_url
        self.jsonl_path = jsonl_path
        self.num_needed = num_needed
        self.headers = {
            'Range':'bytes=0-',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

    # 检查视频名称中是否含有Windows非法命名符
    def name_correction(self, name):
        illegal_chars = r'[\\/:"*?<>|]'
        name_corrected = re.sub(illegal_chars, '', name)

        return name_corrected

    # 读取本地jsonl文件，获取视频url、名称
    def read_jsonl(self, jsonl_path):
        url_list = []
        video_name_list = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                info_dict = json.loads(line)
                url_list.append(info_dict["url"])
                video_name_list.append(info_dict["title"])
        return url_list, video_name_list
    
    # 配置无头浏览器
    def driver_nitialize(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1080)
        return driver
    
    # 视频下载
    def video_download(self,):
        url_list, video_name_list = self.read_jsonl(self.jsonl_path)

        for i in range(self.num_needed):
            driver = self.driver_nitialize()
            driver.get(url= url_list[i])
            wait = WebDriverWait(driver, 10)
            find_video_source = wait.until(EC.visibility_of_element_located((By.XPATH, "//video")))
            source_url = find_video_source.get_attribute("src")
            driver.close()

            name_corrected = self.name_correction(video_name_list[i])
            # 将视频内容写入到本地文件
            response = requests.get(url = source_url, headers=self.headers)
            with open(f"./Videos/{name_corrected}.mp4", "wb") as f:
                f.write(response.content)
            
if __name__ == '__main__':
    vd = VideoDl(r'D:\Programming\PythonProject\interview_ques\xpc\video_info.jsonl', 10)
    vd.video_download()