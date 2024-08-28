Pipeline to generate the detection datasets and run the detection experiments

1. Generate prompts for the GPT4o-based detector:
```
python prompt_loader.py --k 100
```
This generates 100 prompts per LLM (i.e. 100 for GPT4o generation and 100 for llama3 generation) 

2. Run the GPT4o detector via OpenAI API
```
python gpt_detect.py --total_k 200
```
This runs detector over `total_k` number of instances (i.e. 100 + 100 = 200 instances in total) and outputs a detection dataset (in HuggingFace format)

3. Parse human annotations and add the labels to the detection dataset
```
python parse_human_annotations.py --detect_dataset DATASET_PATH
```
This outputs a DETECTION_HUMAN dataset with parsed human labels

4. Evaluate detection accuracy
```
python evaluate_detection.py DETECTION_HUMAN_DATASET_PATH
```
where DETECTION_HUMAN_DATASET_PATH is from step 3.



