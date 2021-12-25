import requests
from bs4 import BeautifulSoup
import re

URL = "http://student.mit.edu/catalog/m8a.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.text.split('\n')
#print(results[30:60])
classes = []
prereqs = []
for i in range(len(results)):
    result = results[i]
    if result[:2]=='8.':
        classes.append(result)
    if result[:7]=='Prereq:':
        prereqs.append(result)

anyCourse = re.compile(r'[\d]{1,2}[\.][\d]+')
print(anyCourse.findall('18.03 drummers, 8.07 beatles, 29, 123'))
classesPrereqs = {}
for i in range(len(classes)):
    reqs = anyCourse.findall(prereqs[i])
    miniRes = anyCourse.findall(classes[i])
    if len(miniRes)>0:
        className = miniRes[0]
        classesPrereqs[className] = reqs
    else:
        print(miniRes)
print(classesPrereqs)


'''
job_elements = soup.find_all('a')


results = soup.findAll("div", 'contentleft')
newResults = [result.text for result in results]
print(newResults)
'''