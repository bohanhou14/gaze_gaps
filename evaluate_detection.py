from datasets import load_from_disk
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Parse label lists from a text file")
    parser.add_argument("dataset")
    args = parser.parse_args()
    assert "human" in args.dataset, "The dataset name should contain 'human'"
    # Load the dataset from disk
    dataset = load_from_disk(args.dataset)
    human_labels = dataset["human_labels"]
    labels = dataset["labels"]
    inaccuracy = 0
    total = 0
    for i, (human_label, label) in enumerate(zip(human_labels, labels)):
        label_set = set(label)
        human_label_set = set(human_label)
        total += 1 if len(human_label_set) > 0 else 0
        inaccuracy += 1 if len(human_label_set) > 0 and label_set != human_label_set else 0
        if len(human_label_set) > 0 and label_set != human_label_set:
            print(f"Example {i+1}:")
            print(f"Human label: {human_label}")
            print(f"Model label: {label}")
            print()
    print(f"Total accuracy: {total - inaccuracy}/{total}, or {(1 - (inaccuracy/total))*100:.2f}%")


    