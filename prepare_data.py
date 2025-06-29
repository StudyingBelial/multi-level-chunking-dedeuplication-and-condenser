import re
import pandas as pd
"""
the return value of all the functions in this file is a list of strings,
each of those string represents an entire chunk of document,
for the case of BBC it's an entire article sent,
this if for the purpose of benchmarking of how the system can still preserve the semantic meanings after all is processing is done
DO NOT TOUCH THE REGEX SUB in this file,
I DO NOT UNDERSTAND MOST OF IT, the files will explode if you do.
"""
def prep_parade() -> list:
    csv_file_path = "data/PARADE_dataset/parade.csv"

    try:
        df = pd.read_csv(csv_file_path)

        required_cols = ["Entity","Definition1","Definition2"]

        if not all (col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            print(f"Missing required columns in CSV: {missing_cols}")
            return

        df["Cleaned_defintion1"] = df["Definition1"].apply(lambda x : str(x).strip().replace("&quote;", '"').replace('""', '"').lstrip("- ").strip())
        df["Cleaned_defintion2"] = df["Definition2"].apply(lambda x : str(x).strip().replace("&quote;", '"').replace('""', '"').lstrip("- ").strip())
        df["Combined_Row_Definition"] = df.apply(lambda x : ". ".join(filter(None, [x["Cleaned_defintion1"], x["Cleaned_defintion2"]])), axis = 1)

        consolidated_data = df.groupby("Entity")["Combined_Row_Definition"].apply(lambda x: ". ".join(filter(None, x))).to_dict()

        sentences = list(consolidated_data.values())
        corrected_sentences = []
        for text_data in sentences:
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
            text_data = re.sub(r'\.{2,}\s*', '. ', text_data)
            text_data = re.sub(r"\s+", " ", text_data).strip() # Consolidate multiple spaces and strip leading/trailing

            corrected_sentences.append(text_data)
        return corrected_sentences
    except Exception as e:
        print(f"An Error occured: {e}")

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