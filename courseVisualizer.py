from igraph import *
import plotly.graph_objects as go
from dataCleaning import generateCleanData
import re
from plotly.offline import plot





def plotCourseGraph(courseNumber, classesDict, classMapping, root = 0, sizing = 'large', bubble_color = '#488214'):

    v_label = list(classesDict.keys())
    nr_vertices = len(classesDict.keys())


    def buildEdges(classes, classesDict):
        classVertMap = {classes[i]:i for i in range(len(classes))}
        edgeList = []
        for className in classesDict:
            for parent in classesDict[className]:
                edgeList.append((classVertMap[parent],classVertMap[className]))
        return edgeList

    edges = buildEdges(v_label, classesDict)

    G = Graph()

    G.add_vertices(range(0,nr_vertices))
    G.add_edges(edges)
    
    print(root)
    if isinstance(root,str):
        root = v_label.index(root)
        print(root)

    lay = G.layout_reingold_tilford(mode="in", root=root)

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

    URLs, descs = getURLs_Desc(labels, classMapping)

    fig = go.Figure()


    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=4),
                    hoverinfo='none'
                    ))

    if sizing == 'large':
        bubble_size = 40
        font_size = 10
    elif sizing == 'regular':
        bubble_size = 30
        font_size = 8
    else: #sizing = 'small'
        bubble_size = 17
        font_size = 5

   
    fig.add_trace(go.Scatter(x=Xn,
                    y=Yn,
                    mode='markers',
                    name='bla',
                    marker=dict(symbol='circle-dot',
                                    size=bubble_size,
                                    color=bubble_color,    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=0.5)
                                    ),
                    text=descs,
                    hoverinfo='text',
                    opacity=0.8,
                    customdata = URLs
                    ))


    def make_annotations(pos, text, font_size=font_size, font_color='#FFFFFF'):
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
    graphTitle = 'Prereq Map for Course  ' + str(courseNumber)

    fig.update_layout(title= graphTitle,
                annotations=make_annotations(position, v_label),
                font_size=25,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(l=40, r=40, b=85, t=100),
                hovermode='closest',
                plot_bgcolor='rgb(248,248,248)'
                )

    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    # Get id of html div element that looks like
    # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
    res = re.search('<div id="([^"]*)"', plot_div)
    div_id = res.groups()[0]

    # Build JavaScript callback for handling clicks
    # and opening the URL in the trace's customdata 
    js_callback = """
    <script>
    var plot_element = document.getElementById("{div_id}");
    plot_element.on('plotly_click', function(data){{
        console.log(data);
        var point = data.points[0];
        if (point) {{
            console.log(point.customdata);
            window.open(point.customdata);
        }}
    }})
    </script>
    """.format(div_id=div_id)

    # Build HTML string
    html_str = """
    <html>
    <body>
    {plot_div}
    {js_callback}
    </body>
    </html>
    """.format(plot_div=plot_div, js_callback=js_callback)

    # Write out HTML file
    filename = 'html-output/course-'+str(courseNumber)+'-graph.html'
    with open(filename, 'w') as f:
        f.write(html_str)


def getURLs_Desc(classLabels, classMapping):
    URLs = []
    descs = []
    for label in classLabels:
        desc, URL = classMapping[label]
        URLs.append(URL)
        descs.append(desc)
    return URLs, descs



if __name__ == "__main__" :
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
    course = courses[-1][0]
    sizing = courses[-1][1]
    root = courses[-1][2]
    classesDict, classMapping = generateCleanData(course, courseExceptions[course])
    print(classesDict)
    plotCourseGraph(course, classesDict,classMapping, sizing=sizing, root = root)