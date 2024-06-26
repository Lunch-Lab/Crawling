import json

def json_value_load(file_path:str="input_condition.json",file_id:int=0,id:int=0,*args,**kwargss):
    with open(file_path,"r") as f:
        json_lines=[json.loads(line) for line in f if (file_id in json.loads(line)["file_id"])&(json.loads(line)["id"]==id)]
    return json_lines[0]["value"]
