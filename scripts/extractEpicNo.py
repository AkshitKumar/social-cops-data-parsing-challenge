from bs4 import BeautifulSoup
import re

data = open('output.html','r').read()
soup = BeautifulSoup(data)

epicnos = soup.findAll(text = re.compile("[A-Z]{3}[0-9]{7}"))
up = soup.findAll(text = re.compile("[A-Z]{2}\/[0-9]{2}\/[0-9]{3}\/[0-9]{7}"))

epicnos = epicnos + up

epicNums = []

def processEpicNo(epicnos):
        for epicno in epicnos:
                if 'ANB' in epicno:
                        index = epicno.index('A')
                        epicno = epicno[index:index+10]
                        epicNums.append(str(epicno))
                elif 'GLT' in epicno:
                        index = epicno.index('G')
                        epicno = epicno[index:index+10]
                        epicNums.append(str(epicno))
                elif 'UP' in epicno:
                        index = epicno.index('U')
                        epicno = epicno[index:index+17]
                        epicNums.append(str(epicno))

processEpicNo(epicnos)
epicNumbers = epicNums
print epicNums
