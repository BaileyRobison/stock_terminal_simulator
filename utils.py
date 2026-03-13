"""
Utility functions
"""
import yaml
import os


def read_yaml(yaml_file):
    """
    Read a yaml file given the name of the file
    """
    # path to yaml file
    current_dir = os.path.dirname(__file__)
    path = current_dir+'/config/'+yaml_file+'.yaml'
    
    # open yaml file
    with open(path, encoding= 'utf-8') as f:
        yaml_content = yaml.safe_load(f)
        
    return yaml_content


def format_num_display(num, digits=0):
    """
    Format a number to readable text
    1200 -> 1.2k
    12000 -> 12k
    120000 -> 120k
    1200000 -> 1.2M
    """            
    if num >= 1e6: # divide by million or thousand
        num /= 1e6
        suffix = 'M'
    elif num >= 1e3:
        num /= 1e3
        suffix = 'k'
    else:
        suffix = ''
    
    if num >= 10: # round
        num = round(num, digits)
    else: # keep decimal if only 1s place
        num = round(num, digits+1)
        
    if num.is_integer(): # convert to int if needed
        num = int(num)
        
    if digits > 0: # ensure correct number of digits if given
        num = "{:.2f}".format(num)
    else:
        num = str(num)
    
    return num+suffix
