#필요한 모듈 모음입니다
from collections import OrderedDict,deque
from functools import partial
import inspect
from typing import Callable,Any,List,AnyStr
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import bs4
import pandas as pd
import re
import json
import csv
import os
import time
import threading as thd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

def read_json(file_path:str,encoding="utf-8",distinct:str="",index:int=0,*args,**kwargs):
    '''
    json으로 파일경로등을 관리할 경우 읽어내기 위한 함수입니다.
    json 파일에서 구별자는 distinct, 정보는 info ,사용하는 값은 value 에 담아놨습니다
    '''
    with open(file_path,"r",encoding=encoding) as f:
        if distinct:
            result=[json.loads(temp) for temp in f.readlines() if json.loads(temp)["distinct"]==distinct][0]["value"]
        else:
            if index:
                result=[json.loads(temp) for temp in f.readlines()][index]["value"]
            else:
                result=[json.loads(temp) for temp in f.readlines()]
    return result

def find_css(driver:Chrome,using_method:By=By.CSS_SELECTOR,css:str="",attribute:str="",distinct:str="",*args,**kwargs):
    '''attribute와 distinct를 사용해서 특정 타입의 요소를 찾는 것을 도와줄 겁니다.'''
    if all([attribute,distinct]):
        WebDriverWait(driver,3).until(visibility_of_all_elements_located((using_method,css)))
        result=[x for x in driver.find_elements(using_method,css) if x.get_attribute(attribute)==distinct]
    elif bool(attribute)!=bool(distinct):
        Warning.add_note('''/n 원하는 attribute 혹은 attribute의 결과값이 입력되지 않았습니다.''')
    else:
        WebDriverWait(driver,3).until(visibility_of_all_elements_located((using_method,css)))
        result=[x for x in driver.find_elements(using_method,css)]
    if len(result)==1:
        return result[0]
    else:
        return result

def find_css_v2(driver:Chrome,using_method:By=By.CSS_SELECTOR,css:str="",txt:str="",*args,**kwargs):
    '''해당 요소의 text을 확인하여 css 값을 가져옵니다.
    예를 들어 해당 css 구성요소의 text값이 '안녕하세요'일 경우 txt값에 해당 문구를 적으면 됩니다.
    '''
    if txt:
        result=[x for x in driver.find_elements(using_method,css) if x.text==txt]
    else:
        Warning.add_note('''/n txt의 결과값이 입력되지 않았습니다.''')
    return result