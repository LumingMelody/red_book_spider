import sweetviz as sv
import pandas as pd

rd = pd.read_excel("D:/red_book/red_book_51wom/06_18/小红书06_18_result.xlsx")
df = pd.DataFrame(rd)
my_report = sv.analyze(df)
my_report.show_html()