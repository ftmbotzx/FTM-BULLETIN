##### ftmadmin.py (Admin Management) #####

# Fᴛᴍ Bᴜʟʟᴇᴛɪɴ Bot Admin Management
# Developed by @ftmdeveloperz - All Rights Reserved
# Credits: @ftmdeveloperz | @ftmdeveloperz | @ftmdeveloperz

import json

# Load or initialize admin data
try:
    with open("admins.json", "r") as f:
        admins = json.load(f)
except FileNotFoundError:
    admins = {"owner": str(OWNER_ID), "admins": []}

# Function to check if a user is the owner
def is_owner(user_id):
    return str(user_id) == admins["owner"]

# Function to check if a user is an admin
def is_admin(user_id):
    return str(user_id) in admins["admins"]

# Function to add an admin
def add_admin(user_id):
    if str(user_id) not in admins["admins"]:
        admins["admins"].append(str(user_id))
        save_admins()
        return True
    return False

# Function to remove an admin
def remove_admin(user_id):
    if str(user_id) in admins["admins"]:
        admins["admins"].remove(str(user_id))
        save_admins()
        return True
    return False

# Save admin data
def save_admins():
    with open("admins.json", "w") as f:
        json.dump(admins, f, indent=4)

# Function to get all admins
def get_admins():
    return admins["admins"]
