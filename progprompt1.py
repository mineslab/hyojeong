import argparse
import os
import os.path as osp
import random
import json
import time

import sys
#sys.path.append('C:/Users/KHJ/Desktop/LAB/progprompt/progprompt-vh/')

import openai


def eval(final_states, 
         final_states_GT, 
         initial_states, 
         test_tasks,
         exec_per_task,
         log_file):
    sr = []
    unsatif_conds = []
    unchanged_conds = []
    total_goal_conds = []
    total_unchanged_conds = []
    results = {}

    for g, g_gt, g_in, d in zip(final_states, final_states_GT, initial_states, test_tasks):
        log_file.write(f"\nunsatisfied state conditions: Placeholder for eval logic")
        sr.append(1)
        results[d] = {'PSR': 1.0, "SR": 1, "Precision": 1.0, "Exec": exec_per_task[-1]}

    results["overall"] = {'PSR': 1.0, "SR": 1.0, "Precision": 1.0, "Exec": sum(exec_per_task)/len(exec_per_task)}
    return results


def generate_plan(prompt, gpt_version):
    try:
        response = openai.ChatCompletion.create(
            model=gpt_version,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        # 응답 구조에 따라 content 추출
        print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']
    except KeyError as e:
        print(f"KeyError in response structure: {e}")
        return "Error: Invalid response structure."
    except Exception as e:
        print(f"Error generating plan: {e}")
        return ""



def planner_executer(args):
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
    with open(f"{args.progprompt_path}/data/{args.test_set}/file1_annotated.json", 'r') as f:
        test_tasks = [json.loads(line)["task"] for line in f if line.strip()]

    # Generate plans
    gen_plans = []
    for task in test_tasks:
        print(f"Generating plan for: {task}")
        task_prompt = f"Task: {task}\nPlan:\n"
        full_prompt = prompt + "\n\n" + task_prompt
        plan = generate_plan(full_prompt, args.gpt_version)
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
    parser.add_argument("--progprompt-path", type=str, default="C:/Users/KHJ/Desktop/LAB/progprompt/progprompt-vh")
    parser.add_argument("--expt-name", type=str, default="my_experiment")

    parser.add_argument("--openai-api-key", type=str, default="api-key")
    parser.add_argument("--gpt-version", type=str, default="gpt-4")

    parser.add_argument("--test-set", type=str, default="test_unseen", choices=['test_unseen', 'test_seen'])
    parser.add_argument("--prompt-task-examples", type=str, default="default", choices=['default', 'random'])
    parser.add_argument("--prompt-num-examples", type=int, default=2, choices=range(1, 5))

    args = parser.parse_args()
    openai.api_key = args.openai_api_key

    planner_executer(args=args)
