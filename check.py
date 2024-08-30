import os
from datasets import load_from_disk
import sys

if __name__ == "__main__":
    dir_path = "outputs"
    for ds_path in os.listdir(dir_path):
        full_ds_path = os.path.join(dir_path, ds_path)
        ds = load_from_disk(full_ds_path)
        for i in range(len(ds)):
            with open(os.path.join(full_ds_path, f"example-{i+1}.txt"), "w") as sys.stdout:
                print(f"Example {i+1}:")
                print(f"User:\n\n{ds['prompt'][i]}\n")
                print("Assistant:\n\n" + '{"label": ' + str(ds['labels'][i]) + ', "explanation": ' + '"' + str(ds['explanations'][i]) + '"}\n')
                print("-"*100)
                # print("User:\n\n" + '{"label": ' + '"' + str(ds['human_labels'][i]) + '"}')
                
            # breakpoint()