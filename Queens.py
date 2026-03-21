# AI was slightly used for clarification on how to animate using matplotlib :>

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from matplotlib.widgets import Button

n = 0
fundamental = set()

# GUI states
fig = None
ax = None
anim = None
button = None
status_text = None
count_text = None
queen_texts = []
active_outline = None
search_steps = None
waiting_for_click = False
finished = False


def is_safe(row, col, board):
    # Check same column
    for i in range(row):
        if board[i][col] == 2:
            return False

    # Check left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 2:
            return False
        i -= 1
        j -= 1

    # Check right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 2:
            return False
        i -= 1
        j += 1

    return True


def rotate90(b):
    r = [0] * n
    for i in range(n):
        r[b[i]] = n - 1 - i
    return r


def reflect(b):
    r = [0] * n
    for i in range(n):
        r[i] = n - 1 - b[i]
    return r


def canonical(b):
    # All symmetric forms
    forms = [b]

    r1 = rotate90(b)
    r2 = rotate90(r1)
    r3 = rotate90(r2)

    forms.append(r1)
    forms.append(r2)
    forms.append(r3)

    forms.append(reflect(b))
    forms.append(reflect(r1))
    forms.append(reflect(r2))
    forms.append(reflect(r3))

    return min(forms)


def solve(row, board, config):
    global fundamental

    # Full board reached
    if row == n:
        solution = tuple(canonical(config))
        if solution not in fundamental:
            fundamental.add(solution)
            yield ("solution", tuple(config), len(fundamental))
        return

    # Trying every column
    for col in range(n):
        if is_safe(row, col, board):
            board[row][col] = 2
            config[row] = col
            yield ("place", row, col)

            yield from solve(row + 1, board, config)

            board[row][col] = 0
            config[row] = 0
            yield ("remove", row, col)


def set_button_state(enabled):
    base_color = "#4c956c" if enabled else "#d9d9d9"
    hover_color = "#5faa7f" if enabled else "#d9d9d9"
    button.color = base_color
    button.hovercolor = hover_color
    button.ax.set_facecolor(base_color)
    button.label.set_color("white" if enabled else "#666666")


def highlight_square(row, col, color):
    # Moving highlight box
    active_outline.set_xy((col, row))
    active_outline.set_edgecolor(color)
    active_outline.set_visible(True)


def recolor_queens(color):
    # Repainting the queens
    for row in range(n):
        for col in range(n):
            if queen_texts[row][col].get_text() == "Q":
                queen_texts[row][col].set_color(color)


def apply_step(step):
    global waiting_for_click, finished

    # Current event type
    step_type = step[0]

    if step_type == "place":
        row, col = step[1], step[2]
        queen_texts[row][col].set_text("♛")
        queen_texts[row][col].set_color("#000000")
        highlight_square(row, col, "#e0ce08")
        status_text.set_text(f"Placed a queen at row {row}, col {col}.")
        return

    if step_type == "remove":
        row, col = step[1], step[2]
        queen_texts[row][col].set_text("")
        highlight_square(row, col, "#c1121f")
        status_text.set_text(f"Backtracking from row {row}, col {col}.")
        return

    if step_type == "solution":
        solution_number = step[2]
        waiting_for_click = True
        recolor_queens("#17a10d")
        count_text.set_text(f"Solutions found: {solution_number}")
        status_text.set_text(
            f"Solution {solution_number} found. Click 'Next Solution' to continue."
        )
        set_button_state(True)
        anim.event_source.stop()
        return

    if step_type == "done":
        finished = True
        waiting_for_click = False
        active_outline.set_visible(False)
        status_text.set_text(
            f"Search complete. Found {len(fundamental)} solution(s)."
        )
        set_button_state(False)


def advance_frame(_frame_index):
    global finished, waiting_for_click

    # Hold while paused
    if waiting_for_click or finished:
        return []

    try:
        # Read next event
        step = next(search_steps)
    except StopIteration:
        apply_step(("done",))
        return []

    # Paint one step
    apply_step(step)
    return []


def on_next_solution(_event):
    global waiting_for_click

    # Ignore wrong clicks
    if not waiting_for_click or finished:
        return

    # Continue animation
    waiting_for_click = False
    recolor_queens("#8b1e3f")
    status_text.set_text(f"Searching for solution {len(fundamental) + 1}...")
    set_button_state(False)
    anim.event_source.start()
    fig.canvas.draw_idle()


def setup_visualization():
    global fig, ax, button, status_text, count_text, queen_texts, active_outline

    # Create plot window
    fig, ax = plt.subplots(figsize=(7, 8))
    plt.subplots_adjust(bottom=0.18, top=0.9)

    # Build chess board
    queen_texts = []
    for row in range(n):
        row_texts = []
        for col in range(n):
            # Alternate square colors
            color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
            square = patches.Rectangle(
                (col, row),
                1,
                1,
                facecolor=color,
                edgecolor="black",
                linewidth=1,
            )
            ax.add_patch(square)

            queen = ax.text(
                col + 0.5,
                row + 0.5,
                "",
                ha="center",
                va="center",
                fontsize=24,
                fontweight="bold",
                color="#8b1e3f",
            )
            row_texts.append(queen)
        queen_texts.append(row_texts)

    # Active move outline
    active_outline = patches.Rectangle(
        (0, 0),
        1,
        1,
        fill=False,
        edgecolor="#3d5a80",
        linewidth=2.5,
        visible=False,
        zorder=5,
    )
    ax.add_patch(active_outline)

    # Outer board border
    board_outline = patches.Rectangle(
        (0, 0),
        n,
        n,
        fill=False,
        edgecolor="black",
        linewidth=1.5,
        zorder=6,
    )
    ax.add_patch(board_outline)

    # Hide axis labels
    ax.set_title("N-Queens Backtracking Search", fontsize=15, pad=14)
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(n + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.invert_yaxis()
    ax.set_aspect("equal")

    # Top solution text
    count_text = fig.text(
        0.12,
        0.93,
        "Fundamental solutions found: 0",
        fontsize=11,
        color="#222222",
    )
    # Bottom status text
    status_text = fig.text(
        0.12,
        0.06,
        "Searching for solution 1...",
        fontsize=11,
        color="#222222",
    )

    # Add control button
    button_ax = fig.add_axes([0.68, 0.045, 0.2, 0.07])
    button = Button(button_ax, "Next Solution")
    button.on_clicked(on_next_solution)
    set_button_state(False)


def animate_solutions(board, config, interval=450):
    global anim, search_steps, waiting_for_click, finished

    # Reset animation flags
    waiting_for_click = False
    finished = False
    # Create step stream
    search_steps = solve(0, board, config)

    setup_visualization()

    # Run frame loop
    anim = animation.FuncAnimation(
        fig,
        advance_frame,
        interval=interval,
        blit=False,
        cache_frame_data=False,
    )
    plt.show()


def main():
    global n, fundamental

    fundamental = set()
    # Empty search state
    board = [[0 for a in range(n)] for b in range(n)]
    config = [0] * n

    animate_solutions(board, config)

    for _ in solve(0, board, config):
        pass

if __name__ == "__main__":
    main()