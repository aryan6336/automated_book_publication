import json
import os

"""
State ID	Description
S1	Long Sentences, Low Readability
S2	Contains Passive Voice, Moderate Readability
S3	Grammar Issues, Moderate Readability
S4	Repetitive Phrases, High Readability
S5	High Quality Text (Ideal state)
"""
"""
Action ID	Description
A1	Simplify sentence structure
A2	Convert passive to active voice
A3	Correct grammar mistakes
A4	Rephrase for clarity
A5	Accept as-is (no change)
"""
# --- 1. Define Reward Table ---
R = {
    "S1": {"A1": 5, "A2": 1, "A3": 2, "A4": 3, "A5": -3},
    "S2": {"A1": 1, "A2": 5, "A3": 2, "A4": 2, "A5": -2},
    "S3": {"A1": 0, "A2": 1, "A3": 5, "A4": 2, "A5": -1},
    "S4": {"A1": 1, "A2": 0, "A3": 1, "A4": 4, "A5": 1},
    "S5": {"A1": -2, "A2": -2, "A3": -2, "A4": -1, "A5": 5}
}

# --- 2. Initialize Q-Table ---
Q = {state: {action: 0.0 for action in actions} for state, actions in R.items()}

# --- 3. Q-Learning Parameters ---
alpha = 0.8            # Learning rate
gamma = 0.9            # Discount factor
episodes = 100         # Training iterations

states = list(R.keys())
actions = ["A1", "A2", "A3", "A4", "A5"]

# --- 4. Train Q-Table ---
for episode in range(episodes):
    for state in states:
        for action in actions:
            reward = R[state][action]

            # Choose next state arbitrarily (assume agent can move to S5 ideally)
            next_state = "S5"
            max_future_q = max(Q[next_state].values())

            # Q-learning formula
            Q[state][action] = reward + gamma * max_future_q

# --- 5. Save Q-Table to File ---
os.makedirs("rl_data", exist_ok=True)

with open("rl_data/q_table.json", "w") as f:
    json.dump(Q, f, indent=4)

print("✅ Q-table saved to rl_data/q_table.json")
