# libraries
import matplotlib

matplotlib.use('svg')
import matplotlib.pyplot as plt
import pandas as pd
import squarify  # pip install squarify (algorithm for treemap)

# If you have 2 lists
squarify.plot(sizes=[13, 22, 35, 5], label=["group A",
                                            "group B", "group C", "group D"], alpha=.7)
plt.axis('off')
plt.savefig('one.png')

# If you have a data frame?
df = pd.DataFrame({'nb_people': [8, 3, 4, 2], 
	'group': [
                  "group A", "group B", "group C", "group D"]})
squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8)
plt.axis('off')
plt.savefig('two.png')
