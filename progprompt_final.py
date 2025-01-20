import argparse
import os
import os.path as osp
import random
import json
import time

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


# Load model
def load_llama_model(local_dir="../llama-2-7b-hf-model", device="cuda" if torch.cuda.is_available() else "cpu"):
    tokenizer = AutoTokenizer.from_pretrained(local_dir)
    model = AutoModelForCausalLM.from_pretrained(local_dir, device_map="auto", torch_dtype=torch.float16)
    return tokenizer, model, device


# Plan generation function
def generate_plan(prompt, tokenizer, model, device):
    try:
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        # Run model
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=600,
            temperature=0.7,
            do_sample=True,
        )
        # Decode output
        plan = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(plan)
        return plan
    except Exception as e:
        print(f"Error generating plan: {e}")
        return ""


def planner_executer(args):
    # Load model and tokenizer
    tokenizer, model, device = load_llama_model(local_dir=args.llama_model)

    # Prompt setup
    prompt = "Available actions: turnright, turnleft, walkforward, grab <obj>, put <obj>, open <obj>, close <obj>"
    prompt += "\n\nobjects = ['apple', 'chair', 'door', 'table']"  # Replace with dynamic object listing if needed

    # Load train examples
    with open(f"{args.progprompt_path}/data/pythonic_plans/train_complete_plan_set.json", 'r') as f:
        prompt_egs = json.load(f)

    if args.prompt_task_examples == "default":
        default_examples = ["wash_mug", "put_apple_in_fridge"]
        for example in default_examples[:args.prompt_num_examples]:
            prompt += f"\n\nExample:\n{prompt_egs[example]}"

    # Test task setup
    test_tasks = []
    with open(f"{args.progprompt_path}/data/{args.test_set}/file1_annotated2.json", 'r') as f:
        test_tasks = [json.loads(line)["task"] for line in f if line.strip()]

    # Generate plans
    gen_plans = []
    for task in test_tasks:
        print(f"Generating plan for: {task}")
        task_prompt = f"Task: {task}\nPlan:\n"
        full_prompt = prompt + "\n\n" + task_prompt
        plan = generate_plan(full_prompt, tokenizer, model, device)
        gen_plans.append(plan)

    # Save generated plans
    results_dir = f"{args.progprompt_path}/results/"
    os.makedirs(results_dir, exist_ok=True)
    log_filename = f"{args.expt_name}_plans.json"
    with open(osp.join(results_dir, log_filename), 'w') as f:
        json.dump(dict(zip(test_tasks, gen_plans)), f)

    print(f"Plans saved to {log_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--progprompt-path", type=str, default="/home/seojin/Desktop/kwon/progprompt-vh")
    parser.add_argument("--expt-name", type=str, default="my_experiment")

    parser.add_argument("--llama-model", type=str, default="meta-llama/Llama-2-7b-hf")
    parser.add_argument("--test-set", type=str, default="test_unseen", choices=['test_unseen', 'test_seen'])
    parser.add_argument("--prompt-task-examples", type=str, default="default", choices=['default', 'random'])
    parser.add_argument("--prompt-num-examples", type=int, default=2, choices=range(1, 5))

    args = parser.parse_args()
    planner_executer(args=args)
