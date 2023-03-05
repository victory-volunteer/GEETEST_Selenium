from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

option = Options()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# 打开chrome浏览器
d = Chrome(options=option)
# 最大化webdriver正在使用的当前窗口
d.maximize_window()
# 因为隐式等待设置是全局的，所以在这儿设置一次就行了
d.implicitly_wait(10)

# 打开携程网注册页面
d.get('https://passport.ctrip.com/user/reg/home')
# 点击同意并继续按钮
d.find_element(By.XPATH, '//*[@id="agr_pop"]/div[3]/a[2]').click()
time.sleep(1)

# ---------------------简单滑块处理---------------------
# 定位到滑块按钮元素
ele_button = d.find_element(By.XPATH, '//*[@id="slideCode"]/div[1]/div[2]')
# 定位到滑块区域元素
ele = d.find_element(By.XPATH, '//*[@id="slideCode"]')
# 打印滑块区域的宽和高
# print('滑块区域的宽：', ele.size['width'])
# print('滑块区域的高：', ele.size['height'])
# 拖动滑块
# 因为这里仅仅是横向移动，仅需要X轴上的偏移量即可，所以这里第二个参数设为0即可
ActionChains(d).drag_and_drop_by_offset(ele_button, ele.size['width'], 0).perform()