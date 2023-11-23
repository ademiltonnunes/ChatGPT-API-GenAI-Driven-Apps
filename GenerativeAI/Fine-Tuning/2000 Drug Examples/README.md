# Fine-Tuning based on 2000 drug examples from an Excel file
## Overview
This product exemplifies fine-tuning of a basic LLM, chatGPT 3.5. In order to fine-tune our project, we used an excel file with several examples of remedies and the malady they treat.
I demonstrated how to transform Excel data into the expected fine-tune data format and tested examples. Please, read the pdf file CS589_week10_q1_19679_AdemiltonMarcelo_DaCruzNunes.pdf. It will have all steps taken to develop this project.

## Implementation Steps
## Step 1: Setting Environment

1. Create and activate the development environment:
   ```bash
   python3 -m venv venv
   . venv/bin/activate
   ```

2. Install Openai and set the Openai key:
   ```bash
   pip install openai==0.28
   export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
   ```
## Step 2: Analyze and Prepare Data

1. Install required library:
   ```bash
   pip install openai[datalib]
   ```

2. Analyze the data.json file:
   ```bash
   openai tools fine_tunes.prepare_data -f data.json
   ```

## Step 3: Fine-Tune the Model

1. Install necessary libraries:
   ```bash
   pip install pandas openpyxl openai==0.28
   ```

2. Fine-tune the model:
   ```bash
   openai api fine_tunes.create -t "data_prepared.jsonl" -m curie
   ```

## Step 4: List Fine-Tuned Models

List your fine-tuned models:
   ```bash
   openai api fine_tunes.list
   ```

## Step 5: Use the Fine-Tuned Model

1. Set the fine-tuned model in the environment variable:
   ```bash
   export FINE_TUNED_MODEL="<YOUR_FINE_TUNED_MODEL>"
   ```

2. Generate completions using the fine-tuned model:
   ```bash
   openai api completions.create -m $FINE_TUNED_MODEL -p "<YOUR_PROMPT>"
   ```

## Step 6: Analyze Fine-Tuned Model

List the fine-tuned model to get its job id:
   ```bash
   openai api fine_tunes.list
   ```

