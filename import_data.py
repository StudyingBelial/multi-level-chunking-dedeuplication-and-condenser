from datasets import load_dataset
from huggingface_hub import login
import pandas as pd
import csv
import os

def import_parade():
    # Repo to download from
    repo_url = "https://github.com/heyunh2015/PARADE_dataset"
    # Destination file name
    data_file_name = "parade.txt"

    if not os.path.exists("data"):
        os.mkdir("data")

    os.chdir("data")

    os.system(f"git clone {repo_url}")

    os.chdir("PARADE_dataset")
    files_to_delete = os.listdir()
    files_to_delete.pop(0)

    if os.path.exists("PARADE_test.txt"):
        os.rename("PARADE_test.txt", data_file_name)
        print(f"{data_file_name} exists. No Need to Clone Repo")

    for file in files_to_delete:
        if os.path.exists(file) and file != data_file_name:
            os.remove(file)

    os.chdir("..")
    os.chdir("..")

    csv_file_path = "data/PARADE_dataset/parade.csv"
    txt_file_path = "data/PARADE_dataset/parade.txt"

    try:
        with open(txt_file_path, "r", encoding="utf-8") as infile:
            with open(csv_file_path, "w", encoding="utf-8") as outfile:
                writer = csv.writer(outfile)
                for line in infile:
                    row = line.strip().split("\t")
                    writer.writerow(row)
    except FileNotFoundError:
        print(f"Error: The file {txt_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Loaded PARADE Dataset")
    
def import_bbc(hf_key : str):
    login(hf_key)

    if not os.path.exists("data"):
        os.mkdir("data")

    ds = load_dataset("permutans/fineweb-bbc-news", name="CC-MAIN-2013-20", split="train")
    filtered = (row for row in ds if '/technology/' in row['url'])

    texts = [row['text'] for row in filtered]

    df = pd.DataFrame(texts, columns=["text"])
    df.to_csv("data/bbc.csv", index=False)

def import_textbook(hf_key : str):
    login(hf_key)

    if not os.path.exists("data"):
        os.mkdir("data")

    dataset = load_dataset("nampdn-ai/tiny-textbooks")
    all_data = []
    for split in dataset:
        all_data.extend(dataset[split]['textbook'])

    df = pd.DataFrame(all_data, columns=["textbook"])

    df.to_csv("data/textbooks.csv", index=False)

#import_parade()
# import_bbc("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")
# import_textbook("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")