import requests
from bs4 import BeautifulSoup
import urllib
import sys
from openpyxl import load_workbook

epicnum = sys.argv[1]
k = sys.argv[2]

url = 'http://164.100.180.4/searchengine/SearchEngineEnglish.aspx'
headers = {
        'Accept':'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip,deflate',
		'Accept-Language': 'en-US,en;q=0.8',
		'Origin': 'http://164.100.180.4',
		'Host':'164.100.180.4',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'http://164.100.180.4/searchengine/SearchEngineEnglish.aspx',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
}
form = {
        '__EVENTVALIDATION':'',
		'__VIEWSTATE':'',
		'__VIEWSTATEGENERATOR':'',
		'ddlDistricts':'' ,
        'RdlSearch':'',
        '__EVENTTARGET':'',
}


wb = load_workbook(filename = 'voterData.xlsx')
sheet = wb['Social']

def form_hidden_params(soup):
        viewState = soup.select('#__VIEWSTATE')[0]['value']
        eventValidation = soup.select('#__EVENTVALIDATION')[0]['value']
        viewStateGenerator = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
        return [viewState,eventValidation,viewStateGenerator]

def search(epicnum):
        session = requests.session()
        resp = session.get(url,headers=headers)
        soup = BeautifulSoup(resp.text,'lxml')

        form['__VIEWSTATE'] , form['__EVENTVALIDATION'] , form['__VIEWSTATEGENERATOR'] = form_hidden_params(soup)
        form['ddlDistricts'] = '--Select--'
        form['RdlSearch'] = '0'

        resp = session.post(url,urllib.urlencode(form),headers=headers)
        soup = BeautifulSoup(resp.text,'lxml')

        form['__VIEWSTATE'] , form['__EVENTVALIDATION'] , form['__VIEWSTATEGENERATOR'] = form_hidden_params(soup)
        form['__EVENTTARGET'] = 'ddlDistricts'
        form['ddlDistricts'] = '67'

        resp = session.post(url,form,headers=headers)
        soup = BeautifulSoup(resp.text,'lxml')

        form['__VIEWSTATE'] , form['__EVENTVALIDATION'] , form['__VIEWSTATEGENERATOR'] = form_hidden_params(soup)
        form['txtEPICNo'] = epicnum
        form['Button1'] = 'Search'
        resp = session.post(url, form, headers= headers)

        if 'No Match Found' in resp.text:
    		return processData('No Match Found')
    	else:
    		return processData(resp.text.encode('utf-8'))

        session.close()

def processData(respData):
        if 'No Match Found' in respData:
                details = []
                details.append('NOT FOUND')
                details.append(epicNum)
        else:
                soup = BeautifulSoup(respData,'lxml')
                table = soup.find('table',{'id':'gvSearchResult'})
                rows = table.findChildren('tr')
                details = []
                alphas = ['Z','Y','X','W','A','B','C','D','E','F','G','H']
                for row in rows:
                        cells = row.findChildren('td')
                        i = 0
                        for cell,alpha in zip(cells,alphas):
                                if(i<4):
                                        i = i + 1
                                        continue
                                try:
                                        sheet[alpha + k] = cell.string
                                except:
                                        print "Not Found Error"
                        i = i + 1

search(epicnum)
wb.save('voterData.xlsx')
