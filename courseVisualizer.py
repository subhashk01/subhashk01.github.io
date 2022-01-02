from igraph import *
import plotly.graph_objects as go
from catalogScraper import generateClassesPrereqs

def removeNonCourse(course, classesDict):
    newClassesDict = {}
    for className in classesDict:
        subClasses = []
        for subClass in classesDict[className]:
            checkString = str(course)+'.'
            if subClass[:len(checkString)] == checkString:
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

def generateCleanData(course, courseExceptions):
    classesDict = generateClassesPrereqs(course, courseExceptions)
    classesDict = removeNonCourse(course, classesDict)
    classesDict = removeNoConnections(classesDict)
    return classesDict


def plotCourseGraph(courseNumber, classesDict, showPlot = True):

    v_label = list(classesDict.keys())
    nr_vertices = len(classesDict.keys())


    def buildEdges(classes, classesDict):
        classVertMap = {classes[i]:i for i in range(len(classes))}
        print(classVertMap)
        edgeList = []
        for className in classesDict:
            for parent in classesDict[className]:
                edgeList.append((classVertMap[parent],classVertMap[className]))
        return edgeList

    edges = buildEdges(v_label, classesDict)

    G = Graph()

    G.add_vertices(range(0,nr_vertices))
    G.add_edges(edges)


    lay = G.layout_reingold_tilford(mode="in", root=0)

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=4),
                    hoverinfo='none'
                    ))

    fig.add_trace(go.Scatter(x=Xn,
                    y=Yn,
                    mode='markers',
                    name='bla',
                    marker=dict(symbol='circle-dot',
                                    size=30,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                    text=labels,
                    hoverinfo='text',
                    opacity=0.95
                    ))


    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
        L=len(pos)
        if len(text)!=L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=labels[k], # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2*M-position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations


    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )
    graphTitle = 'Dependency Graph for Course ' + str(courseNumber)

    fig.update_layout(title= graphTitle,
                annotations=make_annotations(position, v_label),
                font_size=12,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(l=40, r=40, b=85, t=100),
                hovermode='closest',
                plot_bgcolor='rgb(248,248,248)'
                )

    fig.write_image("course-"+str(courseNumber)+'-graph.png') 
    if showPlot:
        fig.show()




if __name__ == "__main__" :
    course8exceptions = {'8.01':['8.02', '8.021', '8.022', '8.282'], '8.02':['8.03', '8.033']}
    classesDict = generateCleanData(8, course8exceptions)
    plotCourseGraph(8, classesDict, False)