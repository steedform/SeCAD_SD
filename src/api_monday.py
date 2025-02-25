'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without   
modification, are not permitted provided that the code retains the 
above copyright notice.
'''

import requests

# Monday API Key
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ0OTMyNTEwNCwiYWFpIjoxMSwidWlkIjozMTMwMzQwOSwiaWFkIjoiMjAyNC0xMi0xN1QyMDo1MTozMy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTMwMjk2MiwicmduIjoidXNlMSJ9.WiUmqwlnkXMNAbv6IlJNkz_0DMEx1JsUonT2qmDb4GY"

# Monday API Endpoint
url = "https://api.monday.com/v2"

# Test API Connection
def test_api_connection():
    query = {"query": "{ me { id name } }"}
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        print("API Connection Successful!")
        print("Response:", response.json())
    else:
        print(f"API Connection Failed: {response.status_code} {response.text}")

# Check for Workspace Existence
def check_workspace(workspace_name):
    query = {
        "query": f"""
            query {{
                workspaces (kind: open) {{
                    id
                    name
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        workspaces = response.json().get("data", {}).get("workspaces", [])
        for workspace in workspaces:
            if workspace["name"] == workspace_name:
                print(f"Workspace '{workspace_name}' exists with ID: {workspace['id']}")
                return workspace['id']
        print(f"Workspace '{workspace_name}' not found.")
        return None
    else:
        print(f"Failed to fetch workspaces: {response.status_code} {response.text}")
        return None

# List Boards in Workspace
def list_boards_in_workspace():
    query = {
        "query": """
            query {
                boards {
                    id
                    name
                    board_folder_id
                }
            }
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        boards = response.json().get("data", {}).get("boards", [])
        print("Boards:")
        for board in boards:
            print(f"- {board['name']} (ID: {board['id']}, Folder ID: {board['board_folder_id']})")
    else:
        print(f"Failed to fetch boards: {response.status_code} {response.text}")

# Get Board ID by Name
def get_board_id_by_name(workspace_id, board_name, progress):
    """
    Fetch the board ID based on the board name within a workspace.
    Args:
        workspace_id (int): The workspace ID to search.
        board_name (str): The name of the board to find.
        progress (ProgressWindow): Progress window for displaying logs.
    Returns:
        int: Board ID if found, None otherwise.
    """
    query = {
        "query": f"""
            query {{
                boards (workspace_ids: [{workspace_id}]) {{
                    id
                    name
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)

    if response.status_code == 200:
        boards = response.json().get("data", {}).get("boards", [])
        for board in boards:
            if board['name'] == board_name:
                progress.update_message(f"Board '{board_name}' found with ID: {board['id']}")
                return board['id']
        progress.update_message(f"Board '{board_name}' not found in Workspace.")
        return None
    else:
        progress.update_message(f"Failed to fetch boards: {response.status_code} {response.text}")
        return None


# List Content in V2 Production Schedule A3
def list_content_in_board(board_id):
    query = {
        "query": f"""
            query {{
                boards (ids: [{board_id}]) {{
                    name
                    items_page (limit: 50) {{
                        items {{
                            id
                            name
                            column_values {{
                                id
                                value
                            }}
                        }}
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        board_data = response.json().get("data", {}).get("boards", [])[0]
        print(f"\nContent in Board: {board_data['name']}")
        for item in board_data.get("items_page", {}).get("items", []):
            print(f"  Item: {item['name']} (ID: {item['id']})")
            for column in item.get("column_values", []):
                print(f"    Column ID: {column['id']}, Value: {column['value']}")
    else:
        print(f"Failed to fetch content: {response.status_code} {response.text}")

# List Group Names in Board
def list_groups_in_board(board_id):
    query = {
        "query": f"""
            query {{
                boards (ids: [{board_id}]) {{
                    name
                    groups {{
                        id
                        title
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        board_data = response.json().get("data", {}).get("boards", [])[0]
        print(f"\nGroups in Board: {board_data['name']}")
        for group in board_data.get("groups", []):
            print(f"  Group: {group['title']} (ID: {group['id']})")
    else:
        print(f"Failed to fetch groups: {response.status_code} {response.text}")

# List Column Headers and Data for Each Group in Board
def list_columns_and_group_data(board_id):
    query = {
        "query": f"""
            query {{
                boards (ids: [{board_id}]) {{
                    name
                    groups {{
                        id
                        title
                    }}
                    columns {{
                        id
                        title
                    }}
                    items_page (limit: 50) {{
                        items {{
                            group {{ id }}
                            column_values {{
                                id
                                value
                            }}
                        }}
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        board_data = response.json().get("data", {}).get("boards", [])[0]
        print(f"\nColumns in Board: {board_data['name']}")
        for column in board_data.get("columns", []):
            print(f"  Column: {column['title']} (ID: {column['id']})")

        # Commented-out block for displaying data per group
        # for group in board_data.get("groups", []):
        #     print(f"\nData for Group: {group['title']}")
        #     for item in board_data.get("items_page", {}).get("items", []):
        #         if item.get("group", {}).get("id") == group['id']:
        #             print("    Item:")
        #             for column_value in item.get("column_values", []):
        #                 print(f"      {column_value['id']}: {column_value['value']}")
    else:
        print(f"Failed to fetch columns and group data: {response.status_code} {response.text}")

# List Columns and Display Data Group-wise
def list_groupwise_data(board_id):
    query = {
        "query": f"""
            query {{
                boards (ids: [{board_id}]) {{
                    name
                    groups {{
                        id
                        title
                    }}
                    columns {{
                        id
                        title
                    }}
                    items_page (limit: 50) {{
                        items {{
                            name
                            group {{ id }}
                            column_values {{
                                id
                                value
                            }}
                        }}
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        board_data = response.json().get("data", {}).get("boards", [])[0]
        groups = {group['id']: group['title'] for group in board_data.get("groups", [])}
        columns = {col['id']: col['title'] for col in board_data.get("columns", [])}

        print(f"\nData Group-wise in Board: {board_data['name']}")
        for group_id, group_title in groups.items():
            print(f"\nGroup: {group_title} (ID: {group_id})")
            print("Columns:")
            for col_id, col_title in columns.items():
                print(f"  {col_title} (ID: {col_id})")

            # Uncomment below to display data
            # print("\nData:")
            # for item in board_data.get("items_page", {}).get("items", []):
            #     if item.get("group", {}).get("id") == group_id:
            #         print(f"  Item: {item['name']}")
            #         for column_value in item.get("column_values", []):
            #             if column_value['id'] in columns:
            #                 print(f"    {columns[column_value['id']]}: {column_value['value']}")
    else:
        print(f"Failed to fetch groupwise data: {response.status_code} {response.text}")

# Search for Item by Item Number with Pagination
def search_item_by_number(board_id, item_name):
    page_cursor = None
    while True:
        query = {
            "query": f"""
                query {{
                    boards (ids: [{board_id}]) {{
                        name
                        items_page (limit: 100, cursor: {f'\"{page_cursor}\"' if page_cursor else 'null'}) {{
                            cursor
                            items {{
                                id
                                name
                                group {{ id title }}
                                column_values {{
                                    id
                                    value
                                }}
                            }}
                        }}
                    }}
                }}
            """
        }
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=query)
        if response.status_code == 200:
            board_data = response.json().get("data", {}).get("boards", [])[0]
            board_name = board_data['name']
            items_page = board_data.get("items_page", {})

            print(f"\nSearching for Item: '{item_name}' in Board: {board_name} (ID: {board_id})")
            for item in items_page.get("items", []):
                if item['name'] == item_name:
                    print(f"\nItem '{item_name}' exists:")
                    print(f"- Workspace Name: Main workspace")
                    print(f"- Board Name: {board_name} (ID: {board_id})")
                    print(f"- Group Name: {item['group']['title']} (ID: {item['group']['id']})")
                    print(f"- Item ID: {item['id']}")
                    print("\nField Values:")
                    for column_value in item.get("column_values", []):
                        print(f"  {column_value['id']}: {column_value['value']}")
                    return item['id'], board_name, item['group']['title']

            # Check if there's a next page
            page_cursor = items_page.get("cursor")
            if not page_cursor:
                print("No more pages. Item not found.")
                break
        else:
            print(f"Failed to search for item: {response.status_code} {response.text}")
            break

    print(f"Item '{item_name}' not found in Board.")
    return None, None, None


# New Function: Get CAD Dropdown Value and Options
# Update CAD Dropdown Value
# calls search function comment it out if you call the serach function
def get_cad_dropdown_values(board_id, item_name):
    item_id, board_name, group_name = search_item_by_number(board_id, item_name)
    if not item_id:
        print(f"Item '{item_name}' not found. Cannot fetch CAD dropdown values.")
        return

    # Fetch column settings for dropdown options
    query_columns = {
        "query": f"""
            query {{
                boards (ids: [{board_id}]) {{
                    columns (ids: ["status_1"]) {{
                        title
                        settings_str
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response_columns = requests.post(url, headers=headers, json=query_columns)

    # Fetch the current value of the dropdown field
    query_value = {
        "query": f"""
            query {{
                items (ids: [{item_id}]) {{
                    column_values (ids: ["status_1"]) {{
                        text
                    }}
                }}
            }}
        """
    }
    response_value = requests.post(url, headers=headers, json=query_value)

    if response_columns.status_code == 200 and response_value.status_code == 200:
        column_data = response_columns.json().get("data", {}).get("boards", [])[0].get("columns", [])[0]
        dropdown_title = column_data['title']
        dropdown_options = column_data['settings_str']

        current_value = response_value.json().get("data", {}).get("items", [])[0].get("column_values", [])[0].get('text', "None")

        print(f"\nField: {dropdown_title} (Dropdown)")
        print(f"Current Value: {current_value}")
        print("Dropdown Options:")
        print(dropdown_options)
    else:
        print(f"Failed to fetch CAD dropdown values: {response_columns.status_code}, {response_value.status_code}")

# Update CAD Dropdown Value
# calls search function comment it out if you call the serach function
def update_cad_dropdown(board_id, item_name, new_label):
    # First, check if the item exists and retrieve the item ID
    item_id, board_name, group_name = search_item_by_number(board_id, item_name)
    
    if not item_id:
        print(f"Item '{item_name}' not found. Cannot update CAD dropdown value.")
        return
    
    # Update the CAD dropdown value using the item ID
    query = {
        "query": f"""
            mutation {{
                change_simple_column_value (board_id: {board_id}, item_id: {item_id}, column_id: "status_1", value: "{new_label}") {{
                    id
                    name
                }}
            }}
        """
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        print(f"\nSuccessfully updated CAD dropdown for Item '{item_name}' to '{new_label}'.")
    else:
        print(f"Failed to update CAD dropdown: {response.status_code} {response.text}")


'''  
# Test the API Connection
test_api_connection()

# Check if the workspace exists and list boards
workspace_name = "Main workspace"
workspace_id = check_workspace(workspace_name)
if workspace_id:
    list_boards_in_workspace()
    # List content in V2 Production Schedule A3
    #v2_production_schedule_a3_id = 2723302339
    board_name = "V2 Production Schedule A3"  # The name of the board
    board_id = get_board_id_by_name(workspace_id, board_name, progress)
    #list_content_in_board(board_id)
    
    # List groups in V2 Production Schedule A3
    list_groups_in_board(board_id)
    list_columns_and_group_data(board_id)
    list_groupwise_data(board_id)
    
    item_number = "ST9565"  # Replace with desired item name to search
    #search_item_by_number(board_id, item_number)
    
    #get_cad_dropdown_values(board_id, item_number)
    
    new_cad_value = "Done"  # Desired CAD dropdown value
    update_cad_dropdown(board_id, item_number, new_cad_value)
'''