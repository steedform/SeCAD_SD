'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without   
modification, are not permitted provided that the code retains the 
above copyright notice.
'''

from api_monday_tk import *
from defs import get_job_id, validate_license

def main_process(progress):
    test_api_connection(progress)
    workspace_name = "Main workspace"
    workspace_id = check_workspace(workspace_name, progress)

    if workspace_id:
        board_name = "V2 Production Schedule A3"  # Dynamic board name
        board_id = get_board_id_by_name(workspace_id, board_name, progress)
        
        if board_id:
            item_name = get_job_id(r"..\job_id.txt")
            print(item_name)
            new_cad_value = "Done"
            update_cad_dropdown(board_id, item_name, new_cad_value, progress)
        else:
            progress.update_message("Board not found. Exiting process.")
    else:
        progress.update_message("Workspace not found. Exiting process.")

    progress.update_message("Process Completed Successfully!")


# Run Tkinter Window with Thread
def run_main():
    root, progress_window = create_progress_window()
    process_thread = Thread(target=main_process, args=(progress_window,))
    process_thread.start()
    root.mainloop()

if __name__ == "__main__":
    validate_license()
    run_main()
