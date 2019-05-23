import requests
from bs4 import BeautifulSoup

links = []
with open('links.txt', 'r') as linksFile:
    for link in linksFile:
        links.append(link)
    linksFile.close()

total = len(links)
current_ = 1

file = open('rokomarioutput.txt', 'a', encoding='utf-8')

def clean(uncleaned_string):
    s = uncleaned_string
    s = s[4:-5]
    return s

def deeper_clean(uncleaned_string):
    s = uncleaned_string
    s = s[s.find('>')+1:]
    s = s[s.find('>')+1:]
    if s:
        while s[0] == ' ' or s[0] == '\n':
            s = s[1:]
    s = s[:s.find('\n')]
    return s

for link in links:
    print('Processing book ' + str(current_) + 'of ' + str(total))
    response = requests.get(link)
    soup = BeautifulSoup(response.text, features='lxml')
    div = soup.find('div', {'id' : 'book-additional-specification'})
    table = div.find('table')

    uncleaned_data = []
    for line in table.findAll('tr'):
        for line2 in line.findAll('td'):
            uncleaned_data.append(str(line2))
            
    datas = []
    for i in range(16):
        if i == 3 or i == 5:
            datas.append(deeper_clean(uncleaned_data[i]))
            #datas.append('balchal')
        else:
            datas.append(clean(uncleaned_data[i]))
    for i in range(8):
        i = 2*i + 1
        data = datas[i]
        data = data + ', '
        file.write(data)
    file.write('\n')
    current_ += 1

file.close()
