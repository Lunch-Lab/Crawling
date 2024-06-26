from Requirements import *
from selenium.webdriver import Chrome
from functools import partial,wraps
# 정보수집
def remove_special_characters(text:str):
    ''' 정규표현식을 제거하기 위한 함수입니다.'''
    pattern = r'[^\w\s]|_'
    result = re.sub(pattern, '', text)
    return result

def Fix_driver(driver:Chrome,func:Callable[...,Any],*args,**kwargs):
    '''driver 값을 쉽게 바꿔줄겁니다'''
    params=inspect.signature(func).parameters.keys()
    if "driver" not in params:
        Warning.add_note("driver 객체를 쓰지않는 함수입니다. 확인해보세요")
    else:
        return partial(func,driver=driver,*args,**kwargs)

def craw_info(driver:Chrome,using_method=By.CSS_SELECTOR,css_list:List[Any]=[],**kwargs):
    '''정보 1차 수집 함수'''
    fc_=Fix_driver(driver=driver,func=find_css)
    def check_info(**kwargs):
        if not fc_(**kwargs):
            return list()
        elif isinstance(fc_(**kwargs),list):
            return list(map(lambda x:x.text,fc_(**kwargs)))
        else:
            return fc_(**kwargs).text
            
        
    return OrderedDict(enumerate(map(lambda x:check_info(**x),css_list)))    

def Dictionary(fun:Callable[...,Any]):
    '''차후 정보 저장을 위해 만들어짐'''
    @wraps(fun)
    def wrapper(*args,**kwargs):
        if isinstance(fun(*args,**kwargs),list):
            value_output=fun(*args,**kwargs)
        else:
            value_output=[fun(*args,**kwargs)]
        key_output=fun.__name__.split("2")
        return OrderedDict(zip(key_output,value_output))
    return wrapper

# nan 값 처리
nan_make=lambda x: x if x else "정보없음"

@Dictionary
def place_name(input_value:str="정보없음",*args,**kwargs):
    '''음식점 이름'''
    return input_value if input_value else place_name()

@Dictionary
def place_cate2place_loc(input_value:List[Any]=["정보없음","정보없음"]):
    '''음식점 카테고리 및 위치'''
    return list(map(nan_make,input_value)) if any(input_value) else place_cate2place_loc()

@Dictionary
def use_method2wait_time2purpose2visit_with(input_value:List[Any]=["정보없음"]*4):
    '''디테일'''
    standard=["이용방법","대기 시간","목적","동행"]
    def get_value(input_value:List[Any],y:str=""): 
        if input_value:
            temp=[x.replace(y,"").strip() for x in input_value if y in x]
            
            return nan_make(temp[0]) if temp else nan_make("")
        else:
            return nan_make("")
        
    result=OrderedDict({y:get_value(input_value,y) for y in standard})
    return list(result.values())
    
@Dictionary
def place_review(input_value:str="정보없음"):
    standard=remove_special_characters(input_value) if input_value else nan_make("")
    return standard

@Dictionary
def place_tag(input_value:List[Any]):
    #return ",".join(list(map(lambda x:"'"+x+"'",input_value))) if input_value else nan_make("")
    return str(input_value).replace('[', '').replace(']', '') if input_value else nan_make("")

@Dictionary
def visit_date2visit_count2visit_weekday(input_value):
     if len(input_value)>=2:
        if '별점' in input_value[0]:
            input_value=input_value[1:]
        else:
           pass

        visit_date_text,visit_count_text = input_value[0],input_value[1]

        visit_date=visit_date_text.split('년')[1].strip()
        visit_weekday =  visit_date[-3:]
        visit_date=visit_date[:-3].strip()
        visit_count = visit_count_text.split('번째 방문')[0].strip()

        return [visit_date,visit_count,visit_weekday]
     else:
         return [nan_make("")]*3
     
get_id=lambda x:(x.get_attribute("id"),x)
