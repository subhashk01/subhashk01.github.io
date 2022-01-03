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
    if course==24:
        letters = ['b']
    elif course==4:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    else:
        letters = ['a', 'b', 'c']
    for letter in letters:
        URL = "http://student.mit.edu/catalog/m"+str(course)+letter+".html"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.text.split('\n')
        tru = None
        for i in range(len(results)):
            result = results[i]
            course_search = str(course)+'.'
            bad_results = ['18.701-18.702 is more extensive and theoretical than the 18.700-18.703 sequence. Experience with proofs necessary. 18.701 focuses on group theory, geometry, and linear algebra.',
                            '6.S974 Special Subject in Electrical Engineering and Computer Science',
                            '18.821 Project Laboratory in Mathematics',
                            'Prereq: Two mathematics subjects numbered 18.10 or above', '7.014 Introductory Biology', 
                            '7.340: https://biology.mit.edu/undergraduate/current-students/subject-offerings/advanced-undergraduate-seminars/',
                            '7.340: TBA.',
                            '7.341: Lecture: T10-12 (68-150)',
                            '7.342: Lecture: W10-12 (68-150)',
                            '7.343: Lecture: T12-2 (68-150)',
                            '7.344: Lecture: W2-4 (68-150)',
                            '7.340: No textbook information available',
                            '7.341: No textbook information available',
                            '7.342: No textbook information available',
                            '7.343: No textbook information available',
                            '7.344: No textbook information available',
                            '7.345-7.349 Advanced Undergraduate Seminar',
                            '7.345: Lecture: R11-1 (68-180)',
                            '7.346: Lecture: R1-3 (68-180)',
                            '7.347: TBA.',
                            '7.348: TBA.',
                            '7.349: TBA.',
                            '7.345: No textbook information available',
                            '7.346: No textbook information available',
                            '7.347: No textbook information available',
                            '7.348: No textbook information available',
                            '7.349: No textbook information available',
                            '15.840-15.843 Seminar in Marketing',
                            'Prereq: 15.810'
                            ]
            if result in bad_results: #manually taking out this class
                continue
            if result[:len(course_search)]==course_search:
                if tru is None or tru is False:
                    classes.append(result)
                    tru = True
                    classToUrl[result] = URL
                else:
                    print('bad class')
                    print(result)
                    break
            if result[:7]=='Prereq:':
                if tru is True:
                    prereqs.append(result)
                    tru = False
    return classes, prereqs, classToUrl


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
        if '9.16' in reqs:
            reqs.remove('9.16')
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


if __name__ == '__main__':
    #classes, prereqs, classToUrl = scraper(7)
    classesPrereqs, totalClassMap = generateClassesPrereqs(9)
    #print(classesPrereqs)
    print(classesPrereqs)
    






