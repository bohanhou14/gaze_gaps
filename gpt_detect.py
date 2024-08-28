from openai import OpenAI, AzureOpenAI
import os
import json
from argparse import ArgumentParser
import re
from tqdm import tqdm
from prompts import DETECT_SYSTEM_PROMPT
from datasets import Dataset

def init_openai_client(port=None, personal=False):
    openai_api_key = os.getenv("OPENAI_API_KEY") if not personal else os.getenv("OPENAI_API_KEY_PERSONAL")
    if port != None:
        openai_api_base = f"http://0.0.0.0:{port}/v1"
        return OpenAI(
            base_url=openai_api_base,
            api_key=openai_api_key
        )
    return OpenAI(
        api_key=openai_api_key
    )

def init_azure_openai_client():
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    return AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version="2024-05-13",
        azure_endpoint=azure_openai_endpoint
    )

def request_GPT(client, prompt, max_retries = 10, max_tokens=300, model="gpt-4o", system_prompt=None):
    num_try = 0
    # print(prompt)
    while num_try < max_retries:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{prompt}"}
                ],
                max_tokens=max_tokens
            )
            if type(prompt) == list:
                return [r.text for r in response.choices]
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            num_try += 1

# def fix_json_string(input_str):
#     # Step 1: Identify keys and wrap them in quotes if they are not already
#     input_str = re.sub(r'(\w+):', r'"\1":', input_str)
    
#     # Step 2: Identify non-quoted string values and wrap them in quotes
#     input_str = re.sub(r'("[^"]+":\s*)([^,\}\n]+)', r'\1"\2"', input_str)

#     # Using a dictionary to temporarily store the key-value pairs
#     escaped = input_str.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
#     breakpoint()
#     return escaped

if __name__ == "__main__":
    dir_path = "prompts/"
    parser = ArgumentParser(description="Detect gaps in the generated text")
    parser.add_argument("--total_k", type=int, default=200, help="Total number of prompts to process")
    args = parser.parse_args()
    k = args.total_k

    client = init_openai_client(personal=False)
    # client = init_azure_openai_client()
    ids = []
    prompts = []
    detection_results = []
    exps = []
    file_list=os.listdir(dir_path)
    
    for filename in tqdm(file_list[:k], desc="Detecting errors", total=k):
        with open(os.path.join(dir_path, filename), "r") as f:
            prompt = f.read()
            response = ""
            while response == "":
                response = request_GPT(client, prompt, model="gpt-4o", system_prompt=DETECT_SYSTEM_PROMPT, max_tokens=400)
                try:
                    parsed_data = json.loads(response)
                    assert "label" in parsed_data and "explanation" in parsed_data, Exception("Failure to parse or missing fields in JSON")
                    ids.append(filename.split(".")[0].replace("test-", ""))
                    prompts.append(prompt)
                    if type(parsed_data['label']) == list:
                        detection_results.append(parsed_data['label'])
                    else:
                        detection_results.append(list(parsed_data['label']))
                    exps.append(str(parsed_data['explanation']))
                except Exception as e:
                    print(f"Failed to parse JSON: {e}")
                    response = ""

    dataset = Dataset.from_dict({
        "data_id": ids,
        "prompt": prompts,
        "labels": detection_results,
        "explanations": exps
    })
    dataset.save_to_disk(f"gpt-4o-gap-detection-top_k={k}")


    
    
    