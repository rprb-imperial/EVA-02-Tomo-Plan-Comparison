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

patient_db = get_current("PatientDB")
use_index_service = True


def load_patient_plan(patient_id, plan_name):
    patient_id = patient_id.strip()
    plan_name = plan_name.strip()

    patientq = patient_db.QueryPatientInfo(Filter={"PatientID": patient_id}, UseIndexService=use_index_service)
    if len(patientq) == 0:
        raise RuntimeError(f"Patient not found in RayStation: {patient_id}")

    patient = patient_db.LoadPatient(PatientInfo=patientq[0], AllowPatientUpgrade=True)

    selected_case = None
    selected_plan_name = None

    for case in patient.Cases:
        for treatment_plan in case.TreatmentPlans:
            if plan_name.lower() in treatment_plan.Name.lower():
                selected_case = case
                selected_plan_name = treatment_plan.Name
                break
        if selected_case is not None:
            break

    if selected_case is None:
        raise RuntimeError(f"Plan not found for patient {patient_id}: {plan_name}")

    selected_case.SetCurrent()
    case = get_current("Case")
    plan_info = case.QueryPlanInfo(Filter={"Name": selected_plan_name})
    if 'DIRONE' in plan_info[0]['ApprovedByLoginName']:
        plan_info[0]['ApprovedByLoginName'] = plan_info[0]['ApprovedByLoginName'][:5]
    if len(plan_info) == 0:
        raise RuntimeError(f"Could not query plan {selected_plan_name} for patient {patient_id}")

    case.LoadPlan(PlanInfo=plan_info[0])
    plan = case.TreatmentPlans[selected_plan_name]
    beam_set = get_current("BeamSet")
    if beam_set is None:
        beam_set = plan.BeamSets[0]

    return plan, patient_id, plan.Name, beam_set


def gather_info(patient_id, plan_name):
    plan, patient_id, plan_name_act, beam_set = load_patient_plan(patient_id, plan_name)
    patient = get_current("Patient")
    patient_id = patient.PatientID
    case = get_current("Case")
    exam = get_current("Examination")
    beam_set = get_current("BeamSet")
    ui = get_current('ui')
    print(patient_id)
    print(plan_name_act)

    beam_mod_act = ''
    if beam_set is not None:
        machine_reference = getattr(beam_set, 'MachineReference', None)
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
    return plan, patient_id, plan_name_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act

def create_array(m, n):
    return System.Array.CreateInstance(System.Object, m, n)

def write_files(plan, patient_id, plan_name_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act):
    export_dir = r'\Cancer Services\Radiotherapy cx + hh\Treatment Planning Systems\RayStation\18. Radixact Planning\Tomo plan testing'
    result_filename = os.path.join(export_dir, 'results.csv')

    # Write result to file (append mode) 
    try:
        with open(result_filename,'at',newline='') as csvfile:
            writer = csv.writer(csvfile,dialect='excel')
            writer.writerow([str(patient_id), str(plan_name_act), str(proj_time), str(jaw_size_act), str(pitch_act), str(dtf_act), str(del_time_act), str(gantry_period_act)])
    except Exception as e:
        print(f"Failed to append to results file {result_filename}: {e}")

    # Define a filename with a timestamp to ensure it's unique and includes an extension
    filename = os.path.join(export_dir, f"clinical_goals_export_{patient_id}_{datetime.datetime.now().strftime('%d%m%y')}.csv")

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
    patient_file = r'\Cancer Services\Radiotherapy cx + hh\Treatment Planning Systems\RayStation\18. Radixact Planning\Tomo plan testing\new\patient_file.csv'

    try:
        with open(patient_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue

                if len(row) < 2:
                    continue

                patient_id = row[0].strip()
                plan_name = row[1].strip()

                if not patient_id or not plan_name:
                    continue

                if patient_id.lower().startswith('patient'):
                    continue

                try:
                    plan, patient_id, plan_name_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act = gather_info(patient_id, plan_name)
                    write_files(plan, patient_id, plan_name_act, proj_time, jaw_size_act, pitch_act, dtf_act, del_time_act, gantry_period_act)
                except Exception as e:
                    print(f"Failed processing patient {patient_id}, plan {plan_name}: {e}")
    except Exception as e:
        print(f"Failed to read patient file {patient_file}: {e}")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# don't edit
if __name__ == "__main__":
    main()
