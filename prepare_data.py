import os
import shutil
import re
import pandas as pd
"""
the return value of all the functions in this file is a list of strings,
each of those string represents a sentence
DO NOT TOUCH THE REGEX SUB in this file,
I DO NOT UNDERSTAND MOST OF IT, the files will explode if you do.
"""
def prep_parade() -> list:
    raw_data = []
    file_path = "data/PARADE_dataset/parade.txt"

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                row = [item.strip() for item in line.split('\t')]
                raw_data.append(row)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        data = [row[3:] for row in raw_data]
        data.pop(0)
        sentences = [item for sublist in data for item in sublist]
    except Exception as e:
        print("An error occured with the list")

    return sentences

def prep_bbc() -> list:
    file_path = "data/bbc.csv"
    sentences = []

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        for index, row in df.iterrows():
            text_data = row["text"]
            # Replace backslashes with single quotes, handling escaped newlines specifically
            text_data = re.sub(r"\\(?!n)", "'", text_data)
            # Replace escaped newlines with actual newlines
            text_data =  re.sub(r"\\n", "\n", text_data)
            # Replace newlines with ". "
            text_data = re.sub(r"\n", ". ", text_data)
            # Replace multiple dots with a single dot followed by a space
            text_data = re.sub(r"\.{2,}", ". ", text_data)
            sentences.append(text_data)
    except Exception as e:
        print(f"Error Index: {index}")
        print(f"Error Value: {row}")
        print(f"An error occurred: {e}")

    return sentences

def prep_textbook() -> list:
    file_path = "data/textbooks.csv"
    sentences = []

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        for index, row in df.iterrows():
            text_data = row["textbook"]

            # 1. Remove markdown headings (e.g., # Heading, ## Subheading)
            # This should be done early to clean structural elements.
            text_data = re.sub(r"^#+\s*", "", text_data, flags=re.MULTILINE)

            # 2. Handle escaped characters (like \' to ' or \" to ")
            # This needs to be done *before* general backslash handling or newline processing.
            text_data = re.sub(r"\\([^\s\n])", r"\1", text_data) # Handles \' to ', \" to ", etc., excludes \n
            text_data = re.sub(r"\\n", "\n", text_data)          # Converts \\n to actual \n

            # 3. Remove bold markdown (**text**)
            text_data = re.sub(r"\*\*([^\*]+?)\*\*", r"\1", text_data)

            # 4. Handle newlines: replace one or more newlines with ". "
            text_data = re.sub(r"\n+", ". ", text_data)

            # 5. Fix specific unwanted patterns created by previous steps
            text_data = re.sub(r":\. ", ": ", text_data) # Replace ":. " with ": "

            # 6. Consolidate multiple dots and clean up spacing
            text_data = re.sub(r"\.{2,}", ". ", text_data) # Replace multiple dots with a single dot followed by a space
            text_data = re.sub(r"\s+", " ", text_data).strip() # Consolidate multiple spaces and strip leading/trailing

            sentences.append(text_data)
    except Exception as e:
        print(f"Error Index: {index}")
        print(f"Error Value: {row}")
        print(f"An error occurred: {e}")

    return sentences