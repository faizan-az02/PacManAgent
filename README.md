# PacManAgent

A Python Pacman-style **grid simulation** with a simple **utility-based agent**.

The game generates a random **4x4** board and moves Pacman until either:
- all food and cherries are consumed (**win**), or
- Pacman steps onto a ghost without a power pellet (**loss**).

## What’s in the grid?

The board is represented as a 1D list of 16 cells (indices **0–15**) mapped row-wise into a 4x4 grid.

- **`P`**: Pacman (always starts at cell `0`)
- **`F`**: Food
- **`C`**: Cherry (grants +1 “power pellet”)
- **`G`**: Ghost
- **`-`**: Empty cell

Random placement (besides Pacman at cell 0):
- 3 ghosts (`G`)
- 3 cherries (`C`)
- 6 food (`F`)
- 3 empty (`-`)

## Agent behavior

At each step, the agent considers the valid neighboring cells (up/down/left/right) and chooses the move with the **highest immediate utility**:

- **`C`**: +10
- **`F`**: +5
- **`G`**:
  - **-9999** if Pacman has **0** power pellets (effectively “avoid”)
  - **+1** if Pacman has **>0** power pellets (it can survive by spending one)
- **otherwise**: 0

Cherry rule:
- stepping on a **`C`** increases `power_pellets` by **1**

Ghost rule:
- stepping on a **`G`** with `power_pellets > 0` consumes **1** pellet and Pacman survives
- stepping on a **`G`** with `power_pellets == 0` ends the game

There is also a `max_steps = 50` cap to prevent infinite loops.

## How to run

### Prerequisites

- Python 3.x (uses only the standard library)

You’ll see:
- the initial random grid
- the grid after each move
- current power pellets
- utility gained per move and total utility

## Notes

If you want to expand this beyond baseline:
- add stochastic ghost movement
- track visited states to reduce loops
- parameterize grid size and item counts

