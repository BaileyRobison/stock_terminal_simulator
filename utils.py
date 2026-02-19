"""
Utility functions
"""
import yaml
import os


def read_yaml(yaml_file):
    # path to yaml file
    current_dir = os.path.dirname(__file__)
    path = current_dir+'/config/'+yaml_file+'.yaml'
    
    # open yaml file
    with open(path, encoding= 'utf-8') as f:
        yaml_content = yaml.safe_load(f)
        
    return yaml_content