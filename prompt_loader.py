'''
This file helps load the dataset and parse the relevant data into the prompt designed for the detection task.
'''
from datasets import load_dataset
from loader import parse_generations_dataset
from argparse import ArgumentParser

if __name__ == "__main__":
    dataset = load_dataset("jhu-clsp/CLERC", data_files={"data": f"generation/test.jsonl"})["data"]
    gpt4o_generations = parse_generations_dataset()
    llama3_generations = parse_generations_dataset("clerc_generations/prompt1/Meta-Llama-3-8B-Instruct/preds")
    parser = ArgumentParser(description="Load the dataset and generate prompts for the detection task")
    parser.add_argument("--k", type=int, default=100, help="Number of prompts per LLM to generate")
    args = parser.parse_args()
    k = args.k
    
    for idx in range(k):
        data = dataset[idx]
        docid = data["docid"]
        gold_text = data["gold_text"]
        prev_text = data["previous_text"]
        short_citations = data["short_citations"]
        citations = [cite[0] for cite in data["citations"]]
        gpt4o_generation = [gen["generation"] for gen in gpt4o_generations if gen["docid"] == docid]
        llama3_generation = [gen["generation"] for gen in llama3_generations if gen["docid"] == docid]
        if len(gpt4o_generation) == 0 or len(llama3_generation) == 0:
            continue

        prompt = '''Output a valid JSON object with the fields of {"label": (one or more integers from 0-3 indicating the gap categories), "explanation": a short explanation justifying the label.}. Do not output anything else such as 'json' or newline characters or redundant spaces. If you label a 3, please elaborate the explanation for it a bit more. Answer after output: '''
        
        with open(f"prompts/test-gpt4o-{idx+1}.txt", "w") as f:
            f.write("Generation:\n\n")
            f.write(gpt4o_generation[0] + "\n\n")
            f.write("citations needed to make: " + str(citations) + "\n\n")
            f.write("target_text: " + gold_text + "\n\n")
            for i, cite in enumerate(short_citations):
                f.write(f"reference_case_{i+1}: " + cite + "\n\n")
            f.write("previous_text: " + prev_text + "\n\n")
            f.write(prompt + "\n\n")
            f.write("output: ")
            f.close()
        
        with open(f"prompts/test-llama3-{idx+1}.txt", "w") as f:
            f.write("**Generation:**\n\n")
            f.write(llama3_generation[0] + "\n\n")
            f.write("citations needed to make: " + str(citations) + "\n\n")
            f.write("gold_text: " + gold_text + "\n\n")
            for i, cite in enumerate(short_citations):
                f.write(f"reference_case_{i+1}: " + cite + "\n\n")
            f.write("previous_text: " + prev_text + "\n\n")
            f.write(prompt + "\n\n")
            f.write("output: ")
            f.close()
        
            

            
    