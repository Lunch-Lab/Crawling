import json
def writejs(file_path:str="",info:str="",distinct:str="",value:dict={}):
    line={
        "info":info,
        "value":value,
        "distinct":distinct
    }
    with open(file_path,"a",encoding="utf-8") as f:
        jline=json.dumps(line,ensure_ascii=False)
        f.write(jline+"\n")
        #f.writelines(["\n"+"{"+f'"info":"{info}","value":{value},"distinct":"{distinct}"'+"}"])
