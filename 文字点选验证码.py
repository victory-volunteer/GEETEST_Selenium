from selenium import webdriver
from Chaojiying import Chaojiying_Client
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

option = Options()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
device = webdriver.Chrome(options=option)
device.maximize_window()

device.get('https://www.geetest.com/Sensebot')
device.execute_script('document.documentElement.scrollTop=3713')
device.find_element(By.XPATH, '//*[@id="gt-sensebot-mobile"]/div[2]/section[3]/div/div[2]/div[1]/ul/li[3]').click()
time.sleep(2)
device.find_element(By.XPATH, '//*[@id="captcha"]').click()
time.sleep(2)

# ---------------------使用超级鹰图片文字识别---------------------
img1 = device.find_element(By.XPATH, '//div[@class="geetest_widget"]')  # 获取验证码图片元素（以后只需更改这里）

chaojiying = Chaojiying_Client('xxx', 'xxx', '936860')  # 936860是在用户中心,生成的一个软件ID
dic = chaojiying.PostPic(img1.screenshot_as_png, 9004)  # 此图片验证码需要识别2~4个字
# 仅做测试
# dic = {'err_no': 0, 'err_str': 'OK', 'pic_id': '1192522510928630011', 'pic_str': '194,270|47,166|39,288|259,101', 'md5': 'c9651cb286a0fe25fa7c1b68a00c4beb'}
print(dic)

# 若出现问题优先考虑这里的height和width(尝试将下方的['height']和['width']位置互换一下,看坐标点击位置是否正确)
height = img1.size['height']  # 计算图片元素的高
width = img1.size['width']    # 计算图片元素的宽
print(height, width)  

result = dic['pic_str']
rs_list = result.split("|")
for rs in rs_list:  # rs格式为 x1,y1
    p_temp = rs.split(",")
    x = int(p_temp[0]) - width / 2   # 取x轴坐标
    y = int(p_temp[1]) - height / 2  # 取y轴坐标
    print(x, y)
    ActionChains(device).move_to_element_with_offset(img1, x, y).click().perform()
    time.sleep(0.5)

img1.screenshot('./yzm.png')  # 获取点选后的图片（仅做测试）
# ---------------------------------------------------------------

# 点击提交按钮
device.find_element(By.XPATH, '//a[@class="geetest_commit"]').click()