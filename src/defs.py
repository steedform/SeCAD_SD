'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without   
modification, are not permitted provided that the code retains the 
above copyright notice.
'''

from playwright.sync_api import sync_playwright
import csv
import pyautogui
import keyboard
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox
import sys, os, psutil
import time
from tkinter import simpledialog
import threading
import pytesseract
import cv2
import argparse
import ctypes
from fuzzywuzzy import fuzz
import logging
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar, OptionMenu
import json

logging.basicConfig(filename="output.log", level=logging.DEBUG)

sys.stdout = open(r"..\output_file.txt", 'w')  # Redirect standard output
sys.stderr = open(r"..\error_file.txt", 'w')    # Redirect standard error (optional)

# Function to listen for a key press and terminate the application
def listen_for_exit_key():
    keyboard.wait('esc')  # Wait for the 'Esc' key
    messagebox.showinfo("ByeBye!","Exiting Program.......")
    print("Program Terminated")# Optional: Print a message to the output file
    sys.stdout.flush()
    os._exit(0)  # Forcefully exit the program
    

def terminate_program():
    # Start the key listener in a separate thread
    exit_thread = threading.Thread(target=listen_for_exit_key)
    exit_thread.daemon = True  # This allows the thread to exit when the main program exits
    exit_thread.start()            


def read_csv(file_path):
    """Reads the CSV file and returns the data as a list of rows."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [row for row in reader if row]  # Filter out empty rows
    return data

def categorize_fields(data):
    """Categorizes fields as 'common_<field_name>' or 'various' based on their values across rows."""
    field_names = data[0][1:]  # Field names excluding area
    num_fields = len(field_names)
    
    # Initialize common variables
    common_values = {}
    
    for i in range(num_fields):
        current_field_values = [row[i + 1] for row in data[1:]]  # Gather values for the current field
        unique_values = set(current_field_values)
        #print(common_values[field_names[i]])
        if len(unique_values) == 1:  # All values are the same
            common_values[field_names[i]] = current_field_values[0]
        else:
            common_values[field_names[i]] = 'various'  # Different values
        

    return common_values
        

#Function Move ontop of a specific element
def move_to(x,y):
    pyautogui.moveTo(x,y)
    time.sleep(0.3)

# Function to click on a specific element
def click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.3)
    
# Function to click on a specific element
def double_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick()
    time.sleep(0.6)
    
# Function to click on a specific element
def right_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')
    time.sleep(1)
    
# Function to switch to the next tab in Edge
def switch_app_tab():
    keyboard.press_and_release('alt+tab')
    time.sleep(1)  # Wait for the tab to switch
    
def open_new_site_url(url):
    keyboard.press_and_release("ctrl+T")
          # Focus the address bar
    pyautogui.write(url)
    pyautogui.press('enter')
    time.sleep(4)
    
def perform_shortcut(shortcut):
    keyboard.press_and_release(shortcut)
    time.sleep(0.35)
    
# Function to read coordinates from CSV
def read_coordinates_from_csv(file_path):
    coordinates = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:  # Ensure there are exactly 3 columns
                name = row[0]  # First column is the name
                x = int(row[1])  # Second column is x
                y = int(row[2])  # Third column is y
                coordinates[name] = (x, y)
    return coordinates

# Function to get coordinates by name
def get_coordinates(name, coordinates):
    return coordinates.get(name, None)

coordinates = read_coordinates_from_csv(r"..\coordinates_SE.csv")


def get_jobs_path(jobs_file_path):
    file_jobs_path = open(jobs_file_path, "r")
    jobs_path = file_jobs_path.read()
    jobs_path = jobs_path.strip()
    
    return jobs_path

def get_job_id(job_id_file_path):
    file_job_id = open(job_id_file_path)
    job_id = file_job_id.read().strip()
    
    return job_id
    

def get_credentials(path_to_credentials):
    with open(path_to_credentials, mode='r') as C_file:
        credentials_content = C_file.read()
        if credentials_content == "None":
            messagebox.showerror("Invalid format for Credentials Files. #1414")
            raise ValueError("Invalid Format of Credentials File! #1414")
        try:
            credentials = credentials_content.split("\n")
        except Exception as e:
            messagebox.showerror('Invalid format for Credentials Files. Terminating #1919')
            raise ValueError(f"{e} #1919")
        
        if len(credentials) == 2:
            print("Valid Credemntials Format!")
        else:
            raise ValueError("Invalid Format for credentials file #222")
        
        for cred in credentials:
            if "username" in cred.strip():
                username = cred.split("username:")[1].strip()
            elif "password" in cred.strip():
                password = cred.split("password:")[1].strip()   
            else:
                raise ValueError("Invalid formart for credentials #F0000")
        
        return username, password
    
def get_job_name(job_name_element, path_job_name):
    if job_name_element:
        job_name_full = job_name_element[0].inner_text()
        print("Job Name:", job_name_full)
    else:
        print("Job Name not found.")
        job_name = ""
    
    with open(path_job_name, mode='w') as file_job_name:
        # Initial splitting logic based on the presence of dash or comma
        if "-" in job_name_full and "," in job_name_full:
            # Find the first occurrence of both characters
            first_dash = job_name_full.find("-")
            first_comma = job_name_full.find(",")

            # Split from the first occurring character
            if first_dash < first_comma and first_dash != -1:
                job_name = job_name_full[:first_dash].strip()
                job_name2 = job_name_full[first_dash + 1:].strip()
                file_job_name.write(f"1. {job_name_full}")
            else:
                job_name = job_name_full[:first_comma].strip()
                job_name2 = job_name_full[first_comma + 1:].strip()
                file_job_name.write(f"2. {job_name_full}")
        elif "-" in job_name_full:
            job_name = job_name_full.split("-")[0].strip()
            job_name2 = job_name_full.split("-")[1].strip()
            file_job_name.write(f"1. {job_name_full}")
        elif "," in job_name_full:
            job_name = job_name_full.split(",")[0].strip()
            job_name2 = job_name_full.split(",")[1].strip()
            file_job_name.write(f"2. {job_name_full}")
        else:
            job_name = job_name_full
            job_name2 = ""
            file_job_name.write(f"3. {job_name_full}")

        # Check lengths of job_name and job_name2 after the first split
        if len(job_name) <= len(job_name2):
            # Split the full job_name_full by the first comma
            if "," in job_name_full:
                job_name = job_name_full.split(",", 1)[0].strip()
                job_name2 = job_name_full.split(",", 1)[1].strip() if len(job_name_full.split(",", 1)) > 1 else ""
                file_job_name.write(f"Split from comma: {job_name} and {job_name2}")

        # Now check the other way around: if we initially split by a comma
        if len(job_name) <= len(job_name2):
            # Split the full job_name_full by the first dash
            if "-" in job_name_full:
                job_name = job_name_full.split("-", 1)[0].strip()
                job_name2 = job_name_full.split("-", 1)[1].strip() if len(job_name_full.split("-", 1)) > 1 else ""
                file_job_name.write(f"Split from dash: {job_name} and {job_name2}")

        # Final results
        print(f"Job Name: {job_name}")
        print(f"Job Name 2: {job_name2}")
            
        time.sleep(1)
        
        file_job_name.flush()
        return job_name, job_name2, job_name_full
    
    
def write_job_det_to_csv(elements):
    csv_data = []
    capturing_data = True
    count = 0

    for row in elements:
        # Get all cells in the current row
        cells = row.query_selector_all('td')
                
        if cells and cells[0].evaluate("el => el.style.fontWeight === 'bold'"):
            if capturing_data == True:
                row_data = [cell.inner_text().strip() for cell in cells]
                #print(row_data, capturing_data)
                #print("appending1")
                csv_data.append(row_data)
                capturing_data = False
            else:
                row_data = [cell.inner_text().strip() for cell in cells]
                print(row_data, capturing_data)
                #print("llllllalalalallalalalalal")
                if os.path.isfile(r"..\um.txt"):
                    try:
                        os.remove(r"..\um.txt")
                    except Exception as e:
                        print(f"{e}\n Couldnt delete the under mount file")
                        
                with open(r"..\um.txt", "w") as um_file:
                    for i, um_data_lbl in enumerate(row_data):
                        if um_data_lbl.strip().lower() == "undermount":
                            um_file.write("True")
                            um_file.flush()
                            break
                        else:
                            if i == len(row_data) - 1:
                                um_file.write("False")
                                um_file.flush()                        
                #print("Im here!!")     
                break
        else:
            if count == 0:
                count = count + 1
                pass
            else:
                if len(cells) > 0:  # Ensure there are cells to capture
                    row_data = [cell.inner_text().strip() for cell in cells]
                    print(f"Row Data and Capturing Data\n{row_data}, {capturing_data} \n")
                    csv_data.append(row_data)
                    #print("appending2")
              
    csv_write = []   
    csv_line_by_line = []            
    for i, csv_data_line in enumerate(csv_data[0]):
        #print("I am looping")
        if i % 7 == 0 and i != 0:
            csv_write.append(csv_line_by_line)
            csv_line_by_line = []
            csv_line_by_line.append(csv_data_line)
        else:
            csv_line_by_line.append(csv_data_line)
            print(csv_line_by_line)
            if i == len(csv_data[0]) - 1:
                csv_write.append(csv_line_by_line)
                
    print("csv_data\n \n \n")
    print(csv_data)        
    print("\ncsv_write\n \n \n")        
    print(csv_write)        
    # Print the collected CSV data
    # Optionally, write to CSV
    with open(r"..\selections_data.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_write)
                    
def get_time_in_human():
    current_time = time.time()
    return current_time

def elapsed_time_cal(start_time, end_time):
    time_diff = end_time - start_time
    return time_diff

def argparser():
    parser = argparse.ArgumentParser(description="Stream Deck Operation")
    parser.add_argument('--button', type=str, help='Button Name')
    args = parser.parse_args()
    return args

# Check if Caps Lock is on
def is_capslock_on():
    # 0x14 is the virtual key code for Caps Lock
    return ctypes.WinDLL("User32.dll").GetKeyState(0x14) == 1


print("Caps Lock is now off (if it was on).")

def get_printer(prt_file_path, tab_name, drpdwn, prt_name):
    time.sleep(2)
    
    # Set up Tesseract path if not already in PATH
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path if needed

    # Step 2: Take a screenshot of the screen (you can also focus the capture area if needed)
    screenshot = pyautogui.screenshot()
    screenshot.save(rf"..\screenshot_{tab_name}.png")  # Save the screenshot to file
    time.sleep(0.6)
    # Load the image
    image_path = rf"..\screenshot_{tab_name}.png"  # Path to the screenshot
    image = cv2.imread(image_path)

    # Load the list of words from a file (one word/phrase per line)
    words_file = prt_file_path
    print(words_file)
    with open(words_file, 'r') as f:
        search_words = [line.strip() for line in f]

    # Perform OCR to extract text and bounding box information
    try:
        # Perform OCR to extract text and bounding box information
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        logging.debug("OCR Text: %s", data['text'])
    except Exception as e:
        logging.error("Error during OCR processing: %s", e)

    print(data['text'])

    with open(r"..\prt_det.txt", "w") as pfile:
        pfile.write(str(data['text']))

    # Store the best matching sequence
    best_sequence = []
    best_coords = []
    total_words = len(search_words)
    half_total_words = total_words / 2

    # Iterate through recognized words
    for i in range(len(data['text'])):
        if data['text'][i].strip():  # Ensure the word is not empty
            current_sequence = []
            current_coords = []
            words_found = set()  # Keep track of found words to avoid repetition

            # Check the sequence from the current word
            for word in search_words:
                found = False
                for j in range(i, len(data['text'])):
                    if data['text'][j].strip():  # Ensure the next word is not empty
                        # Check for fuzzy matches with a threshold
                        if fuzz.ratio(word.lower(), data['text'][j].lower()) >= 80:  # Adjust threshold as needed
                            # Break if the word is already in the sequence
                            if word in words_found:
                                break
                            current_sequence.append(word)
                            current_coords.append((data['left'][j], data['top'][j], data['width'][j], data['height'][j]))
                            words_found.add(word)
                            found = True
                            break

                if not found:
                    break  # Stop looking for the next words if the current word isn't found

            # Update the best sequence if it contains more than 50% of the total words and is longer than the previous best
            if len(current_sequence) > len(best_sequence) and len(current_sequence) > half_total_words:
                best_sequence = current_sequence
                best_coords = current_coords

    # If a best sequence was found, click on the middle word's coordinates
    if best_sequence:
        print(f"Best sequence found: {best_sequence} with length: {len(best_sequence)}")

        # Calculate the index of the middle word
        mid_index = len(best_sequence) // 2
        mid_coord = best_coords[mid_index]

        # Click on the middle word's coordinates
        center_x = mid_coord[0] + mid_coord[2] // 2  # Calculate the center x
        center_y = mid_coord[1] + mid_coord[3] // 2  # Calculate the center y
        
        time.sleep(1)
        click_element(*get_coordinates("outside", coordinates))
        
        time.sleep(0.2)
        # Simulate a mouse click at the center of the middle word's bounding box
        pyautogui.click(*get_coordinates(drpdwn, coordinates))  # This line seems hardcoded; consider updating it to dynamic click
        time.sleep(0.4)
        #pyautogui.click(center_x, center_y)
        pyautogui.click(mid_coord[0], mid_coord[1])
        time.sleep(0.2)
        print(f"Clicked at ({center_x}, {center_y})")
    else:
        print("Not enough words were found in the image.")
        print("Executing Manual Process!!!")
        if prt_name == "proPrt":
            messagebox.showinfo("Printer", "Please select your printer from the drop down and press next")
            keyboard.wait("ctrl+0")
        else:
            click_element(*get_coordinates("outside", coordinates))
            time.sleep(0.2)
            pyautogui.click(*get_coordinates(drpdwn, coordinates))
            time.sleep(0.2)
            click_element(*get_coordinates(prt_name, coordinates))

import os
import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar, OptionMenu

def get_checkpoint_file(script_name, job_id):
    """Generate a checkpoint file name based on script name and job ID."""
    return f"checkpoint_{script_name}_{job_id}.txt"

def save_checkpoint(step, script_name, job_id):
    """Save the current step to a dynamically named checkpoint file."""
    checkpoint_file = get_checkpoint_file(script_name, job_id)
    with open(checkpoint_file, 'w') as file:
        file.write(step)

def load_checkpoint(script_name, job_id):
    """Load the last completed step from a dynamically named checkpoint file."""
    checkpoint_file = get_checkpoint_file(script_name, job_id)
    try:
        with open(checkpoint_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def clear_checkpoint(script_name, job_id):
    """Clear the dynamically named checkpoint file."""
    checkpoint_file = get_checkpoint_file(script_name, job_id)
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

def get_all_checkpoints(script_name):
    """Return a list of all possible checkpoints."""
    if script_name == 'loadProjectV2':
        return [
            "start",
            "job_number_collected",
            "capslock_checked",
            "terminate_program_initiated",
            "browser_initialized",
            "login_completed",
            "search_fd_clicked",
            "search_btn_clicked",
            "search_result_selected",
            "data_extracted",
            "secad_started",
            "streamdeck_input_received",
            "project_saved",
            "fields_and_materials_filled",
            "dxf_imported",
            "final_step"
        ]
    elif script_name == 'SeAutoSalesV2':
        return [
                "start",
                "job_number_collected",
                "capslock_checked",
                "terminate_program_initiated",
                "moved_to_sales",
                "view_created",
                "printer_handled",
                "copies_printed",
                "pdf_saved",
                "pdf_uploaded",
                "moved_to_production"
        ]


def prompt_user_for_checkpoint_with_dropdown(script_name, job_id):
    """Display a dropdown menu for the user to select a checkpoint."""
    checkpoints = get_all_checkpoints(script_name)
    last_checkpoint = load_checkpoint(script_name, job_id)

    # Create a Tkinter window
    root = tk.Tk()
    #root.withdraw()
    root.title("Select Stage")
    root.geometry("400x200")

    selected_stage = StringVar()
    selected_stage.set(last_checkpoint if last_checkpoint else "start")  # Default value

    # Create a dropdown menu
    dropdown = OptionMenu(root, selected_stage, *checkpoints)
    dropdown.pack(pady=20)

    def confirm_selection():
        root.destroy()

    # Confirm button
    confirm_button = tk.Button(root, text="Confirm", command=confirm_selection)
    confirm_button.pack(pady=10)

    root.mainloop()

    return selected_stage.get()

state = {}  # Centralized state dictionary

def load_state(script_name, job_id):
    """
    Load the state from a file. If the file does not exist, initialize an empty state.
    """
    state_file_path = f"{script_name}_{job_id}_state.json"
    if not os.path.exists(state_file_path):
        print(f"State file {state_file_path} does not exist. Initializing empty state.")
        sys.stdout.flush()
        return {}
    with open(state_file_path, "r") as state_file:
        return json.load(state_file)

def save_state(script_name, job_id, state):
    """
    Save the current state to a file.
    """
    state_file_path = f"{script_name}_{job_id}_state.json"
    with open(state_file_path, "w") as state_file:
        json.dump(state, state_file, indent=4)
    print(f"State saved to {state_file_path}.")
    sys.stdout.flush()

def find_next_available_filename(base_path, prefix, extension):
    """
    Find the next available file name with incremental numbering.
    Example: job_id_1, job_id_2, ..., until a free name is found.
    """
    counter = 1
    while os.path.isfile(f"{base_path}\\{prefix}_{counter}.{extension}"):
        counter += 1
    return f"{prefix}_{counter}", counter

def handle_existing_job_id(job_id, base_path):
    """
    Handles existing job_id logic:
    - If user selects "Yes", move the current job_id.sep to job_id_bak, job_id_bak_1, etc.
    - If user selects "No", determine incremental names job_id_1, job_id_2, etc.
    """
    existing_file = os.path.join(base_path, f"{job_id}.sep")
    job_id_save = None  # Variable to hold the final name

    if os.path.isfile(existing_file):
        print(f"{existing_file} already exists.")
        sys.stdout.flush()

        # Prompt user for confirmation
        root = tk.Tk()
        root.withdraw()
        response_save_file = messagebox.askokcancel(
            "Confirmation",
            f"{existing_file} already exists!\n"
            f"Do you wish to move it as {job_id}_bak.sep?"
        )

        if response_save_file:  # User selected "Yes"
            # Handle _bak logic
            bak_file = os.path.join(base_path, f"{job_id}_bak.sep")
            if os.path.isfile(bak_file):
                # If _bak already exists, find the next sequential name
                bak_file_name, _ = find_next_available_filename(base_path, f"{job_id}_bak", "sep")
                bak_file = os.path.join(base_path, f"{bak_file_name}.sep")
                print(f"Backup file already exists. Moving to: {bak_file}")
            os.rename(existing_file, bak_file)
            print(f"File moved to: {bak_file}")
            sys.stdout.flush()

            # Set job_id_save to job_id.sep
            job_id_save = os.path.join(base_path, f"{job_id}.sep")

        else:  # User selected "No"
            # Determine incremental name
            increment_file_name, _ = find_next_available_filename(base_path, job_id, "sep")
            job_id_save = os.path.join(base_path, f"{increment_file_name}.sep")
            print(f"Set job_id_save to: {job_id_save}")
            sys.stdout.flush()

    else:
        # If no existing file, set job_id_save to original job_id
        print(f"No conflicts. Setting job_id_save to: {job_id}.sep")
        job_id_save = os.path.join(base_path, f"{job_id}.sep")

    return job_id_save