import heapq
from typing import Tuple, List, Set, Optional
import time

# optional visualization (including animation)
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import animation
    from matplotlib import patheffects
    VISUAL_AVAILABLE = True
except ImportError:
    VISUAL_AVAILABLE = False

class KnightTourAStar:
    """Knight's Tour solver using Warnsdorff's heuristic with backtracking"""
    
    # Knight move offsets (L-shaped: 2 squares in one direction, 1 in perpendicular)
    MOVES = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        self.board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        self.visited_order = []
        self.calls = 0
        
    def is_valid_move(self, x: int, y: int, board: List[List[int]]) -> bool:
        """Check if a move is valid (within bounds and not visited)"""
        return (0 <= x < self.board_size and 
                0 <= y < self.board_size and 
                board[y][x] == -1)
    
    def count_onward_moves(self, x: int, y: int, board: List[List[int]]) -> int:
        """Warnsdorff's heuristic: count number of valid next moves"""
        count = 0
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny, board):
                count += 1
        return count
    
    def solve_recursive(self, x: int, y: int, move_count: int, board: List[List[int]]) -> bool:
        """
        Recursively solve knight's tour using Warnsdorff's heuristic
        Returns True if a complete tour is found
        """
        self.calls += 1
        
        # Mark current square with move number
        board[y][x] = move_count
        
        # If all squares are visited, we found a solution
        if move_count == self.board_size * self.board_size - 1:
            return True
        
        # Get all valid next moves and sort by Warnsdorff's heuristic
        next_moves = []
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny, board):
                priority = self.count_onward_moves(nx, ny, board)
                next_moves.append((priority, nx, ny))
        
        # Sort by priority (fewest onward moves = higher priority)
        next_moves.sort()
        
        # Try each move
        for _, nx, ny in next_moves:
            if self.solve_recursive(nx, ny, move_count + 1, board):
                return True
        
        # Backtrack: unmark current square
        board[y][x] = -1
        return False
    
    def solve(self, start_x: int = 0, start_y: int = 0) -> bool:
        """
        Solve knight's tour using Warnsdorff's heuristic with backtracking
        Returns True if a complete tour is found
        """
        self.calls = 0
        
        print(f"Starting Knight's Tour Solver (Warnsdorff's Heuristic) from ({start_x}, {start_y})...")
        print(f"Board size: {self.board_size}x{self.board_size}")
        print(f"Goal: Visit all {self.board_size * self.board_size} squares\n")
        
        start_time = time.time()
        
        # Initialize board (-1 means unvisited)
        board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Solve using recursive backtracking
        if self.solve_recursive(start_x, start_y, 0, board):
            self.board = board
            
            # Extract the path from the board
            path = [(0, 0)] * (self.board_size * self.board_size)
            for y in range(self.board_size):
                for x in range(self.board_size):
                    path[board[y][x]] = (x, y)
            
            self.visited_order = path
            
            elapsed = time.time() - start_time
            print(f"✓ Solution found!")
            print(f"Function calls: {self.calls}")
            print(f"Time: {elapsed:.3f} seconds\n")
            return True
        else:
            elapsed = time.time() - start_time
            print(f"✗ No solution found")
            print(f"Function calls: {self.calls}")
            print(f"Time: {elapsed:.3f} seconds\n")
            return False
    
    def visualize_solution(self):
        """Display the knight's tour solution on the board"""
        if not self.visited_order:
            print("No solution to visualize. Run solve() first.")
            return
        
        # Create board with move order
        board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for step, (x, y) in enumerate(self.visited_order):
            board[y][x] = step
        
        # Print the board
        print("\nKnight's Tour Solution (move numbers):")
        print("=" * (self.board_size * 4 + 1))
        
        for y in range(self.board_size):
            print("|", end="")
            for x in range(self.board_size):
                print(f"{board[y][x]:3d}|", end="")
            print()
            print("=" * (self.board_size * 4 + 1))
    
    def visualize_path(self):
        """Display the path as a grid showing the order of visits"""
        if not self.visited_order:
            print("No solution to visualize. Run solve() first.")
            return
        
        print("\nKnight's Tour Path Visualization:")
        print("\nPath sequence:")
        
        # Create visual representation with arrows
        board_chars = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        for step, (x, y) in enumerate(self.visited_order):
            board_chars[y][x] = '*'
        
        for y in range(self.board_size):
            print(" ".join(board_chars[y]))
        
        print(f"\nTotal moves: {len(self.visited_order) - 1}")
        print(f"Squares visited: {len(self.visited_order)}/{self.board_size * self.board_size}")
        
        # if matplotlib available offer graphical board
        if VISUAL_AVAILABLE:
            self.plot_board()
            # also allow the caller to animate

    def plot_board(self):
        """Graphical board using matplotlib"""
        if not self.visited_order:
            return
        fig, ax = plt.subplots(figsize=(6, 6))
        # draw checkerboard
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'
                rect = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)
        # move numbers
        for step, (x, y) in enumerate(self.visited_order):
            ax.text(x + 0.5, y + 0.5, str(step), ha='center', va='center', fontsize=8)
        # arrows
        for i in range(len(self.visited_order) - 1):
            x1, y1 = self.visited_order[i]
            x2, y2 = self.visited_order[i+1]
            ax.arrow(x1+0.5, y1+0.5, x2-x1, y2-y1, head_width=0.1, head_length=0.1, fc='red', ec='red')
        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')
        plt.show()

    def animate_solution(self, interval: int = 600):
        """Animate the knight moving through the solution path on the board."""
        if not VISUAL_AVAILABLE:
            print("Animation requires matplotlib. Install the package to enable this feature.")
            return
        if not self.visited_order:
            print("No solution available to animate. Run solve() first.")
            return
        
        fig, ax = plt.subplots(figsize=(6, 6))
        # draw board squares
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'
                rect = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)
        
        
        knight = ax.text(self.visited_order[0][0] + 0.5,
                         self.visited_order[0][1] + 0.5,
                         '♞', fontsize=28, ha='center', va='center',
                         color='black', zorder=5,
                         path_effects=[
                             patheffects.Stroke(linewidth=2, foreground='white'),
                             patheffects.Normal()
                         ])
        
        
        # prepare grid of X markers (initially invisible) with lower zorder
        xtext = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        flat_texts = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                t = ax.text(x + 0.5, y + 0.5, '', ha='center', va='center',
                            fontsize=24, color='red', fontweight='bold')
                xtext[y][x] = t
                flat_texts.append(t)
        
        def init():
            knight.set_position((self.visited_order[0][0] + 0.5,
                                 self.visited_order[0][1] + 0.5))
            # clear any X marks
            for txt in flat_texts:
                txt.set_text('')
            # mark starting square
            sx, sy = self.visited_order[0]
            xtext[sy][sx].set_text('X')
            return (knight, *flat_texts)
        
        def update(i):
            x, y = self.visited_order[i]
            knight.set_position((x + 0.5, y + 0.5))
            # mark visited square
            xtext[y][x].set_text('X')
            return (knight, *flat_texts)
        
        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')
        
        anim = animation.FuncAnimation(
            fig,
            update,
            init_func=init,
            frames=len(self.visited_order),
            interval=interval,
            blit=True,
            repeat=False,
        )
        plt.show()


def main():
    """Solve and animate a standard 8×8 knight's tour.

    The user is prompted for a starting square (x,y) with 0-based
    coordinates. Press Enter to default to (0,0).
    """
    board_size = 8
    # ask user for start position
    try:
        raw = input(f"Enter starting coordinates x,y (0-{board_size-1}), default 0,0: ")
        if raw.strip() == "":
            start_x, start_y = 0, 0
        else:
            parts = raw.replace(',', ' ').split()
            if len(parts) != 2:
                raise ValueError
            start_x = int(parts[0])
            start_y = int(parts[1])
            if not (0 <= start_x < board_size and 0 <= start_y < board_size):
                raise ValueError
    except Exception:
        print("Invalid input, using default (0,0)")
        start_x, start_y = 0, 0

    solver = KnightTourAStar(board_size=board_size)
    success = solver.solve(start_x=start_x, start_y=start_y)
    if success and VISUAL_AVAILABLE:
        # slower default animation
        solver.animate_solution(interval=600)
    elif success:
        print("Solution computed. Install matplotlib to see animation.")


if __name__ == "__main__":
    main()
