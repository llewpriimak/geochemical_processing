import matplotlib
import matplotlib.pyplot as plt
import math
import openpyxl
import numpy as np
from ternary_diagram import TernaryDiagram


def main_plot():

    # The background color is sometimes transparent in jupyter notebooks, so set facecolor 'white'.
    fig, ax = plt.subplots(facecolor="w")

    # You can set `ax` to select which axes to draw. If not, the current axes will be used.
    td = TernaryDiagram(["Al + Sp", "Gr+An", "Py"], ax=ax)

    # scatter
    td.scatter(vector=[[1, 1, 2], [1, 2, 3]], z=[0, 1])
    # You can set some options in `plt.scatter` like `marker`, `c` etc.
    td.scatter(vector=[[2, 1, 6], [3, 2, 1]], marker="s", c="#022c5e", s=30)

    # line plot
    # You can set some options in `plt.plot` like `lw`, `c`, and so on.
    td.plot([[1, 1, 1], [1, 2, 3]], color="black")

    # save figure
    fig.savefig("figure1.png", dpi=144)

main_plot()

