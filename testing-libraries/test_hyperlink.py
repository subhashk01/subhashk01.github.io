from plotly.offline import plot
import pandas as pd
import plotly.graph_objs as go
import re



# mapbox_access_token = '...'

# Build scattermapbox trace and store URL's in the customdata
# property. The values of this list will be easy to get to in the
# JavaScript callback below

data = [
    go.Scatter(
        x=[1, 2, 3],
        y=[1, 3, 2],
        mode='markers',
        marker=dict(
            size=14
        ),
        name='mapbox 1',
        text=['Montreal'],
        customdata=['https://www.baidu.com', 'http://www.fabricschina.com.cn/', 'https://www.zhihu.com']
    )

]

# Build layout
layout = go.Layout(
    hovermode='closest',
)

# Build Figure
fig = go.Figure(
    data=data,
    layout=layout,
)

# Get HTML representation of plotly.js and this figure
plot_div = plot(fig, output_type='div', include_plotlyjs=True)

print(plot_div)
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
with open('hyperlink_fig.html', 'w') as f:
    f.write(html_str)