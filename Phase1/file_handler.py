import sys
import os
import xlrd
import csv
import pickle
import xml.etree.ElementTree as ET

PROJECT_PARENT_PATH = ""
PERSIAN_FILE_PATH = os.path.join(PROJECT_PARENT_PATH, "Persian.xml")


def load_english_file(filename: str = "English.csv"):
    titles_and_text = []
    path = os.path.join(PROJECT_PARENT_PATH, filename)
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_cnt = 0
        for row in csv_reader:
            if line_cnt == 0:
                # print("name of columns:")
                # print(row[0], " ", row[1])
                pass
            else:
                # print(row[0], row[1])
                if filename == "English.csv":
                    titles_and_text.append((row[0], row[1]))
                else:
                    titles_and_text.append((row[1], row[2]))
            line_cnt += 1
            #print(line_cnt)
    return titles_and_text


def load_persian_file():
    tree = ET.parse(PERSIAN_FILE_PATH)
    root = tree.getroot()
    title = []
    for x in root:
        title.append(x.find("{http://www.mediawiki.org/xml/export-0.10/}title").text)
    text = []
    for x in root:
        for y in x.getchildren():
            if y.tag == "{http://www.mediawiki.org/xml/export-0.10/}revision":
                text.append(y.find("{http://www.mediawiki.org/xml/export-0.10/}text").text)
    titles_and_texts = []
    for i in range(len(title)):
        titles_and_texts.append((title[i], text[i]))
    return titles_and_texts


def save_object_to_file(obj, filename):
    with open(os.path.join(PROJECT_PARENT_PATH, filename), '+wb') as file:
        pickle.dump(obj, file)
