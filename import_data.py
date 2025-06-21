from datasets import load_dataset
import pandas as pd
import requests
import os
import shutil

def import_parade():
    repo_url = "https://github.com/heyunh2015/PARADE_dataset"
    data_file_name = "parade.txt"

    if not os.path.exists("data"):
        os.mkdir("data")

    os.chdir("data")

    if not os.path.exists("PARADE_dataset"):
        os.system(f"git clone {repo_url}")

    os.chdir("PARADE_dataset")
    files_to_delete = os.listdir()
    files_to_delete.pop(0)

    if os.path.exists("PARADE_test.txt"):
        os.rename("PARADE_test.txt", data_file_name)

    for file in files_to_delete:
        if os.path.exists(file) and file != data_file_name:
            os.remove(file)

    os.chdir("..")
    os.chdir("..")
    print("Loaded PARADE Dataset")
    
def import_bbc():
    ds = load_dataset("permutans/fineweb-bbc-news", name="CC-MAIN-2013-20", split="train", streaming=True)
    filtered = (row for row in ds if '/technology/' in row['url'])

    texts = [row['text'] for row in filtered]

    df = pd.DataFrame(texts, columns=["text"])
    df.to_csv("technology_articles_2013_20.csv", index=False)


def import_textbook(hf_key : str):
    dataset = load_dataset("nampdn-ai/tiny-textbooks")
    all_data = []
    for split in dataset:
        all_data.extend(dataset[split]['textbook'])

    df = pd.DataFrame(all_data, columns=["textbook"])

    df.to_csv("tiny_textbooks.csv", index=False)