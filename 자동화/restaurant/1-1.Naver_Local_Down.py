
import selenium.webdriver as webdriver
import chromedriver_autoinstaller
import os
import selenium.webdriver.common.by as By
import functools as ft
import shutil
import time

url="https://www.localdata.go.kr/devcenter/dataDown.do?menuNo=20001"
try:
    chromedriver_autoinstaller.install()
except:
    pass

# 현재 경로에 다운로드 경로를 넣어줘야함
temp_location=os.getcwd()
if not os.path.exists(temp_location+"/Data"):
  os.mkdir(temp_location+"/Data") 
else:
  shutil.rmtree(temp_location+"/Data")
  os.mkdir(temp_location+"/Data") 
# os.removedirs(temp_location+"/Data") 지우기

# 다운로드 경로 변경
temp_option=webdriver.ChromeOptions()
temp_option.add_experimental_option("prefs", {
  "download.default_directory": temp_location+"/Data",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True})
temp_option.add_argument("--disable-notifications")  # 알림 끄기
temp_option.add_argument("--disable-popup-blocking")  # 팝업 차단 해제
temp_option.add_argument("--disable-infobars")  # 정보 표시줄 숨기기
temp_option.add_argument("--disable-web-security")  # 웹 보안 비활성화

# 셀레니움
driver=webdriver.Chrome(temp_option)
driver.get(url)
driver.implicitly_wait(2)

# 함수화
def find_botton(x:webdriver.Chrome,css:str,distinct:str=None):
    if distinct:
      bottons_result=[t for t in x.find_elements(By.By.CSS_SELECTOR,css) if t.text==distinct][0]
    else:
      bottons_result=x.find_elements(By.By.CSS_SELECTOR,css)
    return bottons_result

bott=ft.partial(find_botton,x=driver)

# 식품 카테고리
food_1=bott(css=".category-nm",distinct="식품")
food_1.click()
time.sleep(3)

# 식품>음식점 카테고리
food_2=bott(css=".grouplist_a",distinct="음식점")
food_2.click()
time.sleep(3)

# 음식점 하위 태그(관광식당, 일반음식점, 휴게음식점) 카테고리
food_3=bott(css="tbody.downtdcss tr")
time.sleep(3)

# 함수화(위의 태그값들을 확인한 뒤에 해당 항목 선택)
def find_cate_botton(x:list[webdriver.remote.webelement.WebElement]=[],li:list[str]=[],**kwargs)->None:
    for sub_ in x:
        if sub_.find_element(By.By.CSS_SELECTOR,"td").text in li: #음식점 하위태그 확인
            for down_sub in sub_.find_elements(By.By.CSS_SELECTOR,".down-btn a"):
               if down_sub.text=="CSV":
                  down_sub.click()
        else:
            pass
        time.sleep(1)
# 변경가능
sub_cate=['관광식당','일반음식점','휴게음식점']

find_cate_botton(x=food_3,li=sub_cate)

# 셀레니움 종료 준비(경로가 이미 지정되서 필요없을듯)
counter=ft.partial(lambda x:len(os.listdir(x)),x=temp_location+"/Data") # 다운받은 파일 개수를 확인하기 위함

location=counter()
while location!=len(sub_cate):
    time.sleep(2)
    location=counter()

# 다운로드 시간은 조정이 필요할 듯
time.sleep(60)

# 종료
driver.quit()
