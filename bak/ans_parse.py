import json 

class Answer:
    def __init__(self,a):
        self.ans = a

with open("extst.txt") as f:
    a = Answer(f.readline())

json_string = json.dumps(a.__dict__)
with open('j.txt', 'w') as mfw:
    mfw.writelines(json_string)

new_str = ''
with open('j.txt') as mfr:
    new_str = mfr.readline().replace('\\uff21','A').replace('\\uff22','B').replace('\\uff23','C').replace('\\uff24','D')\
                .replace('\\uff03','#').replace('\"}','').replace('{\"ans\": \"','').replace(' ','')
print(new_str)