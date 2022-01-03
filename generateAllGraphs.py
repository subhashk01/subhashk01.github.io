from courseVisualizer import plotCourseGraph
from dataCleaning import generateCleanData

def generateAllGraphs():
    courseExceptions = {i:{} for i in range(1,25)}
    courseExceptions[8] = {'8.01':['8.02', '8.021', '8.022', '8.282', '8.223'], '8.02':['8.03', '8.033']}
    courseExceptions[18] = {'18.01':['18.02', '18.022', '18.062', '18.095'],
                            '18.02': ['18.03', '18.032','18.04', '18.05', '18.06', '18.061', '18.075', '18.0751',
                                    '18.085', '18.0851', '18.086', '18.0861', '18.100','18.1001', '18.1002', '18.211','18.300',
                                    '18.330', '18.352']}
    courseExceptions[5] = {'5.111':['5.12', '5.24', '5.301', '5.351']}
    courseExceptions[7] = {'7.012':['7.03', '7.05', '7.08']}
    courses = [(1, 'large', 0), (2, 'small', 0), (4,'regular', 0), (5, 'large', '5.111'), (6, 'small', 0),
                (7, 'large', '7.012'), (8, 'large', 0), (9, 'large', 0), (10, 'regular', '10.10'), (11, 'large', 0),
                (12, 'regular', 0), (14, 'small', '14.01'), (15, 'small', 0), (16, 'large', 0), (17, 'large', 0),
                (18, 'small', 0), (20, 'large', 0), (22, 'large', 0), (24, 'large', 0)]
    colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', 
            '#16a085', '#27ae60', '#2980b9', '#8e44ad','#2c3e50',
            '#f1c40f', '#e67e22', '#e74c3c', '#95a5a6', '#f39c12', 
            '#7f8c8d', '#d35400', '#c0392b', '#d63031']
    for i in range(len(courses)):
        course = courses[i][0]
        sizing = courses[i][1]
        root = courses[i][2]
        classesDict, classMapping = generateCleanData(course, courseExceptions[course])
        plotCourseGraph(course, classesDict,classMapping, sizing=sizing, root = root, bubble_color=colors[i])



if __name__ == '__main__':
    generateAllGraphs()
