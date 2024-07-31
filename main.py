# coding =utf-8
# date=2024.07.04

# from video_dl import VideoDl as vd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

url = 'https://passport.xinpianchang.com/login'

# 配置无头浏览器
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
global driver
driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.get(url=url)

wait = WebDriverWait(driver, 10)

# 输入手机号、密码登录
input_account = driver.find_element(By.ID, 'login_phone')
input_passwd = driver.find_element(By.ID, 'login_password')
input_account.clear()
input_passwd.clear()
input_account.send_keys("")
input_passwd.send_keys("")
submit_but = driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div[2]/div[2]/div/div/div/form/div[4]/div/div/span/button')
submit_but.click()

# 回到主页
back_to_front = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section/header/div/div[2]/ul/li[1]/a')))
back_to_front.click()

# 点击发现
click_discover = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/header/nav/div[2]/div[1]/div/div[2]/div/div[1]/div/a')))
click_discover.click()

# 依次点击“音乐/声音”、“其他”
music_sound = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div[1]/div[1]/div/a[14]/div')))
music_sound.click()
others = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div[1]/div[3]/div/a[6]/div')))
others.click()

# 遍历页面上所有视频的信息
def get_info():
    # 获取60个视频相关信息的父元素
    parent_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='sc-7a811143-0 eVXfIM']")))

    # 遍历每个视频，从父元素中匹配相关的子元素
    for item in range(len(parent_elements)):

        # 提取出视频名称、url
        title_url_element = parent_elements[item].find_element(By.XPATH, ".//a[@class='absolute top-0 inset-x-0 pt-[56.5%]']")
        video_title = title_url_element.get_attribute("aria-label")
        # print(title_url_element.get_attribute("aria-label"))
        video_url = title_url_element.get_attribute("href")
        # print(title_url_element.get_attribute("href"))

        # 提取出视频的标签
        tag_elements = parent_elements[item].find_elements(By.XPATH, ".//div[@class='truncate']")
        for tag_element in tag_elements:
            video_type = tag_element.text
            # print(tag_element.text)

        info_dict = {}
        info_dict['title'] = video_title
        # info_dict['page_url'] = 'https://www.xinpianchang.com/discover/article-27-180'
        info_dict['url'] = video_url
        info_dict['video_type'] = video_type
        print(info_dict)
        json_str = json.dumps(info_dict, ensure_ascii=False)
        with open("./video_info.jsonl", "a", encoding='utf-8') as f:
            f.write(json_str + '\n')

print('第一页')
get_info()

# 遍历第2到第7页
for page_num in range(2, 8):

    # 切换页面
    xpath_expression = f"//a[@aria-label='Page {page_num}']"
    page_swtich_but = driver.find_element(By.XPATH, xpath_expression)
    page_swtich_but.click()

    # 等待页面加载完成
    xpa = f"//a[@aria-label='Page {page_num} is your current page']"
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpa)))
    print(f'第{page_num}页')

    get_info()

driver.close()

