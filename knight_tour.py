from typing import List

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import animation
    from matplotlib import patheffects
    VISUAL_AVAILABLE = True
except ImportError:
    VISUAL_AVAILABLE = False

class KnightTourSolver:
    MOVES = [(2, 1), (2, -1), (-2, 1), (-2, -1),(1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        self.board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        self.visited_order = []
        self.calls = 0
        
    def is_valid_move(self, x: int, y: int, board: List[List[int]]) -> bool:

        return (0 <= x < self.board_size and 
                0 <= y < self.board_size and 
                board[y][x] == -1)
    
    def count_onward_moves(self, x: int, y: int, board: List[List[int]]) -> int:
        
        count = 0
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny, board):
                count += 1
        return count
    
    def solve_recursive(self, x: int, y: int, move_count: int, board: List[List[int]]) -> bool:
        
        self.calls += 1
        
        board[y][x] = move_count
        
        if move_count == self.board_size * self.board_size - 1:
            return True
        
        next_moves = []
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny, board):
                priority = self.count_onward_moves(nx, ny, board)
                next_moves.append((priority, nx, ny))
        
        
        next_moves.sort()
        
       
        for _, nx, ny in next_moves:
            if self.solve_recursive(nx, ny, move_count + 1, board):
                return True
        
        board[y][x] = -1
        return False
    
    def solve(self, start_x: int = 0, start_y: int = 0) -> bool:
        
        self.calls = 0
        
        board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        if self.solve_recursive(start_x, start_y, 0, board):
            self.board = board
            
            path = [(0, 0)] * (self.board_size * self.board_size)
            for y in range(self.board_size):
                for x in range(self.board_size):
                    path[board[y][x]] = (x, y)
            
            self.visited_order = path
            
            return True
        else:
            return False 
        

    def animate_solution(self, interval: int = 600):
        
        fig, ax = plt.subplots(figsize=(6, 6))
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = '#f0d9b5' if (x + y) % 2 == 0 else '#b58863'
                rect = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)
        
        
        knight = ax.text(self.visited_order[0][0] + 0.5,
                         self.visited_order[0][1] + 0.5,
                         '♞', fontsize=28, ha='center', va='center',
                         color='black', zorder=5,
                         path_effects=[ patheffects.Stroke(linewidth=2, foreground='white'),
                                        patheffects.Normal()
                                ])
        
        
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
            for txt in flat_texts:
                txt.set_text('')
            sx, sy = self.visited_order[0]
            xtext[sy][sx].set_text('X')
            return (knight, *flat_texts)
        
        def update(i):
            x, y = self.visited_order[i]
            knight.set_position((x + 0.5, y + 0.5))
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
    cboard_size = 8
    try:
        raw = input(f"Enter starting coordinates x,y (0-{cboard_size-1}), default 0,0: ")
        if raw.strip() == "":
            start_x, start_y = 0, 0
        else:
            parts = raw.replace(',', ' ').split()
            if len(parts) != 2:
                raise ValueError
            start_x = int(parts[0])
            start_y = int(parts[1])
            if not (0 <= start_x < cboard_size and 0 <= start_y < cboard_size):
                raise ValueError
    except Exception:
        print("Invalid input, using default (0,0)")
        start_x, start_y = 0, 0

    solver = KnightTourSolver(board_size=cboard_size)
    success = solver.solve(start_x=start_x, start_y=start_y)
    if success and VISUAL_AVAILABLE:
        solver.animate_solution(interval=600)


if __name__ == "__main__":
    main()
