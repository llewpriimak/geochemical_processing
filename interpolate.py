import numpy as np
import pandas as pd

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


    return spess,gross,alman,pyrope,iron,andra


# This function takes X,Y data and returns an array with
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


# This combines two separate data frames and sorts the values in ascending order
# from the transect. Returns the sorted frame
def merge_frame_sort(df1, df2):

    merge_frame = pd.concat([df1, df2], axis=1)
    sorted_frame = merge_frame.sort_values(by = 1)

    return sorted_frame


def main():

    path = input('Gimme the file name: ')
    df = pd.read_excel(f"/Users/llewnosukepriimak/Desktop/Siwaliks Project/core_data/{path}/{path}.xlsx")

    # complete = True
    # set_of_grains = []
    # while complete is True:
    #     new_grain = input("Please type the number of the grain you \nwant from the NUMBER column in the excel sheet \nor if you chose all grains type DONE: ")
    #     if new_grain == "DONE":
    #         break
    #     set_of_grains.append(int(new_grain))
    # grain_names = []
    # for num in set_of_grains:
    one_grain = df
    transect = rim_to_rim(one_grain)
    spess,gross,alm,pyrope,iron,andra = value_correction(one_grain,transect)
    title_grain = (one_grain["SAMPLE"].head(1).values[:])[0]
    #grain_names.append(title_grain)

    super_frame = pd.concat([alm,pyrope,spess,gross], axis = 1)
    super_frame.columns = ['Xalm','Xprp','Xsps','Xgross']

    #ADD LINE TO CHOOSE WHAT NUMBER OF LINES TO ADD
    ###FROM CHATGPT
    # Create a DataFrame with NaN values
    nan_rows = pd.DataFrame(np.nan, index=np.arange(len(super_frame) * 3), columns=super_frame.columns)
    # Fill every third row with the values from the original DataFrame
    nan_rows.iloc[::3] = super_frame.values

    ###

    filled_frame = nan_rows.interpolate()
    filled_frame = filled_frame.iloc[:-2]  #THIS LINE WILL ALSO BE AFFECTED BY NUMBER OF POINTS TO ADD
    filled_frame = filled_frame.astype(float).round(4)
    print(filled_frame)
    split_point = filled_frame['Xsps'].max()
    path1 = filled_frame.iloc[:filled_frame['Xsps'].idxmax()+1,:]
    path2 = filled_frame.iloc[filled_frame['Xsps'].idxmax():,:]
    path1 = path1.sort_values(by='Xsps',ascending = False)
    path1.insert(0,'n',range(1,1+len(path1)))
    path2.insert(0, 'n', range(1, 1 + len(path2)))
    print(path1)
    print(path2)
    filled_frame.to_excel(f'/Users/llewnosukepriimak/Desktop/Siwaliks Project/core_data/{path}/{path}_interpolate.xlsx', index=False)

    with pd.ExcelWriter(f"/Users/llewnosukepriimak/Desktop/Siwaliks Project/core_data/{path}/{path}_interpolate.xlsx", mode="a", engine="openpyxl") as writer:
        path1.to_excel(writer, sheet_name="Path1", index=False)
        path2.to_excel(writer, sheet_name="Path2", index=False)
    #filled_frame.to_excel(f'/Users/llewnosukepriimak/Desktop/Siwaliks Project/core_data/{path}/{path}_interpolate.xlsx', index=False)

main()