import os
from pathlib import Path
import logging
from setuptools import find_packages, setup

# files needed to create the data science project
# 1. setup.py files
# use for building the python packages
# 2. requirements.txt files
# 3. Creating the src directory
# 4. Creating the __init__.py files in src directory

# files & directory need to be created
# 1. .github/workflow
# as
# 2. src directory
# 3. components directory
# __init__.py file
# data_ingestion.py file
# data_transformation.py file
# model_trainer.py file
# 4. pipeline directory
# train_pipeline.py file
# prediction_pipeline.py file
# __init__.py file
# logger.py file
# exception.py file
# utils.py file
# app.py
# templatest/index.html file
# static/css/main.css file
# static/js/main.js file
# Dockerfile
# main.py
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s:')

project_name = "general_project_structures"

list_of_files = [".github/workflow/.gitkeep",
                 f"src/__init__.py",
                 f"src/{project_name}/__init__.py",
                 f"src/{project_name}/components/__init__.py",
                 f"src/{project_name}/components/data_ingestion.py",
                 f"src/{project_name}/components/data_transformation.py",
                 f"src/{project_name}/components/model_trainer.py",
                 f"src/{project_name}/pipeline/__init__.py",
                 f"src/{project_name}/pipeline/train_pipeline.py",
                 f"src/{project_name}/pipeline/prediction_pipeline.py",
                 f"src/{project_name}/logger.py",
                 f"src/{project_name}/exceptions.py",
                 f"src/{project_name}/utils.py",
                 f"src/{project_name}/utils/__init__.py",
                 f"src/{project_name}/config/__init__.py",
                 f"src/{project_name}/config/configuration.py",
                 f"src/{project_name}/entity/__init__.py",
                 f"src/{project_name}/constants/__init__.py",
                 "main.py",
                 "app.py",
                 "templates/index.html",
                 "static/main.css",
                 "static/js/main.js",
                 "Dockerfile",
                 "requirements.txt",
                 "setup.py",
                 "research/train.ipynb",
                 "config/config.yaml",
                 "dvc.yaml",
                 "params.yaml",
                 "research/trials.ipynb", ]

for filepath in list_of_files:
    # gets the rigt format for the os the program is running on as windoes has backslash for seprating the path.
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating the directory:{filedir}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating the empty file:{filepath}")

    else:
        logging.info(f"File already exists:{filepath}")