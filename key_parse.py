import sys, json, os
import PyPDF2, re

class Question:
    def __init__(self,i,q,a,b,c,d):
        self._id = i
        self.question = q
        self.image = ''
        self.optionA = a
        self.optionB = b
        self.optionC = c
        self.optionD = d
        self.answer = ''
        self.userAnswer = ''
        self.explanation = ''
    
    def set_answer(self, a):
        self.answer = a

    def set_explanation(self, e):
        self.explanation = e

    def set_img(self, i):
        self.image = i

    def __str__(self):
        print_str = self._id + ': ' + self.question + '\nA: ' + self.optionA \
                    + '\nB: ' + self.optionB + '\nC: ' + self.optionC + '\nD: ' + self.optionD \
                    + '\nAnswer: ' + self.answer
        return print_str

class Answer:
    def __init__(self,a):
        self.ans = a

def parse_ans(af):
    a = ''
    new_str = ''
    
    # with open("extst.txt") as f:
    with open(af) as f:
        a = Answer(f.readline())
    json_string = json.dumps(a.__dict__)

    with open("tmpANS.txt", 'w') as mfw:
        mfw.writelines(json_string)

    with open('tmpANS.txt') as mfr:
        new_str = mfr.readline().replace('\\uff21','A').replace('\\uff22','B').replace('\\uff23','C').replace('\\uff24','D')\
                .replace('\\uff03','#').replace('\"}','').replace('{\"ans\": \"','').replace(' ','')
            
    return new_str

def file_cleanup():
    os.remove('tmpANS.txt')
    os.remove('tmpPDF.txt')
    if os.path.exists('bak'):
        os.replace(mf_name, 'bak/'+mf_name)
        os.replace(mf_fixed, 'bak/'+mf_fixed)
        os.replace(mf_ans, 'bak/'+mf_ans)
    else:
        os.makedirs('bak')
        os.replace(mf_name, 'bak/'+mf_name)
        os.replace(mf_fixed, 'bak/'+mf_fixed)
        os.replace(mf_ans, 'bak/'+mf_ans)

    if os.path.exists('json'):
        os.replace(mf_json, 'json/'+mf_json)
    else:
        os.replace(mf_json, 'bak/'+mf_json)


def check_line(nl):
    if nl.isnumeric():
        # print(nl)
        if int(nl) == 0:
            return True
        else:
            return False
    else:
        if nl not in ['A','B','C','D']:
            return True
        else:
            return False
    
name = sys.argv[1]
print('Parsing: ' + name)
mf_name = name+'.txt'
mf_fixed = name + '_fix.txt'
mf_ans = name+'_ans.txt'
mf_json = name+'.json'
mf_pdf = name+'.pdf'
name = name.replace('ex','')

if not os.path.exists(mf_fixed):
        os.mknod(mf_fixed)
if not os.path.exists(mf_json):
        os.mknod(mf_json)
if not os.path.exists('tmpPDF.txt'):
        os.mknod('tmpPDF.txt')

# ***
# *** Clean up original text file so questions and answers are all one line each ***
# ***

fArray = []
qArray = []
prev = ''

with open(mf_name) as mfr:
    line = mfr.readline()
    while line != '':        
        n_l = mfr.readline()
        if n_l != '':
            split_nl = n_l.split('.',1)
            while check_line(split_nl[0]):
                tmp_l = n_l
                line = line + tmp_l.replace('\n', '').replace('\r','')
                n_l = mfr.readline()
                split_nl = n_l.split('.',1)
        if n_l != '':
            fArray.append(line.replace('\n','') + '\n')
        else:
            fArray.append(line)

        line = n_l

with open(mf_fixed, 'w') as mfw:
    mfw.writelines(fArray)

# ***
# *** Open cleaned file, create question objects, store into array
# ***

with open(mf_fixed, 'r') as mfr:
    qnum = 0
    q = mfr.readline()
    while q != '':
        qnum+=1
        # print(q)
        q = q.split('.',1)[1].replace('\n', '').replace('r','')
        a = mfr.readline().split('.',1)[1].replace('\n', '').replace('\r','')
        b = mfr.readline().split('.',1)[1].replace('\n', '').replace('\r','')
        c = mfr.readline().split('.',1)[1].replace('\n', '').replace('\r','')
        d = mfr.readline().split('.',1)[1].replace('\n', '').replace('\r','')
        i = name + str(qnum)
        q = Question(i,q,a,b,c,d)
        qArray.append(q)
        q = mfr.readline()

