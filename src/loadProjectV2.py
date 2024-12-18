'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are not permitted provided that the code retains the
above copyright notice.
'''

from defs import *
from playwright.sync_api import sync_playwright
import pyautogui
import keyboard
import time
import pyperclip
from tkinter import messagebox
import os
import sys

def main():
    # Derive script name and prompt for job ID
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    job_id = simpledialog.askstring("Input", "Enter Job ID:", initialvalue="ST")

    print(f"Script: {script_name} | Job ID: {job_id}")
    sys.stdout.flush()

    # Load state
    state = load_state(script_name, job_id)

    start_time = get_time_in_human()
    selected_step = prompt_user_for_checkpoint_with_dropdown(script_name, job_id)

    print(f"Starting from step: {selected_step}")
    sys.stdout.flush()

    if selected_step == "start":
        pyperclip.copy(job_id)
        with open(r"..\job_id.txt", "w") as idFile:
            idFile.write(job_id)
        print(f"Job number {job_id} saved.")
        sys.stdout.flush()
        save_checkpoint("job_number_collected", script_name, job_id)

    if selected_step in ["job_number_collected", "start"]:
        if is_capslock_on():
            pyautogui.press('capslock')
            print("Caps Lock was on. Turning it off.")
        else:
            print("Caps Lock was already off.")
        sys.stdout.flush()
        save_checkpoint("capslock_checked", script_name, job_id)

    if selected_step in ["capslock_checked", "job_number_collected", "start"]:
        terminate_program()
        print("Terminate program initiated. Waiting for 'Esc' key to exit.")
        sys.stdout.flush()
        save_checkpoint("terminate_program_initiated", script_name, job_id)

    with sync_playwright() as p:
        if selected_step in ["terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            browser = p.chromium.launch(headless=False, channel="msedge", args=["--start-maximized", "--disable-infobars"])
            context = browser.new_context()
            page = context.new_page()
            page.goto('https://steedform.moraware.net/sys/')
            print("Navigated to Moraware login page.")
            sys.stdout.flush()

            username, password = get_credentials(path_to_credentials=r"..\credentials.txt")
            page.fill('input[name="user"]', username)
            page.fill('input[name="pwd"]', password)
            page.click('#LOGIN')
            page.wait_for_load_state('networkidle')
            print("Login completed.")
            sys.stdout.flush()
            save_checkpoint("login_completed", script_name, job_id)

        if selected_step in ["login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            time.sleep(0.5)
            click_element(*get_coordinates('search_fd', coordinates))
            time.sleep(0.5)
            print("Search field clicked.")
            sys.stdout.flush()
            save_checkpoint("search_fd_clicked", script_name, job_id)

        if selected_step in ["search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            pyautogui.write(job_id)
            print("Pasted job number into search field.")
            time.sleep(0.2)
            click_element(*get_coordinates('search_btn', coordinates))
            print("Search button clicked.")
            time.sleep(1)
            sys.stdout.flush()
            save_checkpoint("search_btn_clicked", script_name, job_id)

        if selected_step in ["search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            time.sleep(0.5)
            click_element(*get_coordinates('search_result', coordinates))
            print("Search result selected.")
            time.sleep(2.2)
            sys.stdout.flush()
            save_checkpoint("search_result_selected", script_name, job_id)

        if selected_step in ["search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            elements = page.query_selector_all('td:has(div:has-text("Selections:")) div > table')
            write_job_det_to_csv(elements=elements)
            print("Job details written to CSV.")
            sys.stdout.flush()

            job_name_element = page.query_selector_all('.pageInfoLabel:has-text("Job Name:") + .pageInfoValue')
            job_name, job_name2, job_name_full = get_job_name(job_name_element=job_name_element, path_job_name=r"..\Job_name_full.txt")

            file_path = r"..\selections_data.csv"
            data = read_csv(file_path)
            state['data'] = data
            state['job_name'] = job_name
            state['job_name_full'] = job_name_full
            categorize_fields(data)
            save_state(script_name, job_id, state)

            time.sleep(0.5)
            browser.close()
            print("Browser closed after extracting job details.")
            sys.stdout.flush()
            save_checkpoint("data_extracted", script_name, job_id)

        state = load_state(script_name, job_id)  # Reload state

        if selected_step in ["data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            shortcut_path = "C:\\Sekon\\SekonPrograms\\SeCAD V12\\SeCAD12 - Shortcut.lnk"
            os.startfile(shortcut_path)
            print("SeCAD application started.")
            time.sleep(2)
            sys.stdout.flush()
            save_checkpoint("secad_started", script_name, job_id)

        if selected_step in ["secad_started", "data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            keyboard.wait('ctrl+0')
            print("StreamDeck input received.")
            sys.stdout.flush()
            save_checkpoint("streamdeck_input_received", script_name, job_id)

        if selected_step in ["streamdeck_input_received", "secad_started", "data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            # dynamic job_id
            base_path = r"S:\Sekon Master Data\CAD-CAM-Data\SeCAD12-Files"
    
            # Get the final job_id_save name
            job_id_save = handle_existing_job_id(job_id, base_path)
            print(f"Final job_id_save: {job_id_save}")
            sys.stdout.flush()
            click_element(*get_coordinates('file', coordinates))
            time.sleep(0.1)
            click_element(*get_coordinates('save_project_as', coordinates))
            time.sleep(0.1)
            click_element(*get_coordinates('file_name_fd', coordinates))
            time.sleep(0.1)
            pyautogui.write(job_id_save)
            time.sleep(0.2)
            click_element(*get_coordinates('save', coordinates))
            print("Project saved in SeCAD.")
            sys.stdout.flush()
            save_checkpoint("project_saved", script_name, job_id)

        if selected_step in ["project_saved", "streamdeck_input_received", "secad_started", "data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            click_element(*get_coordinates('order_data', coordinates))
            time.sleep(0.2)
            categorized_results = categorize_fields(state['data'])

            click_element(*get_coordinates('material_colour', coordinates))
            time.sleep(0.2)
            pyautogui.write(categorized_results.get('Material Colour', 'various'))
            print("Material colour populated.")

            click_element(*get_coordinates('material_brand', coordinates))
            time.sleep(0.2)
            pyautogui.write(categorized_results.get('Material Brand', 'various'))
            print("Material brand populated.")

            click_element(*get_coordinates('edge_profile', coordinates))
            time.sleep(0.2)
            pyautogui.write(categorized_results.get('Edge Profile', 'various'))
            print("Edge profile populated.")

            click_element(*get_coordinates('thickness', coordinates))
            time.sleep(0.2)
            try:
                pyautogui.write(categorized_results.get('Material Thickness', 'various').split("mm")[0])
            except Exception as e:
                pyautogui.write(categorized_results.get('Material Thickness', 'various'))
            time.sleep(0.2)
            print("Material thickness populated.")

            click_element(*get_coordinates('job_name', coordinates))
            time.sleep(0.2)
            pyautogui.write(state['job_name_full'])
            print("Job name populated.")

            if categorized_results.get('Material Brand', 'various').strip() == 'SA Zenith Surfaces':
                click_element(*get_coordinates('clk_grp_drp_dwn', coordinates))
                time.sleep(0.2)
                click_element(*get_coordinates('clk_grp_stn', coordinates))
                time.sleep(0.2)
                click_element(*get_coordinates('clk_mtrl_drp_dwn', coordinates))
                time.sleep(0.2)
                click_element(*get_coordinates('clk_mtrl', coordinates))
                time.sleep(0.2)
                print("Done Updating the Material Groups!")

            messagebox.showinfo("Important", "Well, Click next on your streamDeck when you are done with the Inputs ;)")
            keyboard.wait("ctrl+0")

            click_element(*get_coordinates('order_okay', coordinates))
            time.sleep(0.2)
            print("Order details filled successfully!")
            sys.stdout.flush()
            save_checkpoint("fields_and_materials_filled", script_name, job_id)

        if selected_step in ["fields_and_materials_filled", "project_saved", "streamdeck_input_received", "secad_started", "data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            time.sleep(0.2)
            print("Im in here!!")
            sys.stdout.flush()
            click_element(*get_coordinates('file', coordinates))
            time.sleep(0.1)
            click_element(*get_coordinates('file_import', coordinates))
            time.sleep(0.5)
            click_element(*get_coordinates('import_dxf', coordinates))
            time.sleep(0.1)
            click_element(*get_coordinates('import_menu_bar', coordinates))
            time.sleep(0.2)
            pyautogui.write(get_jobs_path(r"..\jobs_path.txt"))
            time.sleep(0.1)
            perform_shortcut("enter")
            click_element(*get_coordinates('import_file_fd', coordinates))
            pyautogui.write(job_id)
            time.sleep(0.1)
            perform_shortcut("enter")
            time.sleep(0.1)
            pyautogui.write(job_id)
            time.sleep(0.1)
            pyautogui.write("T")
            time.sleep(0.1)
            click_element(*get_coordinates('import_btn', coordinates))
            time.sleep(0.1)
            perform_shortcut('Enter')
            time.sleep(0.3)
            print("DXF file imported.")
            sys.stdout.flush()
            save_checkpoint("dxf_imported", script_name, job_id)

        if selected_step in ["dxf_imported", "fields_and_materials_filled", "project_saved", "streamdeck_input_received", "secad_started", "data_extracted", "search_result_selected", "search_btn_clicked", "search_fd_clicked", "login_completed", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
            end_time = get_time_in_human()
            elapsed_time = elapsed_time_cal(start_time=start_time, end_time=end_time)
            print(f"Process completed in {elapsed_time} seconds.")
            sys.stdout.flush()
            messagebox.showinfo("Completed!", f"Process Completed! Elapsed Time: {elapsed_time} seconds.")
            clear_checkpoint(script_name, job_id)

if __name__ == '__main__':
    validate_license()
    main()
