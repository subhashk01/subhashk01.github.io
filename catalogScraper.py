import requests
from bs4 import BeautifulSoup
import re


'''
Accesses the data from the student catalog for a course number
and returns every course and its direct prereqs
'''
def scraper(course):
    classes = []
    prereqs = []
    classToUrl = {}
    for letter in ['a', 'b', 'c']:
        URL = "http://student.mit.edu/catalog/m"+str(course)+letter+".html"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.text.split('\n')
        
        for i in range(len(results)):
            result = results[i]
            if result[:2]==str(course)+'.':
                classes.append(result)
                classToUrl[result] = URL
            if result[:7]=='Prereq:':
                prereqs.append(result)
    
    return classes, prereqs, classToUrl

classes, prereqs, classToUrl = scraper(8)



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
    classNumToName = {}
    for i in range(len(classes)):
        reqs = anyCourse.findall(prereqs[i])
        miniRes = anyCourse.findall(classes[i])
        if len(miniRes)>0:
            classNum = miniRes[0]
            classNumToName[classNum] = classes[i]
            classesPrereqs[classNum] = reqs
    for exception in exceptions.keys():
        for classNum in exceptions[exception]:
            classesPrereqs[classNum].append(exception)
    
    return classesPrereqs, classNumToName


'''
Generates dictionary that has keys of courses 
and values that are the dependent courses
'''
def generateClassesPrereqs(course, course_exceptions = {}):
    classes, prereqs, classToUrl = scraper(course)
    classesPrereqs, classMap = create_dependencies(classes,prereqs,course_exceptions)
    totalClassMap = {} #will have mapping from class number to a tuple of course description and link
    for classNum in classesPrereqs:
        classDesc = classMap[classNum]
        classURL = classToUrl[classDesc]+"#"+classNum
        totalClassMap[classNum] = (classDesc, classURL)
    return classesPrereqs, totalClassMap

classesPrereqs, totalClassMap = generateClassesPrereqs(8)





