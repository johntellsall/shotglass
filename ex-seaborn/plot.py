import seaborn.objects as so
import palmerpenguins as pp
import pandas as pd
import matplotlib.pyplot as plt

# read datafrom from csv file
monthly = pd.read_csv('monthly.csv')

# keys from data


penguins = pp.load_penguins()
   
data = {'year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
        'Life_Expectancy': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
       }
  
healthexp = pd.DataFrame(data)
# (
#     so.Plot(
#         penguins, x="bill_length_mm", y="bill_depth_mm",
#         edgecolor="sex", edgewidth="body_mass_g",
#     )
#     .add(so.Dot(color=".8"))
# )
# (
#     so.Plot(healthexp, x="Year", y="Life_Expectancy", color="Country")
#     .add(so.Line())
# )
# plot = (
#     so.Plot(penguins, x="species", y="body_mass_g")
#     .add(so.Dot(pointsize=10), so.Agg())
# )
# plot = (
#     so.Plot(penguins, x="species", y="body_mass_g", color="sex")
#     .add(so.Bar(), so.Agg())
# )
# plot = (
#     so.Plot(penguins, x="species", y="body_mass_g", color="sex")
#     .add(so.Dot(), so.Dodge(), so.Jitter(.3))
# )
plot = (
    so.Plot(healthexp, x="year", y="Life_Expectancy")
    .add(so.Line(marker='o', edgecolor='w'), so.Agg(), linestyle=None)
)
plot.save('plot.png', dpi=220)
# plot.show()
