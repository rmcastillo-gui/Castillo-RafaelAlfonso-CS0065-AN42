import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------- Get user input from console --------
num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def step(self, start_positions, reserved_positions):
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        x, y = self.position
        x = max(0, min(self.model.p.grid_size[0]-1, x + direction[0]))
        y = max(0, min(self.model.p.grid_size[1]-1, y + direction[1]))
        destination = (x, y)
        if self.model.path_is_clear(
            self, destination, start_positions, reserved_positions
        ):
            self.position = destination
            reserved_positions.add(destination)

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        # Create agents
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        available_positions = [
            (x, y)
            for x in range(self.p.grid_size[0])
            for y in range(self.p.grid_size[1])
        ]
        if len(self.agents) > len(available_positions):
            raise ValueError("Number of agents cannot exceed the number of grid cells.")
        for agent, position in zip(
            self.agents, random.sample(available_positions, len(self.agents))
        ):
            agent.position = position

        # For grid
        self.grid = ap.Grid(self, self.p.grid_size, torus=False)
        self.grid.add_agents(self.agents)
       
        # Limit two-cell square perimeter around other agents
    def path_is_clear(self, agent, destination, start_positions, reserved_positions):
        if destination in reserved_positions:
            return False
        return all(
            destination != start_positions[id(other)]
            for other in self.agents
            if other is not agent
        )

    def step(self):
        start_positions = {
            id(agent): agent.position for agent in self.agents
        }
        reserved_positions = set()
        for agent in self.agents:
            agent.step(start_positions, reserved_positions)

# -------- Parameters from user input -----------
parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps
}

# -------- Run Model -----------
model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation -----------
fig, ax = plt.subplots()
ax.set_xlim(0, model.p.grid_size[0])
ax.set_ylim(0, model.p.grid_size[1])
ax.set_xticks(range(model.p.grid_size[0]+1))
ax.set_yticks(range(model.p.grid_size[1]+1))
ax.grid(True)

scat = ax.scatter([], [], s=200)  # s = size of agents

def update(frame):
    model.step()
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]
    scat.set_offsets(list(zip(x, y)))
    return scat,

ani = animation.FuncAnimation(fig, update, frames=model.p.steps, blit=True, repeat=False)
plt.show()
