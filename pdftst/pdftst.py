import PyPDF2, re

# creating a pdf reader object
reader = PyPDF2.PdfReader('1111a.pdf')

# print the number of pages in pdf file
print(len(reader.pages))
pdf_all = ''

explanations = []
for p in reader.pages:
    text = p.extract_text()
    pdf_all += text

pdf_ol = pdf_all.replace('\r','').replace('\n', '')
with open('pdf_ol.txt', 'w') as w:
    w.write(pdf_ol)

simple = re.split('簡解 | 詳解', pdf_ol)
count = 1

with open('pdf_all.txt', 'w') as mfw:
    for s in simple:
        if count%2==0:
            mfw.write(s + '\n')
        else:
            qNum = re.search("醫學一第\d+", s.replace(' ',''))
            if qNum:
                print(qNum.group(0).replace('醫學一第',''))
        count += 1

    # simple = re.split('簡解 | 詳解', text)
    # explanations.append(simple[1])
    # print(simple[1])

# print the text of the first page
# print(reader.pages[100].extract_text())