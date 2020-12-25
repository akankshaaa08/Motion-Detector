from motiondetect import df
from bokeh.plotting import show , output_file , figure
from bokeh.models import HoverTool , ColumnDataSource

df["Start_S"]=df["START"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_E"]=df["END"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

f=figure(x_axis_type="datetime",height=300,width=700,title="Motion Detector")
f.yaxis.minor_tick_line_color = None


f.yaxis[0].ticker.desired_num_ticks=1

hover = HoverTool(tooltips=[("Start  ","@Start_S") , ("End  ", "@End_E")])
f.add_tools(hover)

f.quad(left="START", right="END", bottom=0 , top=1 , color='red' , source=cds)

output_file("Motion-Detect-Plot.html")
show(f)