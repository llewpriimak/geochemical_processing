import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math
import openpyxl
import numpy as np
from ternary_diagram import TernaryDiagram
# plt.rcParams["axes.grid"]  = True

# This script is designed to take data from the JAX-8200 superprobe
# and plot element changes throughout the crystal. **

# Value correction takes oxide weight percents and
# returns 5 values each corresponding to compositions
# Spessartine, Grossular, Almandine, Pyrope, and Fe.
def value_correction(grain_frame,transect):


    Si = 60.09 ; Al = 101.96 ; Mn = 70.938 ; Mg = 40.305 \
        ; Ca = 56.078 ; Na = 61.978 ; Fe = 71.847 ; Ti = 79.88

    #print(grain_frame)
    new_Na = (grain_frame["Na2O"] / Na) ; new_Si = (grain_frame["SiO3"] / Si) * 3
    new_Al = (grain_frame["Al2O3"] / Al) * 3 ; new_Mn = (grain_frame["MnO"] / Mn)
    new_Ca = (grain_frame["CaO"] / Ca) ; new_Fe = (grain_frame["FeO"] / Fe)
    new_Ti = (grain_frame["TiO2"] / Ti) * 2 ; new_Mg = (grain_frame["MgO"] / Mg)

    # Write this part into a data frame/array^
    total_it = new_Na + new_Si + new_Al + new_Mn + new_Ca + new_Fe + new_Ti + new_Mg
    normal_12 = 12/total_it

    new2_Na = new_Na * normal_12 ; new2_Mg = new_Mg * normal_12
    new2_Si = new_Si * normal_12 ; new2_Al = new_Al * normal_12
    new2_Mn = new_Mn * normal_12 ; new2_Ca = new_Ca * normal_12
    new2_Fe = new_Fe * normal_12 ; new2_Ti = new_Ti * normal_12

    pure_Na = new2_Na * 2 ; pure_Si = new2_Si * (1/3)
    pure_Al = new2_Al * (2/3) ; pure_Mn = new2_Mn ; pure_Mg = new2_Mg
    pure_Fe = new2_Fe; pure_Ca = new2_Ca ; pure_Ti = new2_Ti * 0.5

    spess = pure_Mn / (pure_Mn + pure_Mg + pure_Ca + pure_Fe)
    gross = pure_Ca / (pure_Mn + pure_Mg + pure_Ca + pure_Fe)
    alman = pure_Fe / (pure_Mn + pure_Mg + pure_Ca + pure_Fe)
    pyrope = pure_Mg / (pure_Mn + pure_Mg + pure_Ca + pure_Fe)
    andra = pure_Ti / (pure_Mn + pure_Mg + pure_Ca + pure_Fe + pure_Ti)
    iron = pure_Fe / (pure_Fe + pure_Mg)

    spess = merge_frame_sort(spess,transect)
    gross = merge_frame_sort(gross,transect)
    alman = merge_frame_sort(alman,transect)
    pyrope = merge_frame_sort(pyrope,transect)
    iron = merge_frame_sort(iron,transect)
    andra = merge_frame_sort(andra,transect)

    return spess,gross,alman,pyrope,iron,andra

# This function takes X,Y data dand returns an array with
# Distance from rim point
def rim_to_rim(grain_frame):

    x_start = float(grain_frame["X-POS"].values[:1])
    y_start = float(grain_frame["Y-POS"].values[:1])
    new_x = np.abs(grain_frame["X-POS"] - x_start)
    new_y = np.abs(grain_frame["Y-POS"] - y_start)
    dist = np.power(new_x**2+new_y**2,0.5)
    normalized = (dist-min(dist))/(max(dist)-min(dist))
    #print(normalized)
    return normalized

