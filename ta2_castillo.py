# ---- Task 1: Environment ----
environment = {"A": "Clean", "B": "Clean"}


def set_initial_state(env):
    "Let the user set the initial state of each room."
    for room in env:
        while True:
            state = input(f"Is Room {room} Dirty or Clean? ").strip().capitalize()
            if state in ("Dirty", "Clean"):
                env[room] = state
                break
            print("Invalid input. Please type 'Dirty' or 'Clean'.")


def is_dirty(env, room):
    "Return True if the given room is dirty."
    return env[room] == "Dirty"


def clean_room(env, room):
    "Clean the given room."
    env[room] = "Clean"


def show_environment(env):
    "Display the current state of both rooms."
    return ", ".join(f"Room {room}: {state}" for room, state in env.items())


# ---- Task 2: Rule-Based Agent ----
class VacuumAgent:
    def __init__(self, start_location="A"):
        self.location = start_location

    def move(self):
        "Switch to the other room."
        self.location = "B" if self.location == "A" else "A"

    def perceive_and_act(self, env):
        "Apply rules and return the action taken."
        # Rule 1: If current room is dirty, clean it
        if is_dirty(env, self.location):
            clean_room(env, self.location)
            return "Cleaned"
        # Rule 2: If current room is clean, move to next room
        else:
            self.move()
            return "Moved"


# ---- Task 3: Run Simulation ----
def run_simulation(env, agent, steps):
    for step in range(1, steps + 1):
        action = agent.perceive_and_act(env)
        print(f"Step {step}:")
        print(f"  Agent location: Room {agent.location}")
        print(f"  Action taken:   {action}")
        print(f"  Environment:    {show_environment(env)}")
        print()


if __name__ == "__main__":
    set_initial_state(environment)

    while True:
        try:
            steps = int(input("How many steps should the sim run? "))
            if steps > 0:
                break
            print("Enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a whole number :P")

    agent = VacuumAgent(start_location="A")

    print("\nInitial environment:", show_environment(environment))
    print(f"Agent starts in Room {agent.location}\n")

    run_simulation(environment, agent, steps)