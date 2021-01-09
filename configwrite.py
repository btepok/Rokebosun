import os.path

def is_exist(user_id):
    if os.path.isfile (f"users/{user_id}.ini"):
        return True
    else:
        return False
