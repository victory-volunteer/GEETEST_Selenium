from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

option = Options()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)
driver.maximize_window()

driver.get('https://www.geetest.com/Sensebot')
driver.execute_script('document.documentElement.scrollTop=3713')
driver.find_element(By.XPATH, '//div[@class="box-left"]//li[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//div[@class="geetest_radar_tip"]/span[1]').click()
time.sleep(1)

# ----------------------获取滑块相关图片----------------------
# # 滑块验证码背景图元素
img = driver.find_element(By.XPATH, '//a[@class="geetest_link"]/div[1]')

# 获取缺失滑块图
js = 'document.getElementsByClassName("geetest_canvas_slice geetest_absolute")[0].setAttribute("style","display: none;")'
driver.execute_script(js)
bg = img.screenshot('./bg.png')  # 仅测试
target_bytes = img.screenshot_as_png

# 获取完整图
js = 'document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].style="display: block;"'
driver.execute_script(js)
# fullbg = img.screenshot('./fullbg.png')  # 仅测试
background_bytes = img.screenshot_as_png

# 注意: 此处修改了滑块验证码标签属性后，虽然页面上会显示完整图，但你尽管操作就好，不会影响滑动的

# ----------------------获取滑块位置识别结果----------------------
import ddddocr

det = ddddocr.DdddOcr(det=False, ocr=False)

res = det.slide_comparison(target_bytes, background_bytes)

print('识别结果: ', res)

# ----------------------移动滑块----------------------

# 滑块元素
ele_button = driver.find_element(By.XPATH, '//div[@class="geetest_slider_button"]')
action_chains = webdriver.ActionChains(driver)

# ***************************************************
# 经实测验证得知滑块移动的初始位置，是滑块本身的最左侧，因此只需要将识别出的x轴坐标赋给这里的第一个参数即可（因为这里仅仅是横向移动，仅需要X轴上的偏移量即可，所以这里第二个参数设为0即可）
# 注意: 这里需要减5是为了弥补偏差(滑块距离左边有 5~10 像素左右误差, 具体减多少需要自己观察判断)
# ***************************************************

# 使用此drag_and_drop_by_offset拖动滑块会导致验证失败,因为这个动作太快了,但绝不可以直接加 time.sleep(1) 了,这么做是不会成功的,会提示拼图被怪物吃掉了,请重试
# action_chains.drag_and_drop_by_offset(ele_button, res['target'][0] - 5, 0).perform()

# 实际上人做滑块验证的过程可以归为：手指快速拖拽验证码到指定位置，修正误差，停留一会儿，释放滑块。
# 下面将参考drag_and_drop_by_offset(eleDrag,x,y)的实现，使用move_by_offset方法

action_chains.click_and_hold(ele_button)  # 点击鼠标，准备拖拽
action_chains.pause(0.2)  # 设置停留时间

# 简单实现(滑动虽然慢了，但是立马就移到正确位置，也会被检测出爬虫，因此需要添加修正过程)
# action_chains.move_by_offset(res['target'][0] - 5, 0)
# 修正过程的实现
action_chains.move_by_offset(res['target'][0] - 5 - 10, 0)  # 故意多偏移10
action_chains.pause(0.6)
action_chains.move_by_offset(10, 0)  # 修正刚刚多偏移的10

action_chains.pause(0.6)
action_chains.release()  # 松开鼠标
action_chains.perform()