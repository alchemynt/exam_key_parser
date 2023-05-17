import sys, json, os

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
        if(a=='#'):
            self.answer = ''
        else:
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

    with open("ans_tmp.txt", 'w') as mfw:
        mfw.writelines(json_string)

    with open('ans_tmp.txt') as mfr:
        new_str = mfr.readline().replace('\\uff21','A').replace('\\uff22','B').replace('\\uff23','C').replace('\\uff24','D')\
                .replace('\\uff03','#').replace('\"}','').replace('{\"ans\": \"','').replace(' ','')
            
    return new_str

def file_cleanup():
    os.remove('ans_tmp.txt')
    if os.path.exists('bak'):
        os.replace(mf_name, 'bak/'+mf_name)
        os.replace(mf_fixed, 'bak/'+mf_fixed)
        os.replace(mf_ans, 'bak/'+mf_ans)
        os.replace(mf_json, 'bak/'+mf_json)
    else:
        os.makedirs('bak')
        os.replace(mf_name, 'bak/'+mf_name)
        os.replace(mf_fixed, 'bak/'+mf_fixed)
        os.replace(mf_ans, 'bak/'+mf_ans)
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
mf_name = name+'.txt'
mf_fixed = name + '_fix.txt'
mf_ans = name+'_ans.txt'
mf_json = name+'.json'
name = name.replace('ex','')

# print(mf_name)

# ***
# *** Clean up original text file so questions and answers are all one line each ***
# ***

# with open(mf_name) as mf:
fArray = []
qArray = []
prev = ''

with open(mf_name) as mfr:
    # init_qtxt = mf.readlines()
    line = mfr.readline()
    while line != '':        
        n_l = mfr.readline()
        if n_l != '':
            split_nl = n_l.split('.',1)
            #while (not split_nl[0].isnumeric()) and (not split_nl[0] in ['A','B','C','D']):
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
        # i = ex_id + str(qnum)
        i = name + str(qnum)
        q = Question(i,q,a,b,c,d)
        qArray.append(q)
        q = mfr.readline()

# ***
# *** Parse answer text file, store in questions
# ***
ans_list=parse_ans(mf_ans)
print(ans_list)
ind = 0
for c in ans_list:
    qArray[ind].set_answer(c)
    print(ind)
    ind += 1

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
json_str += ']'

with open(mf_json, 'w') as mfw:
    mfw.writelines(json_str)
    print('done')

file_cleanup()