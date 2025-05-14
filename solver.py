import time  # Import the time module

def parse_grid(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f]

def turn_left(grid, x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # N, S, W, E
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # NW, NE, SW, SE
    filled = set()
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 'X':
            filled.add((nx, ny))
    return filled

def turn_right(grid, x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E
    filled = set()
    for dx, dy in directions:
        nx, ny = x, y
        while 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 'X':
            filled.add((nx, ny))
            nx += dx
            ny += dy
    return filled

def is_fully_covered(grid):
    """Check if all holes (X) are covered."""
    return all(cell != 'X' for row in grid for cell in row)

def apply_relic(grid, x, y, direction):
    """Apply a relic to the grid and return the updated grid and covered positions."""
    filled = turn_left(grid, x, y) if direction == 'left' else turn_right(grid, x, y)
    new_grid = [row[:] for row in grid]  # Create a copy of the grid
    for fx, fy in filled:
        new_grid[fx][fy] = '.'  # Mark as filled
    new_grid[x][y] = 'L' if direction == 'left' else 'R'  # Mark relic placement
    return new_grid, filled

def backtrack_min_relics(grid, placements, covered):
    """Recursive backtracking to find the minimum number of relics."""
    if is_fully_covered(grid):
        return placements[:]  # Return a copy of the placements list

    best_solution = None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'X':  # Try placing a relic at each hole
                for direction in ['left', 'right']:
                    new_grid, filled = apply_relic(grid, x, y, direction)

                    # Calculate new holes filled by this placement
                    new_filled = filled - covered

                    # Skip if applying the relic doesn't fill any new holes
                    if not new_filled:
                        continue

                    # Update the covered set with the new filled positions
                    placements.append((x, y, direction))
                    result = backtrack_min_relics(new_grid, placements, covered | new_filled)
                    if result:  # If a solution is found, check if it's better
                        if best_solution is None or len(result) < len(best_solution):
                            best_solution = result
                    placements.pop()  # Backtrack if no solution
    return best_solution

def solve_single_puzzle(grid):
    """Solve a single puzzle to find the minimum number of relics."""
    placements = backtrack_min_relics(grid, [], set())
    if placements is None:
        raise ValueError("No solution found for the given grid.")
    # Apply the placements to the grid
    for x, y, direction in placements:
        grid, _ = apply_relic(grid, x, y, direction)
    return placements, grid

def save_solution(grid, file_path):
    """Save the solution to a file."""
    solution_file = file_path.replace('.txt', '_solution.txt')
    with open(solution_file, 'w') as f:
        for row in grid:
            f.write(''.join(row) + '\n')
    print(f"Solution saved to {solution_file}")

def main():
    grid_files = ['images/a.txt', 'images/b.txt', 'images/c.txt', 'images/d.txt']  # List of all grid files
    for grid_file in grid_files:
        print(f"Solving puzzle: {grid_file}")
        grid = parse_grid(grid_file)
        try:
            start_time = time.time()  # Start the timer
            placements, updated_grid = solve_single_puzzle(grid)
            end_time = time.time()  # End the timer
            elapsed_time = end_time - start_time  # Calculate elapsed time
            print(f"Placements: {placements}")
            print(f"Time taken for {grid_file}: {elapsed_time:.2f} seconds")  # Display elapsed time
            save_solution(updated_grid, grid_file)
        except ValueError as e:
            print(f"Could not solve the grid {grid_file}: {e}")

if __name__ == "__main__":
    main()