import numpy as np
import skfuzzy as fuzz
import pandas as pd
import tkinter as gui



from tkinter import *
from tkinter import Menu
from skfuzzy import control as ctrl
from tkinter import filedialog
from pandastable import Table
from tkintertable import TableCanvas
from tkinter import messagebox as msg




B = pd.DataFrame()

s = None


ATTENDANCE = 'Attendance'
PERFORMANCE = 'Performance'
INTERNAL_MARKS = 'Internal_Marks'
EXTERNAL_MARKS = 'External_Marks'
POOR = 'Poor'
AVERAGE = 'Average'
GOOD = 'Good'
V_GOOD = 'V.Good'
EXCELLENT = 'Excellent'
low_parameter = [0, 0, 40, 50]
average_parameter = [30, 40, 50, 60]
good_parameter = [40, 50, 60, 70]
v_good_parameter = [50, 60, 70, 80]
excellent_parameter = [65, 80, 100, 100]




# Main program code



# Gui code
window = gui.Tk()
width= window.winfo_screenwidth()
height= window.winfo_screenheight()
window.geometry("%dx%d" % (width,height))
window.title("Student Performance analysis")
window['background']='#97C1EA'

file_display_frame = LabelFrame(window,text="Student data")
file_display_frame.pack(fill="both", side=LEFT, padx=5)
file_display_frame.place(bordermode=INSIDE,height=650, width=500)


# creating menu bar

menuBar = Menu(window)
window.config(menu=menuBar)

def importstudentdata():
    global B
    global s
    filename = filedialog.askopenfilename(initialdir="/", title="Select a student data file",
                                          filetypes=(("Excel file", "*.xlsx"), ("all files", "*.*")))

    s = filename
    B = pd.read_excel(s, sheet_name=0, header=0, index_col=False, keep_default_na=True)

    if (len(B) == 0):
        msg.showinfo('No records ', 'No records found')
    else:
        pass

    table = Table(file_display_frame, dataframe=B, read_only= True)

    table.show()


    print(B)
    return B

#file Menu
fileMenu = Menu(menuBar,tearoff=0)
path = fileMenu.add_command(label="Import Student data", command=importstudentdata)


print(path)
# crating data frame form the imported file



fileMenu.add_separator()
menuBar.add_cascade(label="File",menu=fileMenu)

# compute fuzzy code

