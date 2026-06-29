######################################################################################################################################
#
#   SCRIPT CODE: EVA-02
#
#   SCRIPT TITLE: Tomo Plan Comparison
#
#   VERSION: 0.0
#
#   INTERPRETER: IP
#
######################################################################################################################################

from raystation import *
import sys, System, datetime
import csv
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Retrieve the path to RayStation.exe (This will only work if the script is run from within RayStation)
script_path = System.IO.Path.GetDirectoryName(sys.argv[0])
path = script_path.rsplit('\\',1)[0]
sys.path.append(path)

print(os.getcwd())
os.chdir(r'\\CLIENT\S$')
print(os.getcwd())

class basic_form():

    outputs= {}
    win_list = []

    def __init__(self,title, window = tk.Tk()):

        # initialise variables
        self.window = window
        self.win_title = title
        self.col_count = 0
        self.row_count = 0

        # create logo and set in titlebar
        self.logo = tk.PhotoImage(file="\\Cancer Services - Radiation Physics\\Personal Folders\\Louie\\rprb_tools\\images\\logo.png")
        self.window.iconphoto(False,self.logo)

        # set title and colour
        self.window.title(self.win_title)
        self.window.configure(background='#3C3C3C')

        # empty dict to store widget outputs and counters to track number of each type
        self.lab_counter = 0
        self.butt_counter = 0
        self.dd_counter = 0
        self.cb_counter = 0
        self.tb_counter = 0

        self.outputs[self.win_title] = {}
        self.win_list.append(self.window)


    def butt_switch(self,num):
        self.outputs[f'button {num}'].set(True)
        self.window.withdraw()


    def get_pos(self,grid):
        col = grid[0]
        row = grid[1]

        if col > self.col_count:
            self.col_count = col
        if row > self.row_count:
            self.row_count = row


    def get_outputs(self,outputs):
        for form in outputs:
            for widget in outputs[form]:
                try:
                    outputs[form][widget] = outputs[form][widget].get()
                except:
                    outputs[form][widget] = None
        print(f'\noutput dictionary:\n{outputs}')


    def clear_outputs(self,outputs):
        for form in outputs:
            for widget in outputs[form]:
                outputs[form][widget] = None
        print(f'\noutput dictionary:\n{outputs}') 


    def close(self):
        self.clear_outputs(self.outputs)
        self.window.destroy()


    def submit(self):
        self.get_outputs(self.outputs)
        self.win_list[0].destroy()


    def add_label(self,grid,text,col_span=None,row_span=None):
        self.label = tk.Label(self.window,text=text)
        self.label.grid(row=grid[1],column=grid[0],columnspan=col_span,rowspan=row_span,padx=10,pady=10)
        self.label.config(bg='#3C3C3C',fg='#FFFFFF')

        self.get_pos(grid)
        self.lab_counter += 1
        self.outputs[self.win_title][f'label {self.lab_counter}'] = self.label


    def add_button(self,grid,text,action=None):
        self.butt_output = tk.BooleanVar()
        self.button = tk.Button(self.window,text=text)
        self.button.grid(row=grid[1],column=grid[0],padx=10,pady=10)
        self.button['command'] = action

        self.get_pos(grid)
        self.butt_counter += 1
        self.outputs[self.win_title][f'button {self.butt_counter}'] = self.butt_output


    def add_dropdown(self,grid,input):
        self.dd_output = tk.StringVar()
        self.dd_output.set("Select")
        self.dropdown = tk.OptionMenu(self.window,self.dd_output,*input)
        self.dropdown.grid(row=grid[1],column=grid[0],padx=10,pady=10)
        self.dropdown.config(highlightbackground='#3C3C3C')

        self.get_pos(grid)
        self.dd_counter += 1
        self.outputs[self.win_title][f'dropdown {self.dd_counter}'] = self.dd_output


    def add_checkbox(self,grid,text=None,action=None):
        self.cb_output = tk.IntVar(0)
        self.checkbox = tk.Checkbutton(self.window,text=text,variable=self.cb_output,onvalue=1,offvalue=0,command=action)
        self.checkbox.grid(row=grid[1],column=grid[0],padx=10,pady=10)
        self.checkbox.config(relief='raised')

        self.get_pos(grid)
        self.cb_counter += 1
        self.outputs[self.win_title][f'checkbox {self.cb_counter}'] = self.cb_output


    def add_textbox(self,grid,col_span=None,row_span=None):
        self.textbox = tk.Entry(self.window)
        self.textbox.grid(row=grid[1],column=grid[0],columnspan=col_span,rowspan=row_span,padx=10,pady=10)

        self.get_pos(grid)
        self.tb_counter += 1
        self.outputs[self.win_title][f'textbox {self.tb_counter}'] = self.textbox

    
    def add_close(self):
        self.close_button = tk.Button(self.window,text='Close',command=self.close)
        self.close_button.grid(row=self.row_count+1,column=0,columnspan=self.col_count+1,padx=10,pady=10)
        self.close_button.config(bg="#EE2B2B",relief='raised')


    def add_submit(self, submit_action=None):
        self.submit_button = tk.Button(self.window,text='Submit',command=submit_action or self.submit)
        self.submit_button.grid(row=self.row_count+1,column=0,columnspan=self.col_count+1,padx=10,pady=10)
        self.submit_button.config(bg="#228B22",relief='raised')


    def add_close_submit(self,submit_action=None):
        self.cs_frame = tk.Frame(self.window)
        self.cs_frame.configure(background='#3C3C3C')
        self.close_button = tk.Button(self.cs_frame,text='Close',command=self.close)
        self.close_button.grid(row=0,column=0,padx=10,pady=10)
        self.close_button.config(bg="#EE2B2B",relief='raised')

        self.submit_button = tk.Button(self.cs_frame,text='Submit',command=submit_action or self.submit)
        self.submit_button.grid(row=0,column=1,padx=10,pady=10)
        self.submit_button.config(bg="#228B22",relief='raised')

        self.cs_frame.grid(row=self.row_count+1,column=0,columnspan=self.col_count+1)

