import matplotlib.pyplot as plt
from pywaffle import Waffle

PlotFile = f'{__file__.split(".")[0]}.png'

def main():
    fig = plt.figure(
        FigureClass=Waffle,
        rows=5,
        columns=10,  # Either rows or columns could be omitted
        values=[30, 16, 4]  # Pass a list of integers to values
    )
    fig.savefig(PlotFile, bbox_inches="tight")
    print(f"Plot saved to {PlotFile}")


if __name__ == "__main__":
    main()
