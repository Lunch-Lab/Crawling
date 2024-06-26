import os
import shutil
import functools as fts
import csv

# 파일 압축 후 zip 파일 지우기 -> 압축된 파일명 가져오기 
def unziping(path:str="",file_names:list[str]=[],save_point:str=None,*args,**kwargs)->list[str]:
    for file in file_names:
        total_temp_path=path+"/"+file
        shutil.unpack_archive(total_temp_path,save_point)
        os.remove(total_temp_path)
    return map(lambda x:path+"/"+x,os.listdir(path))

if not os.path.exists("./Data"):
    Warning.add_note("There is not exist : Path : ./Data")

# 압축해제
path="./Data"
unzip=fts.partial(unziping,path=path,file_names=os.listdir(path))

test_ls=list(unzip(save_point="./Data"))

# 불러오기
zip_dict=dict.fromkeys(range(len(test_ls)))


for idx in zip_dict:    
    with open(test_ls[idx],"r",encoding="cp949") as f:
        zip_dict[idx]=f.readlins() #->  각각 딕셔러니 형태로 저장해놓음

# cp949 파싱
def encode_line(text:str):
    return list(map(lambda x:x.replace('"',""),text.split('","')))

# 고정 columne
selected_columns = ['영업상태명', '소재지전체주소', '도로명전체주소', '사업장명', '최종수정시점','데이터갱신일자','업태구분명', '좌표정보(x)', '좌표정보(y)','소재지면적']


# column 순서 유의
def mkline(line:list[str],idxs:list[int],condition_idx:int,condition:str,*ags,**kwargs):
    if line[condition_idx]!=condition:
        return [line[idx] for idx in idxs] 

# 필요한 정보
txt_total=[selected_columns]

# 각 파일마다 처리
for idx in zip_dict:
    test=zip_dict[idx]

    condition_idx=encode_line(test[0]).index("영업상태명")
    column_idx_dic={x:encode_line(test[0]).index(x) for x in selected_columns}
    mkln=fts.partial(mkline,idxs=column_idx_dic.values(),condition_idx=condition_idx,condition="폐업") # 폐업 상태의 가게는 제거

    for txt in test[1:]:
        if mkln(encode_line(txt)):
            txt_total.append(mkln(encode_line(txt)))

# 결과 csv 파일화

with open("test_mk.csv","w") as mkcsv:
    writer=csv.writer(mkcsv)
    writer.writerows(txt_total)
