import sys
import os
import xlrd
import csv
import pickle

PROJECT_PARENT_PATH = "C:\\Users\\hosse\\Desktop\\MIR\\MIRRepo"
ENGLISH_FILE_PATH = os.path.join(PROJECT_PARENT_PATH, "English.csv")
PERSIAN_FILE_PATH = os.path.join(PROJECT_PARENT_PATH, "Persian.xml")


def load_english_file():
    titles_and_text = []
    with open(ENGLISH_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_cnt = 0
        for row in csv_reader:
            if line_cnt == 0:
                # print("name of columns:")
                # print(row[0], " ", row[1])
                pass
            else:
                # print(row[0], row[1])
                titles_and_text.append((row[0], row[1]))
            line_cnt += 1
    return titles_and_text


def load_persian_file():
    pass


def save_object_to_file(obj, filename):
    with open(os.path.join(PROJECT_PARENT_PATH, filename), '+wb') as file:
        pickle.dump(obj, file)
