import random

def print_grid(grid):
    """
    Print the 4x4 grid.
    """
    for row in range(4):
        row_repr = []
        for col in range(4):
            cell_index = row * 4 + col
            row_repr.append(grid[cell_index])
        print(row_repr)
    print()

def get_neighbors(pos):
    """
    Given a cell index (0-15) in a 4x4 grid, return valid neighbor cells
    (up, down, left, right) that are within the grid bounds.
    """
    neighbors = []
    row = pos // 4
    col = pos % 4

    # Up
    if row > 0:
        neighbors.append(pos - 4)
    # Down
    if row < 3:
        neighbors.append(pos + 4)
    # Left
    if col > 0:
        neighbors.append(pos - 1)
    # Right
    if col < 3:
        neighbors.append(pos + 1)

    return neighbors

def compute_move_utility(grid, current_pos, next_pos, power_pellets):
    """
    Compute a simple utility for moving from current_pos to next_pos.

    Utility logic (example):
      - +10 for a Cherry 'C'
      - +5 for Food 'F'
      - +1 for a Ghost 'G' if we have power pellets
      - -9999 for a Ghost 'G' if we have no power pellets
      - 0 otherwise
    """
    cell_value = grid[next_pos]
    utility = 0

    if cell_value == 'C':
        utility += 10
    elif cell_value == 'F':
        utility += 5
    elif cell_value == 'G':
        if power_pellets == 0:
            utility -= 9999
        else:
            utility += 1
    return utility

def all_pellets_consumed(grid):
    """
    Check if all food 'F' and cherries 'C' have been consumed.
    """
    for cell in grid:
        if cell == 'F' or cell == 'C':
            return False
    return True

def generate_random_grid():
    """
    Generate a 4x4 grid.
    Pacman ('P') is always at cell 0.
    Randomly place:
      - 3 Ghosts 'G'
      - 3 Cherries 'C'
      - 6 Food 'F'
      - The remaining cells are empty '-'
    """
    # Define the item pool for the 15 remaining cells
    items = [
        'G','G','G',   # 3 Ghosts
        'C','C','C',   # 3 Cherries
        'F','F','F','F','F','F',  # 6 Food
        '-','-','-'    # 3 Empty
    ]

    # Shuffle the items
    random.shuffle(items)

    # Build the grid
    # Index 0 is Pacman, so we'll place 'P' there and fill the rest from our list
    grid = ['P'] + items
    return grid

def run_pacman_game():
    """
    Main function to run the Pacman game until:
    1) All pellets are eaten, or
    2) Pacman is destroyed by moving onto a ghost (when no power pellet).
    """
    # Generate a random 4x4 grid
    grid = generate_random_grid()

    # Pacman starts at cell 0
    pacman_position = 0

    # Number of power pellets Pacman currently holds
    power_pellets = 0

    # Keep track of total utility
    total_utility = 0

    # Print the initial state of the grid
    print("Initial Grid State:")
    print_grid(grid)

    step_count = 0
    max_steps = 50  # To prevent infinite loops

    while step_count < max_steps:
        step_count += 1

        # Check if all pellets are consumed
        if all_pellets_consumed(grid):
            print("All pellets have been consumed! Pacman wins!")
            break

        # Determine valid moves
        neighbors = get_neighbors(pacman_position)

        # If no neighbors (completely trapped - not likely in an open 4x4), break
        if not neighbors:
            print("Pacman has no moves left. Game Over.")
            break

        # Compute utility for each neighbor; pick the best
        best_move = None
        best_move_utility = -999999

        for n_pos in neighbors:
            move_utility = compute_move_utility(grid, pacman_position, n_pos, power_pellets)
            if move_utility > best_move_utility:
                best_move_utility = move_utility
                best_move = n_pos

        next_pos = best_move

        # Check if next_pos has a ghost without power pellet
        if grid[next_pos] == 'G' and power_pellets == 0:
            print(f"Pacman moved onto a Ghost at cell {next_pos} with no power pellet! Game Over.")
            total_utility += best_move_utility
            break

        # If it's a Cherry, increase power pellets
        if grid[next_pos] == 'C':
            power_pellets += 1

        # If it's a Ghost but we have power pellets, we survive (use one pellet)
        if grid[next_pos] == 'G' and power_pellets > 0:
            power_pellets -= 1

        # Consume whatever is in next_pos (except Ghost remains, but effectively it's safe now)
        # Mark old position as '-'
        grid[pacman_position] = '-'
        pacman_position = next_pos
        grid[pacman_position] = 'P'

        # Update total utility
        total_utility += best_move_utility

        # Print the grid state after the move
        print(f"After move {step_count} (Pacman -> cell {pacman_position}):")
        print_grid(grid)
        print(f"Current power pellets: {power_pellets}")
        print(f"Utility from this move: {best_move_utility}")
        print(f"Total utility so far: {total_utility}")
        print("--------------------------------------------------")

    else:
        # If we exit the loop because we hit max_steps.
        print("Maximum step limit reached. Ending game.")

    print("Final Grid State:")
    print_grid(grid)
    print(f"Final total utility: {total_utility}")

if __name__ == "__main__":
    run_pacman_game()