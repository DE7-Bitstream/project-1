import os

CSV_FOLDER_NAME = "csv"
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

CSV_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), CSV_FOLDER_NAME)
if not os.path.exists(CSV_DIR):
    os.mkdir(CSV_DIR)
