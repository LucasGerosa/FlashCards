from lxml import html
import os.path
import requests
from flashcard import writeDic
def finder():
    page = requests.get('https://www.learn-japanese-adventure.com/hiragana-chart.html')
    tree = html.fromstring(page.content)
    elems = tree.xpath('//td/text()')
    letrasDic = {}
    key = ''
    for elem in elems:
      if len(elem) < 4 and elem != '　':
        if key == '':
            key = elem
        else:
            letrasDic[key] = [elem,10]
            key = ''
    if os.path.isfile('hiragana.txt') == True:
        print('this file already exists. Do you want to overwrite it?')
        if input() == 'yes':
            writeDic(letrasDic,'hiragana.txt')
        else:
            print('The file is not being overwritten.')


    
finder()