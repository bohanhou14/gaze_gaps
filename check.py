import os
from datasets import load_from_disk
import sys
if __name__ == "__main__":
    ds = load_from_disk("gpt-4o-gap-detection-top_k=200_human")
    for i in range(20):
        if set(ds['human_labels'][i]) != set(ds['labels'][i]):
            with open(f"temp-{i+1}.txt", "w") as sys.stdout:
                print(f"Id: {ds['data_id'][i]}")
                print(f"User:\n\n{ds['prompt'][i]}\n")
                print("Assistant:\n\n" + "{label: " + str(ds['labels'][i]) + ", explanation: " + str(ds['explanations'][i]) + "}\n")
                print("User:\n\n" + "{label: " + str(ds['human_labels'][i]) + "}")
            # breakpoint()