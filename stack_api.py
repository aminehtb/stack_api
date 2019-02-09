import urllib.request
import xlsxwriter
from stackapi import StackAPI 
from bs4 import BeautifulSoup


def get_answer(url):
    content = urllib.request.urlopen(url)
    soup = BeautifulSoup(content,features='lxml')
    try:
        answer = soup.find_all('div',attrs={'class':'accepted-answer'})
        accepted_content = answer[0].contents[1].find('div',attrs = {'class':'post-text'})
        return accepted_content.text
    except Exception :
        return 'not answered'

if __name__ == "__main__":
    tag = 'python'
    workbook = xlsxwriter.Workbook(tag+'.xlsx')
    worksheet = workbook.add_worksheet()


    site = StackAPI('stackoverflow')
    questions = site.fetch('questions',tagged = tag)
    for i,item in enumerate(questions['items']):
        worksheet.write(i,0,item['title'])
        worksheet.write(i,1,get_answer(item['link']).strip())

    workbook.close()