def ask_for_rating():
    rating_form = basic_form(title = "Provide rating")
    rating_form.add_label(grid = [0,0], text = "Choose rating:")
    rating_form.add_dropdown(grid = [0,5], input = ["1 - Clinically Unacceptable", "2 - Sub Optimal to VMAT Plan", "3 - Comparable to VMAT Plan", "4 - Improvement to VMAT Plan"])
    rating_form.add_close_submit()
    rating_form.window.mainloop()
    return rating_form

def gather_info():
    # load_plan()
    patient = get_current("Patient")
    patient_id = get_current("Patient").PatientID
    case = get_current("Case")
    exam = get_current("Examination")
    plan = get_current("Plan")
    beam_set = get_current("BeamSet")
    ui = get_current('ui')
    print(patient_id)
    plan_name_act = plan.Name
    print(plan_name_act)

    # plan_setup()
    beam_mod_act = beam_set.MachineReference.MachineName
    print(beam_mod_act)

    # tomo_param()
    proj_time = beam_set.Beams[0].BeamMU
    print(proj_time)
    jaw_front_act = str(plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].TomoPropertiesPerBeam.FrontJawPosition)
    jaw_back_act = str(plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].TomoPropertiesPerBeam.BackJawPosition)
    jaw_size_act = [jaw_front_act,jaw_back_act] # centimetres
    print(jaw_size_act)

    pitch_act = str(plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].TomoPropertiesPerBeam.PitchTomoHelical)
    print(pitch_act)

    dtf_act = str(plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].TomoPropertiesPerBeam.MaxDeliveryTimeFactor)
    print(dtf_act)

    del_time_act = round(proj_time * len(beam_set.Beams[0].Segments),0)  # seconds
    print(del_time_act)

    gantry_period_act = round(proj_time * 51,2) # seconds
    print(gantry_period_act)
    return plan, patient_id, plan_name_act, beam_mod_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act

def create_array(m, n):
    return System.Array.CreateInstance(System.Object, m, n)