# Plots 4 graphs of desired composition as a function of distance
# through the crystal
def plot_it(spess,gross,alman,pyrope,iron, fig, axs):


    fig.supxlabel("Normalized Distance From Rim to Rim")
    fig.supylabel("Mole Fraction")
    axs[0,0].plot(spess[1],spess[0], marker='o',markeredgecolor = '0') ; axs[0,0].set_title('Spessartine')
    #axs[0,0].set(xlabel = ("Distance From Rim to Rim"), ylabel = ('Amount of Spessartine'))
    axs[0,1].plot(gross[1],gross[0], marker = 'o',markeredgecolor = '0') ; axs[0,1].set_title('Grossular')
    #axs[0,1].set(xlabel = ("Distance From Rim to Rim"), ylabel = ('Amount of Grossular'))
    axs[1,0].plot(pyrope[1],pyrope[0], marker = 'o',markeredgecolor = '0') ; axs[1,0].set_title('Pyrope')
    #axs[1,0].set(xlabel = ("Distance From Rim to Rim"), ylabel = ('Amount of Pyrope'))
    axs[1,1].plot(iron[1],iron[0], marker = 'o',markeredgecolor = '0') ; axs[1,1].set_title('Fe+Fe/Mg')
   # axs[1,1].set(xlabel = ("Distance From Rim to Rim"), ylabel = ('Amount of Fe+Fe/Mg'))

    plt.tight_layout()



###################
###################

#Plotting function called by polynomial_regression()
def poly_plot_it(x,y,a0,a1,a2):


    plt.xlabel('X'); plt.ylabel('Y')
    plt.plot(x, y, 'ro', label='Data points')
    plt.plot(x, a0+(a1*x)+(a2*np.power(x,2)),label='Fitting')
    plt.grid(True)
    plt.legend()
    plt.show()



# Polynomial regression function is good for plotting a polynomial line
# through a set of point. This is good for fitting with respect to curves
# bends in the data trend.
def polynomial_regression(x,y):

    n = len(x)
    A = np.array([[n, np.sum(x), np.sum(x**2)],
                  [np.sum(x),np.sum(x**2),np.sum(x**3)],
                  [np.sum(x**2),np.sum(x**3),np.sum(x**4)]])
    b = np.array([np.sum(y),np.sum(x*y),np.sum((x**2)*y)])

    a0,a1,a2 = np.linalg.solve(A,b)


    # plot_it = int(input('Type 1 for poly_plot, 0 for no plot: '))
    # if plot_it == 1:

    poly_plot_it(x,y,a0,a1,a2)


    return a0,a1,a2



########################
#########################


# This combines two separate data frames and sorts the values in ascending order
# from the transect. Returns the sorted frame
def merge_frame_sort(df1, df2):

    merge_frame = pd.concat([df1, df2], axis=1)
    sorted_frame = merge_frame.sort_values(by = 1)

    return sorted_frame



def main():

    df = pd.read_excel("/Users/llewnosukepriimak/Desktop/Siwaliks Project/EPMA Data/SK_run3.xlsx")

    #print('If you have multiple grains you want to \nsee plotted on the same graph please \nenter the first and last numbers from \nthe SAMPLE column when prompted. \n')
    # num_first = int(input('Please enter the first SAMPLE number: '))
    # num_last = int(input('Please enter the last SAMPLE number: '))
    complete = True
    set_of_grains = []
    while complete is True:
        new_grain = input("Please type the number of the grain you \nwant from the NUMBER column in the excel sheet \nor if you chose all grains type DONE: ")
        if new_grain == "DONE":
            break
        set_of_grains.append(int(new_grain))
    #print(set_of_grains)
    #num = int(input("Please type the number of the grain you \nwant from the NUMBER column in the excel sheet: "))
    fig, axs = plt.subplots(2, 2)
    #fig.suptitle(f'Sample/Grain {title_grain}')
    grain_names = []
    for num in set_of_grains:
        one_grain = df.loc[(df["NUMBER"] == num)]
        transect = rim_to_rim(one_grain)
        spess,gross,alm,pyrope,iron,andra = value_correction(one_grain,transect)
        title_grain = (one_grain["SAMPLE"].head(1).values[:])[0]
        grain_names.append(title_grain)
        plot_it(spess, gross, alm, pyrope, iron,fig,axs)
    #fig.legend(grain_names,loc="center", shadow=True, fancybox=True)
    fig.legend(grain_names,loc = (0.39,0.96), ncol=len(grain_names),shadow=True, fancybox=True)
    plt.tight_layout()
    #polynomial_regression(spess[1],spess[0])
    plt.show()



main()