def compute_fuzzy(attend, intr_mark, extn_mark):
    intrn_marks = ctrl.Antecedent(np.arange(0, 105, 5), INTERNAL_MARKS)
    attendance = ctrl.Antecedent(np.arange(0, 105, 5), ATTENDANCE)
    extrn_marks = ctrl.Antecedent(np.arange(0, 105, 5), EXTERNAL_MARKS)
    performance = ctrl.Consequent(np.arange(0, 105, 5), PERFORMANCE)

    intrn_marks[POOR] = fuzz.trapmf(intrn_marks.universe, low_parameter)
    intrn_marks[AVERAGE] = fuzz.trapmf(intrn_marks.universe, average_parameter)
    intrn_marks[GOOD] = fuzz.trapmf(intrn_marks.universe, good_parameter)
    intrn_marks[V_GOOD] = fuzz.trapmf(intrn_marks.universe, v_good_parameter)
    intrn_marks[EXCELLENT] = fuzz.trapmf(intrn_marks.universe, excellent_parameter)

    attendance[POOR] = fuzz.trapmf(attendance.universe, [0, 0, 45, 55])
    attendance[AVERAGE] = fuzz.trapmf(attendance.universe, [35, 45, 55, 65])
    attendance[GOOD] = fuzz.trapmf(attendance.universe, [45, 55, 65, 75])
    attendance[V_GOOD] = fuzz.trapmf(attendance.universe, [55, 65, 75, 85])
    attendance[EXCELLENT] = fuzz.trapmf(attendance.universe, [65, 75, 100, 100])

    extrn_marks[POOR] = fuzz.trapmf(extrn_marks.universe, low_parameter)
    extrn_marks[AVERAGE] = fuzz.trapmf(extrn_marks.universe, average_parameter)
    extrn_marks[GOOD] = fuzz.trapmf(extrn_marks.universe, good_parameter)
    extrn_marks[V_GOOD] = fuzz.trapmf(extrn_marks.universe, v_good_parameter)
    extrn_marks[EXCELLENT] = fuzz.trapmf(extrn_marks.universe, excellent_parameter)

    performance[POOR] = fuzz.trapmf(performance.universe, low_parameter)
    performance[AVERAGE] = fuzz.trapmf(performance.universe, average_parameter)
    performance[GOOD] = fuzz.trapmf(performance.universe, good_parameter)
    performance[V_GOOD] = fuzz.trapmf(performance.universe, v_good_parameter)
    performance[EXCELLENT] = fuzz.trapmf(performance.universe, excellent_parameter)

    rule1 = ctrl.Rule(attendance[POOR] & extrn_marks[POOR] & intrn_marks[POOR], performance[POOR])
    rule2 = ctrl.Rule(attendance[POOR] & extrn_marks[AVERAGE] & intrn_marks[POOR], performance[POOR])
    rule3 = ctrl.Rule(attendance[POOR] & extrn_marks[GOOD] & intrn_marks[POOR], performance[AVERAGE])
    rule4 = ctrl.Rule(attendance[POOR] & extrn_marks[V_GOOD] & intrn_marks[POOR], performance[AVERAGE])
    rule5 = ctrl.Rule(attendance[POOR] & extrn_marks[GOOD] & intrn_marks[V_GOOD], performance[GOOD])
    rule6 = ctrl.Rule(attendance[POOR] & extrn_marks[POOR] & intrn_marks[AVERAGE], performance[POOR])
    rule7 = ctrl.Rule(attendance[POOR] & extrn_marks[AVERAGE] & intrn_marks[AVERAGE], performance[AVERAGE])
    rule8 = ctrl.Rule(attendance[POOR] & extrn_marks[GOOD] & intrn_marks[AVERAGE], performance[AVERAGE])
    rule9 = ctrl.Rule((attendance[POOR] & extrn_marks[GOOD] & intrn_marks[GOOD]), performance[GOOD])
    rule10 = ctrl.Rule(attendance[POOR] & extrn_marks[EXCELLENT] & intrn_marks[GOOD], performance[V_GOOD])
    rule11 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[AVERAGE] & intrn_marks[GOOD], performance[AVERAGE])
    rule12 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[GOOD] & intrn_marks[GOOD], performance[GOOD])
    rule13 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[V_GOOD] & intrn_marks[GOOD], performance[GOOD])
    rule14 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[V_GOOD] & intrn_marks[V_GOOD], performance[V_GOOD])
    rule15 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[AVERAGE] & intrn_marks[EXCELLENT], performance[GOOD])
    rule16 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[AVERAGE] & intrn_marks[AVERAGE], performance[AVERAGE])
    rule17 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[POOR] & intrn_marks[POOR], performance[POOR])
    rule18 = ctrl.Rule(attendance[AVERAGE] & extrn_marks[POOR] & intrn_marks[GOOD], performance[AVERAGE])
    rule19 = ctrl.Rule(attendance[GOOD] & extrn_marks[AVERAGE] & intrn_marks[AVERAGE], performance[AVERAGE])
    rule20 = ctrl.Rule(attendance[GOOD] & extrn_marks[EXCELLENT] & intrn_marks[EXCELLENT], performance[V_GOOD])
    rule21 = ctrl.Rule(attendance[GOOD] & extrn_marks[GOOD] & intrn_marks[AVERAGE], performance[GOOD])
    rule22 = ctrl.Rule(attendance[GOOD] & extrn_marks[POOR] & intrn_marks[POOR], performance[POOR])
    rule23 = ctrl.Rule(attendance[V_GOOD] & extrn_marks[EXCELLENT] & intrn_marks[V_GOOD], performance[V_GOOD])
    rule24 = ctrl.Rule(attendance[V_GOOD] & extrn_marks[V_GOOD] & intrn_marks[V_GOOD], performance[V_GOOD])
    rule25 = ctrl.Rule(attendance[V_GOOD] & extrn_marks[POOR] & intrn_marks[POOR], performance[POOR])
    rule26 = ctrl.Rule(attendance[V_GOOD] & extrn_marks[GOOD] & intrn_marks[V_GOOD], performance[V_GOOD])
    rule27 = ctrl.Rule(attendance[V_GOOD] & extrn_marks[EXCELLENT] & intrn_marks[EXCELLENT], performance[EXCELLENT])
    rule28 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[EXCELLENT] & intrn_marks[V_GOOD], performance[V_GOOD])
    rule29 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[AVERAGE] & intrn_marks[AVERAGE], performance[V_GOOD])
    rule30 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[AVERAGE] & intrn_marks[V_GOOD], performance[GOOD])
    rule31 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[AVERAGE] & intrn_marks[GOOD], performance[GOOD])
    rule32 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[POOR] & intrn_marks[POOR], performance[POOR])
    rule33 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[AVERAGE] & intrn_marks[POOR], performance[AVERAGE])
    rule34 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[POOR] & intrn_marks[AVERAGE], performance[POOR])
    rule35 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[GOOD] & intrn_marks[POOR], performance[GOOD])
    rule36 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[POOR] & intrn_marks[GOOD], performance[AVERAGE])
    rule37 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[V_GOOD] & intrn_marks[POOR], performance[V_GOOD])
    rule38 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[POOR] & intrn_marks[V_GOOD], performance[AVERAGE])
    rule39 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[POOR] & intrn_marks[EXCELLENT], performance[GOOD])
    rule40 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[AVERAGE] & intrn_marks[EXCELLENT], performance[V_GOOD])
    rule41 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[GOOD] & intrn_marks[EXCELLENT], performance[V_GOOD])
    rule42 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[V_GOOD] & intrn_marks[EXCELLENT], performance[V_GOOD])
    rule43 = ctrl.Rule(attendance[EXCELLENT] & extrn_marks[EXCELLENT] & intrn_marks[EXCELLENT], performance[EXCELLENT])


    rule_list = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14,
                 rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27,
                 rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40,
                 rule41, rule42, rule43]

    performance_ctrl = ctrl.ControlSystem(rule_list)
    perf_analysis = ctrl.ControlSystemSimulation(performance_ctrl)

    perf_analysis.input[ATTENDANCE] = attend
    perf_analysis.input[EXTERNAL_MARKS] = extn_mark
    perf_analysis.input[INTERNAL_MARKS] = intr_mark

    perf_analysis.compute()
    #return performance.view(sim=perf_analysis)
    return str(perf_analysis.output[PERFORMANCE])



# compute performance
def compute_performance():

    if (len(B) == 0):
        msg.showinfo('No record ', 'Import student data')
    else:
        performance_result = B[["Attendence", "Internal Marks", "External Marks"]].apply(lambda x: compute_fuzzy(*x),axis=1)
        result_data_frame = pd.DataFrame(performance_result)

        #final_result = pd.concat([B, result_data_frame], ignore_index=True)
        #final_result.to_excel(s, index=True,index_label="output")

        final_result = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
        result_data_frame.to_excel(final_result,sheet_name='output')
        final_result.save()
        r = pd.read_excel('output.xlsx', sheet_name=0, header=0, index_col=False, keep_default_na=True)
        table = Table(file_display_frame, dataframe=r, read_only=True)
        table.show()



        print(result_data_frame)


# Buttons
b = gui.Button(window,text="compute performance", command=compute_performance)
b.pack()



window.mainloop()


# end of Gui code



# end of Main program code



