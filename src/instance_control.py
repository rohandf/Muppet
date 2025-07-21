'''
Instace Control Module

This module:
    this module is used to handle every instance the user makes.

-DOURAN
'''

class Config:
    def __init__(self):
        self.userinput_contentpath = r""
        self.userinput_dmxconvert = r""
        self.userinput_meshscale = 1

def handle_set_command(config_instance, var_name, value):
    # Look for attributes that contain "user" and match the input var
    matched_vars = [attr for attr in dir(config_instance)
                    if "user" in attr.lower() and not attr.startswith("__")]

    if var_name not in matched_vars:
        print(f"'{var_name}' is not a recognized user variable.")
        print("Available user-settable variables:")
        for var in matched_vars:
            print(f" - {var}")
        return

    setattr(config_instance, var_name, value)
    print(f"Set {var_name} = {value}")