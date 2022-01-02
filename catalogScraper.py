import requests
from bs4 import BeautifulSoup
import re


'''
Accesses the data from the student catalog for a course number
and returns every course and its direct prereqs
'''
def scraper(course):
    
    URL = "http://student.mit.edu/catalog/m"+str(course)+"a.html"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.text.split('\n')

    classes = []
    prereqs = []
    for i in range(len(results)):
        result = results[i]
        if result[:2]==str(course)+'.':
            classes.append(result)
        if result[:7]=='Prereq:':
            prereqs.append(result)
    return classes, prereqs

classes, prereqs = scraper(8)


'''
Returns a dictionay whos keys are classes and whos 
values are the direct prereq of the key classes. 

classes: a list of courses
prereqs: string of full prereqs to be parsed
exceptions: a dictionary of the form prereq: all classes with that prereq
to add in some prereqs manually if needed
'''
def create_dependencies(classes, prereqs, exceptions = {}):
    anyCourse = re.compile(r'([\d]{1,2}[\.][\d]+)')

    classesPrereqs = {}
    for i in range(len(classes)):
        reqs = anyCourse.findall(prereqs[i])
        miniRes = anyCourse.findall(classes[i])
        if len(miniRes)>0:
            className = miniRes[0]
            classesPrereqs[className] = reqs
    for exception in exceptions.keys():
        for className in exceptions[exception]:
            classesPrereqs[className].append(exception)
    
    return classesPrereqs

course8exceptions = {'8.01':['8.02', '8.021', '8.022'], '8.02':['8.03', '8.033']}

classesPrereqs = create_dependencies(classes,prereqs,course8exceptions)

