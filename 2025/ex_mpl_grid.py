import matplotlib.pyplot as plt
import numpy as np

# import matplotlib
# import matplotlib as mpl


vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
              "potato", "wheat", "barley"]
farmers = ["Joe", "Bros.", "Smith",
           "Agrifun", "Organic", "Ltd.", "Corp."]

harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])

title = "BEER"

def grid():
    fig, ax = plt.subplots()
    _im = ax.imshow(harvest)

    xt_style = dict(rotation=45, ha="right", rotation_mode="anchor")

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(range(len(farmers)), labels=farmers, **xt_style)
    ax.set_yticks(range(len(vegetables)), labels=vegetables)

    t_style = dict(ha="center", va="center", color="white", fontweight="bold")

    # Loop over data dimensions and create text annotations.
    for i in range(len(vegetables)):
        for j in range(len(farmers)):
            text = ax.text(j, i, harvest[i, j], **t_style)

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig("beer.png")
    print('DING')