# ***
# *** Parse answer text file, store in questions
# ***
ans_list=parse_ans(mf_ans)
#print(ans_list)
ind = 0
for c in ans_list:
    qArray[ind].set_answer(c)
    #print(ind)
    ind += 1

# ***
# *** Parse explanations from pdf file, store in questions
# ***
reader = PyPDF2.PdfReader("pdf/" + mf_pdf)
pdf_all = ''

explanations = {}
for p in reader.pages:
    pdf_all += p.extract_text() + ' '

pdf_ol = pdf_all.replace('\r',' ').replace('\n', ' ').replace('  ',' ')

#simple = re.split('( 簡解 )|( 詳解 )', pdf_ol)
# pdf_lines = pdf_ol.replace('-簡解','簡解').replace(' 簡解 ','\n').replace(' 詳解 ','\n')
count = 1
simple = []
pdfl = []
skip = False

s1 = pdf_ol.replace('-簡解','簡解').split(' 簡解 ')
for s in s1:
    s2 = s.split(' 詳解 ',1)
    pdfl.append(s2[0])
    if len(s2) > 1:
        pdfl.append(s2[1])

with open('tmpPDF.txt','w') as mfw:
    for l in pdfl:
        mfw.write(l+'\n')
    # mfw.writelines(pdfl)
    # mfw.write(pdf_ol.replace('-簡解','簡解').replace(' 簡解 ','\n').replace(' 詳解 ','\n'))

with open('tmpPDF.txt') as mfr:
    pdf_lines = mfr.readlines()

for line in pdf_lines:
    # print(str(count) + ': ' + line)
    if count%2 == 0 and '醫學二 第' in line:
        line = line.replace('醫學二 第','\n醫學二 第')
        for l in line.splitlines():
            simple.append(l)
            #print(str(count) + ': ' + l)
        skip = True
        count += 1
    else:
        simple.append(line)
    count += 1
#simple = pdf_ol2.split('\n')
count = 1
qNum = 0

#build dictionary array with question number and simple explanation

#1111a and 1111b use different pdf format than 1112+
if('1111' in name):
    for s in simple:
        #print(str(count)+': '+s)
        if count%2==0:
            explanations[qNum]=s
        else:
            qNumS = re.search("醫學一第\d+", s.replace(' ',''))
            if qNumS:
                qNum = qNumS.group(0).replace('醫學一第','')
            else:
                qNumS = re.search("醫學二第\d+", s.replace(' ',''))
                if qNumS:
                    qNum = qNumS.group(0).replace('醫學二第','')
        count += 1
else:
    for s in simple:
        ####print(str(count)+': '+s)
        if count%2==0:
            explanations[qNum]=s
        else:
            qNumS = re.search("題號\d+", s.replace(' ',''))
            if qNumS:
                qNum = qNumS.group(0).replace('題號','')
            #else:
                #print('error')
                # qNumS = re.search("醫學\d+", s.replace(' ',''))
                # if qNumS:
                #     qNum = qNumS.group(0).replace('醫學','')
        count += 1

for q in qArray:
    qNum = q._id.replace(name,'')
    if qNum in explanations:
        q.set_explanation(explanations[qNum].replace('\n',''))
        #print(qNum + ': ' + q.explanation+ '\n')
    else: print('explanation missing: ' + qNum + '\n')

#print(explanations)

# for q in qArray:
#     print(q)
#     print()

# ***
# *** can't use json.dumps because it doesn't recognize chinese characters well (saves as \u####)
# ***

# json_string = json.dumps([ob.__dict__ for ob in qArray])
# with open('j.txt', 'w') as mfw:
#     mfw.writelines(json_string)

json_str = '[\n'
for q in qArray:
    json_str += ('{\n' + \
                 '"_id": "' + q._id + '",\n'\
                 '"question": "' + q.question + '",\n'\
                 '"image": "' + q.image + '",\n'\
                 '"optionA": "' + q.optionA + '",\n'\
                 '"optionB": "' + q.optionB + '",\n'\
                 '"optionC": "' + q.optionC + '",\n'\
                 '"optionD": "' + q.optionD + '",\n'\
                 '"answer": "' + q.answer + '",\n'\
                 '"userAnswer": "' + q.userAnswer + '",\n'\
                 '"explanation": "' + q.explanation + '",\n'\
                 '},\n'
                 )
    #print(q.explanation)
json_str += ']'

with open(mf_json, 'w') as mfw:
    mfw.writelines(json_str)
    print('done\n')

file_cleanup()