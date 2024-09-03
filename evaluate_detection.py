from datasets import load_from_disk
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import re
import os

def extract_integers_from_path(path):
    # Use regex to find all sequences of digits in the path
    integers = re.findall(r'\d+', path)
    
    # Convert the extracted digit sequences to integers
    integers = [int(num) for num in integers]
    assert len(integers) > 0, "No integers found in the path"

    return integers[-1]

def add_annotations(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', 
                ha='center', va='bottom', fontsize=14, color='black')

if __name__ == "__main__":
    parser = ArgumentParser(description="Parse label lists from a text file")
    parser.add_argument("dataset_dir", help="directory containing the datasets to evaluate")
    parser.add_argument("--model", type=str, help="Model to use for detection, for naming the plot", default="gpt-4o")
    args = parser.parse_args()

    dataset_paths = []
    file_list = os.listdir(args.dataset_dir)
    for filename in file_list:
        if "human" in filename:
            dataset_paths.append(os.path.join(args.dataset_dir, filename))

    # sort dataset_path by int in descending order
    dataset_paths = sorted(dataset_paths, key=extract_integers_from_path)[::-1]
    exs, ps, rs, f1s = [], [], [], []
    
    for ds_path in dataset_paths:
        dataset = load_from_disk(ds_path)
        human_labels = dataset["human_labels"]
        labels = dataset["labels"]
        exact_match_total, exact_match_inaccuracy = 0, 0
        p_total, r_total, intersections = 0, 0, 0
        for i, (human_label, label) in enumerate(zip(human_labels, labels)):
            if len(human_label) == 0:
                continue
            label_set = set(label)
            human_label_set = set(human_label)
            exact_match_total += 1 
            exact_match_inaccuracy += 1 if label_set != human_label_set else 0
            intersection = label_set.intersection(human_label_set)
            intersections += len(intersection)
            p_total += len(label_set) 
            r_total += len(human_label_set) 

        exact_match_accuracy = 1 - exact_match_inaccuracy / exact_match_total
        exs.append(exact_match_accuracy)
        p = intersections / p_total
        ps.append(p)
        r = intersections / r_total
        rs.append(r)
        f1 = 2 * p * r / (p + r)
        f1s.append(f1)
    
    shots_nums = [extract_integers_from_path(dataset_path) for dataset_path in dataset_paths]
    
    plot_x = ["#=" + str(num) for num in shots_nums]

    plt.rcParams.update({
        'font.size': 16,          # Default font size for all text
        'axes.titlesize': 20,     # Font size for axes titles
        'axes.labelsize': 20,     # Font size for axes labels
        'xtick.labelsize': 15,    # Font size for x-axis tick labels
        'ytick.labelsize': 14,    # Font size for y-axis tick labels
        'legend.fontsize': 12,    # Font size for legend text
        'figure.titlesize': 24    # Font size for figure title
    })
    fig, axes = plt.subplots(2,2, figsize=(10, 8))
    bars = axes[0, 0].bar(plot_x, exs, color='#008080', label='Exact Match Accuracy')
    axes[0,0].set_ylabel("Exact Match Accuracy")
    axes[0,0].set_ylim(0, 1)
    axes[0,0].set_title("Exact Match vs # of Shots")
    add_annotations(axes[0, 0], bars)

    bars = axes[0,1].bar(plot_x, ps, color='#FF7F50', label='Precision')
    axes[0,1].set_ylabel("Precision")
    axes[0,1].set_ylim(0, 1)
    axes[0,1].set_title("Precision vs # of Shots")
    add_annotations(axes[0, 1], bars)

    bars = axes[1,0].bar(plot_x, rs, color='#FFD700', label='Recall')
    axes[1,0].set_ylabel("Recall")
    axes[1,0].set_ylim(0, 1)
    axes[1,0].set_title("Recall vs # of Shots")
    add_annotations(axes[1, 0], bars)

    bars = axes[1,1].bar(plot_x, f1s, color='#4169E1', label='F1 Score')
    axes[1,1].set_ylabel("F1 Score")
    axes[1,1].set_ylim(0, 1)
    axes[1,1].set_title("F1 Score vs # of Shots")
    add_annotations(axes[1, 1], bars)
    
    plt.tight_layout()
    plt.savefig(f"{args.model}-metrics.png")


    