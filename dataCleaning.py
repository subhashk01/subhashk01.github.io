
from catalogScraper import generateClassesPrereqs

def removeNonCourse(course, classesDict):
    newClassesDict = {}
    for className in classesDict:
        subClasses = []
        for subClass in classesDict[className]:
            checkString = str(course)+'.'
            if subClass[:len(checkString)] == checkString:
                if subClass=='18.10':
                    print(className,'here')
                subClasses.append(subClass)
        newClassesDict[className] = subClasses
    return newClassesDict

def removeNoConnections(classesDict):
    classConnected = {i:False for i in classesDict.keys()}
    for className in classesDict:
        for parent in classesDict[className]:
            classConnected[className] = True
            classConnected[parent] = True
    newClassesDict = {}
    for className in classConnected:
        if classConnected[className]:
            newClassesDict[className] = classesDict[className]
    return newClassesDict

def generateCleanData(course, courseExceptions = {}):
    classesDict, classMapping = generateClassesPrereqs(course, courseExceptions)
    classesDict = removeNonCourse(course, classesDict)
    classesDict = removeNoConnections(classesDict)
    if '18.0002' in classesDict:
        classesDict.pop('18.0002')
    return classesDict, classMapping





if __name__ == '__main__':
    #classes, prereqs, classToUrl = scraper(6)
    classesDict, totalClassMap = generateCleanData(24)
    print(classesDict)