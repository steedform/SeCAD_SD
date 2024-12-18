'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are not permitted provided that the code retains the
above copyright notice.
'''

from defs import *
from defs import get_printer as gp
import pyautogui
import time
import os
import sys

def main():
    # Derive script name and read job ID
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(r"..\job_id.txt", "r") as idFile:
        job_id = idFile.read().strip()

    print(f"Script: {script_name} | Job ID: {job_id}")
    sys.stdout.flush()

    # Load state
    state = load_state(script_name, job_id)
    selected_step = prompt_user_for_checkpoint_with_dropdown(script_name, job_id)

    print(f"Starting from step: {selected_step}")
    sys.stdout.flush()

    # Read coordinates
    coordinates = read_coordinates_from_csv(r"..\coordinates_SE.csv")
    time.sleep(0.1)

    # Step: Move to Print Tab
    if selected_step in ["start"]:
        click_element(*get_coordinates("proPrtTab", coordinates))
        print("Moved to Print tab.")
        sys.stdout.flush()
        save_checkpoint("print_tab_selected", script_name, job_id)

    # Step: Select Printer Dropdown
    if selected_step in ["print_tab_selected", "start"]:
        click_element(*get_coordinates("proPrtDrpDwn", coordinates))
        time.sleep(0.2)
        gp(r"..\prt_prod_con.txt", "Production", "proPrtDrpDwn", "proPrt")
        print("Printer selected from dropdown.")
        sys.stdout.flush()
        save_checkpoint("printer_selected", script_name, job_id)

    # Step: Select Number of Printouts
    if selected_step in ["printer_selected", "print_tab_selected", "start"]:
        click_element(*get_coordinates("no_prt_outs", coordinates))
        time.sleep(0.5)
        pyautogui.write("1")
        print("Number of printouts entered.")
        sys.stdout.flush()
        save_checkpoint("printouts_selected", script_name, job_id)

    # Step: Click Print All
    if selected_step in ["printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        click_element(*get_coordinates("proPrtAll", coordinates))
        print("Clicked on Print All.")
        time.sleep(2)
        sys.stdout.flush()
        save_checkpoint("print_all_clicked", script_name, job_id)

    # Step: Move to Export Tab
    if selected_step in ["print_all_clicked", "printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        click_element(*get_coordinates("exportTab", coordinates))
        print("Moved to Export tab.")
        time.sleep(4)
        sys.stdout.flush()
        save_checkpoint("export_tab_selected", script_name, job_id)

    # Step: Click on XML Tab
    if selected_step in ["export_tab_selected", "print_all_clicked", "printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        click_element(*get_coordinates("xmlTab", coordinates))
        print("XML tab selected.")
        sys.stdout.flush()
        save_checkpoint("xml_tab_selected", script_name, job_id)

    # Step: Save XML File
    if selected_step in ["xml_tab_selected", "export_tab_selected", "print_all_clicked", "printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        click_element(*get_coordinates("name_xml", coordinates))
        time.sleep(0.5)
        click_element(*get_coordinates("xml_save", coordinates))
        print("XML file saved.")
        time.sleep(0.6)
        sys.stdout.flush()
        save_checkpoint("xml_saved", script_name, job_id)

    # Step: Close Application
    if selected_step in ["xml_saved", "xml_tab_selected", "export_tab_selected", "print_all_clicked", "printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        perform_shortcut("alt+F4")
        time.sleep(0.2)
        perform_shortcut('Enter')
        click_element(*get_coordinates("save_project_final", coordinates))
        print("Application closed and project saved.")
        sys.stdout.flush()
        save_checkpoint("project_final_saved", script_name, job_id)

    # Final Step: Complete Script
    if selected_step == ["project_final_saved", "xml_saved", "xml_tab_selected", "export_tab_selected", "print_all_clicked", "printouts_selected", "printer_selected", "print_tab_selected", "start"]:
        print("Script completed successfully!")
        sys.stdout.flush()
        clear_checkpoint(script_name, job_id)

if __name__ == '__main__':
    validate_license()
    main()
