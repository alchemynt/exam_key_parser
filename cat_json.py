import os 

if not os.path.exists('json_cat.json'):
    os.mknod('json_cat.json')

str_json = ''    
# with open('json_cat.json', 'w') as mfw:
if os.path.exists('json/fix'):
    for f in os.listdir('json/fix'):
        with open('json/fix/' + f) as mfr:
            for line in mfr:
                str_json += (line)

str_json = str_json.replace('\n][','').replace(',\n]','\n]')
with open('json_cat.json', 'w') as mfw:
    mfw.write(str_json)