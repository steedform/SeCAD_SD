'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are not permitted provided that the code retains the
above copyright notice.
'''

from tkinter import simpledialog
from playwright.sync_api import sync_playwright
import csv
import pyautogui
import keyboard
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox
import sys
import time
from defs import get_printer as gp
from defs import terminate_program as tp
from defs import *


tp()

coordinates = read_coordinates_from_csv(r"..\coordinates_SE.csv")

def main():
    # Derive script name and read job ID from file
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(r"..\job_id.txt", "r") as idFile:
        job_id = idFile.read().strip()

    print(f"Script: {script_name} | Job ID: {job_id}")
    sys.stdout.flush()
    
    # Load state
    state = load_state(script_name, job_id)
    print(state)

    start_time = get_time_in_human()
    selected_step = prompt_user_for_checkpoint_with_dropdown(script_name, job_id)

    print(f"Starting from step: {selected_step}")
    sys.stdout.flush()

    if selected_step == "start":
        print(f"Job number {job_id} loaded from file.")
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

    # Step: Move to Sales Tab
    if selected_step in ["terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        click_element(*get_coordinates('moveToSales', coordinates))
        print("Moved to Sales tab.")
        sys.stdout.flush()
        save_checkpoint("moved_to_sales", script_name, job_id)

    # Step: Create View
    if selected_step in ["moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        click_element(*get_coordinates('createView', coordinates))
        print("Clicked on Create View.")
        time.sleep(0.4)
        move_to(*get_coordinates('Random_Sales', coordinates))
        time.sleep(0.1)
        # Click on really create yes
        perform_shortcut('Enter')

        perform_shortcut('Enter')

        sys.stdout.flush()
        save_checkpoint("view_created", script_name, job_id)

    # Step: Handle Printer
    if selected_step in ["view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        # Click on print tab
        click_element(*get_coordinates('printTab', coordinates))

        # click on printer drpdwn
        click_element(*get_coordinates('prtDrpDwn', coordinates))
        gp(r"..\prt_sales_con.txt", "Sales", "prtDrpDwn", "salesPrt")
        print("Handled printer configuration.")
        sys.stdout.flush()
        save_checkpoint("printer_handled", script_name, job_id)

    # Step: Print Copies
    if selected_step in ["printer_handled", "view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        um_file = open(r"..\um.txt", 'r')
        um = um_file.read().strip()

        if um == "True":
            no_of_copies = "3"
        else:
            no_of_copies = "2"

        state['no_of_copies'] = no_of_copies
        save_state(script_name, job_id, state)
        click_element(*get_coordinates("noCopies", coordinates))
        pyperclip.copy(no_of_copies)
        time.sleep(0.2)
        perform_shortcut("ctrl+V")
        time.sleep(0.1)
        click_element(*get_coordinates('prt', coordinates))
        print(f"Printed {no_of_copies} copies for Sales Printer (Brother JFC).")
        sys.stdout.flush()
        save_checkpoint("copies_printed", script_name, job_id)
    
    
    # Step: PDF Confirmation
    if selected_step in ["copies_printed", "printer_handled", "view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        root = tk.Tk()
        root.withdraw()
        print(no_of_copies)
        response_print_pdf = messagebox.askokcancel(
            "Confirmation", "Do you wish to print it as a PDF?")
        state['response_print_pdf'] = response_print_pdf
        save_state(script_name, job_id, state)
        if response_print_pdf:
            print("User clicked OK. Proceeding...")
            no_diags = int(simpledialog.askstring("Input", "Please Enter the number of Diagrams"))
            state['no_diags'] = no_diags
            save_state(script_name, job_id, state)
            gp(r"..\prt_sales_pdf_con.txt", "SalesPDF", "prtDrpDwn", "pdfPrt")
            click_element(*get_coordinates("noCopies", coordinates))
            pyperclip.copy(1)
            perform_shortcut("ctrl+V")
            time.sleep(0.1)
            click_element(*get_coordinates('prt', coordinates))
            for i in range(state['no_diags']):
                print("No diags", state['no_diags'], "type", type(state['no_diags']))
                print(i)
                time.sleep(1.5)
                click_element(*get_coordinates('savePdfMenu', coordinates))
                jobs_path_pdf = get_jobs_path(r"..\jobs_path.txt")
                job_id_pdf = get_job_id(r"..\job_id.txt")
                state['job_id_pdf'] = job_id_pdf
                state['jobs_path_pdf'] = jobs_path_pdf
                save_state(script_name, job_id, state)
                pyautogui.write(fr"{jobs_path_pdf}\{job_id_pdf}")
                time.sleep(0.2)
                perform_shortcut("Enter")
                time.sleep(0.2)
                click_element(*get_coordinates('svPdfFd', coordinates))
                time.sleep(0.2)
                pyautogui.write(f"{job_id_pdf}_{i}")
                time.sleep(0.2)
                perform_shortcut("Enter")
                time.sleep(1.5)
                print("Done {}".format(i))
            save_checkpoint("pdf_saved", script_name, job_id)
        else:
            print("User clicked Cancel. Aborting PDF print process.")
            sys.stdout.flush()
            
    state = load_state(script_name, job_id)
    if selected_step in ["pdf_saved", "copies_printed", "printer_handled", "view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        if state['response_print_pdf']:
            with sync_playwright() as p:
                # Launch the browser
                browser = p.chromium.launch(headless=False, channel="msedge", args=["--start-maximized", "--disable-infobars"])
                context = browser.new_context()
                page = context.new_page()

                # Navigate to the login page
                page.goto('https://steedform.moraware.net/sys/')  # Replace with your actual login URL
                page.set_viewport_size({"width": 1920, "height": 1080})

                # Get credentials from a file or another source
                username, password = get_credentials(path_to_credentials=r"../credentials.txt")

                # Fill in the login form using the updated selectors
                page.fill('input[name="user"]', username)  # Username field
                page.fill('input[name="pwd"]', password)    # Password field

                # Click the login button
                page.click('#LOGIN')

                # Wait for the page to load
                page.wait_for_load_state('networkidle')

                print(f"Logged in successfully as {username}")

                # Now go to the page with the table
                click_element(*get_coordinates('search_fd', coordinates))
                
                time.sleep(0.4)
                
                pyautogui.write(state['job_id_pdf'])
                
                time.sleep (0.1)
                
                click_element(*get_coordinates('search_btn', coordinates))
                
                time.sleep(0.5)
                page.wait_for_load_state('networkidle')
                time.sleep(3)
                click_element(*get_coordinates('search_result', coordinates))
                page.wait_for_load_state('networkidle')

                # Example: Extract table data
                rows = page.locator('#FilesScroll1Body tr')
                for i in range(rows.count()):
                    # Get all the cell texts for the row
                    cells = rows.nth(i).locator('td')
                    cell_data = [cells.nth(j).inner_text() for j in range(cells.count())]
                    print(f"Row {i+1}: {cell_data}")
                    
                # Example: Click the button to attach a file
                attach_button_selector = '#btnCreateFile'
                page.click(attach_button_selector)

                for i in range(state['no_diags']):
                    time.sleep(2)
                    # Wait for the label element to be visible
                    page.wait_for_selector('label.fileUploadButton')

                    # Click on the label to activate the file input
                    page.click('label.fileUploadButton')
                    
                    time.sleep(2)
                    
                    pyautogui.write(rf"{state['jobs_path_pdf']}\{state['job_id_pdf']}\{state['job_id_pdf']}_{i}")
                    time.sleep(0.5)
                    perform_shortcut('Enter')
                    
                    time.sleep(1)
                
                    page.wait_for_selector('select[name="attrVal3"]')

                # Select the "CAD file" option by its value
                page.select_option('select[name="attrVal3"]', '10')
                time.sleep(1)
                
                # Wait for the "Save" button and click it
                page.wait_for_selector('button.dialogSubmitButton[name="ok"]')
                page.click('button.dialogSubmitButton[name="ok"]')
                time.sleep(3)
                browser.close()
                print("Uploading process completed!")
                sys.stdout.flush()
                save_checkpoint("pdf_uploaded", script_name, job_id)
            # Add your code for the OK condition here
        else:
            print("User clicked Cancel. Aborting print pdf process........") 
        
    
    # Step: Move to Production
    if selected_step in ["pdf_uploaded", "pdf_saved", "copies_printed", "printer_handled", "view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        click_element(*get_coordinates("proTab", coordinates))
        time.sleep(0.5)
        print("Moved to Production tab.")
        sys.stdout.flush()
        click_element(*get_coordinates("createViewPro", coordinates))
        time.sleep(2)
        move_to(*get_coordinates('Random_Sales', coordinates))
        perform_shortcut("Enter")
        perform_shortcut("Enter")
        print("Created the view for Production")
        sys.stdout.flush()
        save_checkpoint("moved_to_production", script_name, job_id)

    # Final Step: Complete Process
    if selected_step == ["moved_to_production", "pdf_uploaded", "pdf_saved", "copies_printed", "printer_handled", "view_created", "moved_to_sales", "terminate_program_initiated", "capslock_checked", "job_number_collected", "start"]:
        end_time = get_time_in_human()
        elapsed_time = elapsed_time_cal(start_time=start_time, end_time=end_time)
        print(f"Process completed in {elapsed_time} seconds.")
        sys.stdout.flush()
        messagebox.showinfo("Completed!", f"Process Completed! Elapsed Time: {elapsed_time} seconds.")
        clear_checkpoint(script_name, job_id)

if __name__ == '__main__':
    main()
