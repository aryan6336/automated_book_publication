# q_learning_agent.py

import json
from state_detector import detect_states  # Detects S1–S5 from input text
from ai_agents.reviewer import run_reviewer_agent  # Sends prompt to reviewer LLM
import os

# Load Q-values from file
with open("rl_data/q_table.json", "r") as f:
    Q = json.load(f)

# Load the AI reviewer output
INPUT_PATH = "output/rewritten_by_writer.txt"
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Mapping of actions to prompts
ACTION_PROMPTS = {
    "A1": (
        "The following text contains several long and complex sentences. "
        "Please rewrite it by breaking down long sentences into shorter, clearer ones "
        "to improve readability while maintaining the original meaning:\n\n{text}"
    ),
    "A2": (
        "The following text uses passive voice in many sentences. "
        "Please convert the sentences into active voice wherever possible to make the writing more direct and engaging:\n\n{text}"
    ),
    "A3": (
        "The following text may have grammar mistakes, punctuation errors, or awkward phrasing. "
        "Please correct all grammatical issues and ensure that punctuation and sentence structure are clear and professional:\n\n{text}"
    ),
    "A4": (
        "The text below may have repetitive words or phrases. "
        "Please identify and reduce redundancy, using synonyms or rephrasing to improve vocabulary variety and flow:\n\n{text}"
    ),
    "A5": (
        "The text is in its final stage. Please polish it for publishing-level quality: "
        "refine the language, check flow, tone, grammar, and style to make it clear, concise, and compelling:\n\n{text}"
    )
}
    
def run_q_learning_ai_reviewer():
    # Step 1: Detect the current state of the text
    detected_states = detect_states(text)
    if not detected_states:
        print("⚠️ No identifiable state detected. Defaulting to S5.")
        current_state = "S5"
    else:
        current_state = detected_states[0]

    print(f"📍 Detected state: {current_state}")

    # Step 2: Pick the best action for the current state based on Q-values
    best_action = max(Q[current_state], key=Q[current_state].get)
    prompt =ACTION_PROMPTS[best_action].format(text=text)

    print(f"🎯 Selected action: {best_action} → {prompt}")

    # Step 3: Apply the selected prompt to the reviewer model (LLM)
    improved_text = run_reviewer_agent(prompt)

    return improved_text