def write_files(plan, patient_id, plan_name_act, beam_mod_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act, comment):
    result_filename = '\Cancer Services\Radiotherapy cx + hh\\Treatment Planning Systems\\RayStation\\18. Radixact Planning\\Tomo plan testing\\results.csv'

    # Write result to file (append mode) 
    try:
        with open(result_filename,'at',newline='') as csvfile:
            writer = csv.writer(csvfile,dialect='excel')
            writer.writerow([str(patient_id), str(plan_name_act), str(beam_mod_act), str(proj_time), str(jaw_size_act), str(pitch_act), str(dtf_act), str(del_time_act), str(gantry_period_act), str(comment)])
    except Exception as e:
        print(f"Failed to append to results file {result_filename}: {e}")

    # Define a filename with a timestamp to ensure it's unique and includes an extension
    filename = f"\Cancer Services\\Radiotherapy cx + hh\\Treatment Planning Systems\\RayStation\\18. Radixact Planning\\Tomo plan testing\\clinical_goals_export_{patient_id}_{datetime.datetime.now().strftime('%d%m%y')}.csv"

    try:
        with open(filename, "w") as f:
            # Write header to the CSV file
            f.write("Plan Name, ROI Name, Goal Criteria, Acceptance Level, Parameter Value, Clinical Goal Value, Goal Achieved\n")
            #print(f"Processing plan: {plan.Name}")
            
            # Find the clinical goals, there is a separate entry in EvaluationFunctions for each of the clinical goals
            number_of_goals = len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)
            #print(f"Number of clinical goals in plan '{plan.Name}': {number_of_goals}")
            
            if number_of_goals == 0:
                print(f"No clinical goals found for plan '{plan.Name}'.")
            
            results = create_array(number_of_goals, 6)
            
            for idx in range(number_of_goals):
                goal = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[idx]
                results[idx, 0] = goal.ForRegionOfInterest.Name # roi name
                results[idx, 1] = goal.PlanningGoal.GoalCriteria # criteria (e.g., at most/at least, etc.)
                if goal.PlanningGoal.Type == 'VolumeAtDose':
                    # For VolumeAtDose goals, multiply Level and Value by 100 to give value in %, divide limit by 100 to give value in Gy
                    results[idx, 2] = goal.PlanningGoal.PrimaryAcceptanceLevel * 100 # level (e.g., At most 50% volume...)
                    #print(goal.PlanningGoal.PrimaryAcceptanceLevel)
                    results[idx, 3] = goal.PlanningGoal.ParameterValue / 100 # limit (e.g., ...at 40.8 Gy)
                    #print(goal.PlanningGoal.ParameterValue)
                    results[idx, 4] = goal.GetClinicalGoalValue() * 100 # actual value in plan
                else: 
                    # For Dose related goals, multiply limit by 100 to give value in %, divide Level and Value by 100 to give value in Gy        
                    results[idx, 2] = goal.PlanningGoal.PrimaryAcceptanceLevel / 100 # level (e.g., at least 57Gy...)
                    #print(goal.PlanningGoal.PrimaryAcceptanceLevel)
                    results[idx, 3] = goal.PlanningGoal.ParameterValue * 100 # limit (e.g., ...at 98% volume)
                    #print(goal.PlanningGoal.ParameterValue)
                    results[idx, 4] = goal.GetClinicalGoalValue() / 100 # actual value in plan
                results[idx, 5] = str(goal.EvaluateClinicalGoal(EvaluateUsingSecondaryAcceptanceLevelIfExists = True)) # is goal achieved? (TRUE/FALSE)
                
            # Write results to the file
            for i in range(number_of_goals):
                f.write(f"{plan.Name}, {results[i,0]}, {results[i,1]}, {results[i,2]:.2f}, {results[i,3]:.2f}, {results[i,4]:.2f}, {results[i,5]}\r\n")
                
        print(f"Clinical goals have been successfully exported to {filename}")
    except Exception as e:
        print(f"Failed to write to file: {e}")

def main():
    plan, patient_id, plan_name_act, beam_mod_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act = gather_info()
    rating = ask_for_rating()
    if rating.outputs['Provide rating']['dropdown 1'] == "Select":
        messagebox.showerror("Error", "Please rerun and provide rating")
    else:
        #print(rating.outputs['Provide rating']['dropdown 1'])
        write_files(plan, patient_id, plan_name_act, beam_mod_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act, rating.outputs['Provide rating']['dropdown 1'])

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# don't edit
if __name__ == "__main__":
    main()
