import pandas as pd
import matplotlib.pyplot as plt

def to_utc(s):
    MONTH = {"oct":"10","nov":"11"}
    m, d, t = MONTH[s[:3]], s[3:5], s[6:]
    return f"2025-{m}-{d}T{t}:00Z"

def load_events(path="files/main.txt"):
    rows = []
    with open(path) as f:
        for i, line in enumerate(f):
            if i >= 3 and i <= 147 and line.strip() and not line.startswith("---") and line[19:25] == "tagged":
                parts = [p.strip() for p in line.split("|")]
                ts = to_utc(parts[0])
                target, color = parts[3].split(" with ")
                rows.append([ts, parts[1], target, color.replace(" marker","")])
    return pd.DataFrame(rows, columns=["Datetime", "Tagger", "Tagged", "Marker Color"])

def main():
    df = load_events()

    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True, errors="coerce")
    df["Marker Color"] = df["Marker Color"].astype(str).str.strip().str.title()
    df["Tagged"] = pd.to_numeric(df["Tagged"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Datetime", "Tagged", "Marker Color"]).copy()

    df["_seq"] = range(len(df))
    df = df.sort_values(["Datetime", "_seq"]).drop(columns="_seq")

    game_end = df["Datetime"].max() + pd.Timedelta(seconds=1)

    plt.figure(figsize=(8, 6))

    all_players = set()
    for color, g in df.groupby("Marker Color"):
        g = g.sort_values("Datetime").copy()
        g["Next Datetime"] = g["Datetime"].shift(-1)
        g.loc[g.index[-1], "Next Datetime"] = game_end
        COLOR_MAP = {"Purple": "tab:purple", "Green": "tab:green", "Orange": "tab:orange"}
        c = COLOR_MAP.get(color, None)

        first = True
        for _, row in g.iterrows():
            start, end = row["Datetime"], row["Next Datetime"]
            holder = int(row["Tagged"])
            all_players.add(holder)

            plt.plot([start, end], [holder, holder], linewidth=3, label=color if first else "", color=c)
            plt.scatter([start], [holder], s=16, zorder=3, color=c)
            first = False

    all_players = sorted(all_players)
    if all_players:
        plt.yticks(all_players)
        plt.ylim(min(all_players) - 0.5, max(all_players) + 0.5)

    plt.xlabel("Day")
    plt.ylabel("Player ID (holder)")
    plt.title("marker possession")
    plt.legend(title="Marker", loc='upper left', bbox_to_anchor=(1.02, 1))
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)

    ax = plt.gca()
    ticks = pd.date_range(df["Datetime"].min(), game_end, periods=11)

    ax.set_xticks(ticks)
    ax.set_xticklabels([str(i) for i in range(0, 11)])

    plt.tight_layout()
    plt.savefig("charts/marker_vs_time.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
