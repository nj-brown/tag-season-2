import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Data: rows = days, cols = players
    points = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [100, 100, 0, 25, 0, 25, 0, 0, 100, 0, 0, 0, 0],
        [100, 100, 0, 25, 0, 125, 0, 100, 150, 50, 0, 0, 100],
        [100, 100, 100, 125, 0, 125, 0, 100, 150, 50, 100, 0, 100],
        [100, 100, 150, 125, 0, 125, 100, 100, 150, 150, 100, 100, 150],
        [100, 200, 300, 125, 50, 175, 100, 100, 200, 300, 100, 100, 150],
        [200, 200, 300, 125, 50, 225, 100, 100, 300, 300, 100, 150, 250],
        [300, 200, 300, 125, 150, 225, 150, 100, 400, 300, 100, 150, 250],
        [400, 200, 300, 225, 150, 325, 150, 100, 400, 300, 150, 150, 250],
        [400, 200, 400, 225, 200, 325, 250, 100, 400, 300, 150, 150, 350],
        [400, 200, 500, 275, 350, 325, 250, 150, 400, 300, 200, 300, 350],
    ]

    data = np.array(points)
    days = np.arange(data.shape[0])
    num_players = data.shape[1]

    out_dir = "charts"
    os.makedirs(out_dir, exist_ok=True)

    grey_color = "grey"
    highlight_color = "navy"

    for p in range(num_players):
        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot everyone in grey first
        for q in range(num_players):
            ax.plot(
                days,
                data[:, q],
                color=grey_color,
                linewidth=1.5,
                alpha=0.35,
                marker="o",
            )

        # Highlight player p in deep blue
        ax.plot(
            days,
            data[:, p],
            color=highlight_color,
            linewidth=3.0,
            alpha=1.0,
            marker="o",
            label=f"P{p+1}",
        )

        ax.set_title(f"Player Score Progress: P{p+1} Highlighted")
        ax.set_xlabel("Day")
        ax.set_ylabel("Points")
        ax.set_xticks(days)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="upper left", frameon=True)

        fname = os.path.join(out_dir, f"player_{p+1:02d}.png")
        plt.tight_layout()
        plt.savefig(fname, dpi=200)
        plt.close(fig)

    print(f"Saved {num_players} charts to: {os.path.abspath(out_dir)}")

if __name__ == "__main__":
    main()
