import re
import os
import argparse
from datasets import load_from_disk, Dataset

def parse_labels(text):
    # Define regex pattern to match "Label:" followed by one or more integers, possibly separated by commas
    pattern = r"\*\*Label:\*\*\s*([\d\s,]+)"
    
    # Find all matches for the pattern in the text
    matches = re.findall(pattern, text)
    
    # Parse and collect all label values as a list of lists of integers
    parsed_labels = []
    for match in matches:
        # Split the matched string by commas to get individual numbers
        numbers_str = match
        
        # Ensure that only valid integers are captured (strip whitespace and check if digit)
        numbers = [num.strip() for num in numbers_str.split(',') if num.strip().isdigit()]
        
        # Convert each valid string number to an integer
        integers_list = list(map(int, numbers))
        parsed_labels.append(integers_list)
    
    return parsed_labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse label lists from a text file")
    parser.add_argument("--detect_dataset")
    args = parser.parse_args()

    # parse human annotations
    path = "train_examples"
    gpt_4o_labels = []
    gpt_4o_ids = []
    llama3_labels = []
    llama3_ids = []
    file_list = os.listdir(path)
    sorted_file_list = sorted(file_list, key=lambda x: int(x.split('-')[1].split('.')[0]))
    for idx, filename in enumerate(sorted_file_list):
        with open(os.path.join(path, filename), "r") as f:
            text = f.read()
            text.replace("\\n", "")
            parsed_lists = parse_labels(text)
            if len(parsed_lists) > 0:
                gpt_4o_labels.append(parsed_lists[0])
                gpt_4o_ids.append(f"gpt4o-{idx+1}")
            if len(parsed_lists) > 1:
                llama3_labels.append(parsed_lists[1])
                llama3_ids.append(f"llama3-{idx+1}")
    if args.detect_dataset:
        dataset = load_from_disk(args.detect_dataset)
        ids = dataset["data_id"]
        prompt = dataset["prompt"]
        labels = dataset["labels"]
        explanations = dataset["explanations"]
        human_labels = []
        for idx, data_id in enumerate(ids):
            if data_id in gpt_4o_ids:
                human_labels.append(gpt_4o_labels[gpt_4o_ids.index(data_id)])
            elif data_id in llama3_ids:
                human_labels.append(llama3_labels[llama3_ids.index(data_id)])
            else:
                human_labels.append([])
            
        data = {
            "data_id": ids,
            "prompt": prompt,
            "labels": labels,
            "explanations": explanations,
            "human_labels": human_labels
        }
        dataset = Dataset.from_dict(data)
        dataset.save_to_disk(args.detect_dataset + "_human")