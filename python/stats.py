import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Player:
    def __init__(self, ID: int, name: str):
        self.ID: int = ID
        self.name: str = name
        self.total_time_tagged = 0
        self.transactions = 0

    def calculate_total_time_tagged(self):
        tags = load_tag_events()
        colors = ['green', 'purple', 'orange']
        total = 0

        for color in colors:
            tags_of_one_color = tags.query("Marker_Color == @color")
            tag_pairs = compute_tag_lengths(tags_of_one_color)
            
            for player_id, time_tagged in tag_pairs:
                if player_id == self.ID:
                    total += time_tagged

        self.total_time_tagged = total

    def calculate_transactions(self):
        tags = load_tag_events()
        count = ((tags["Tagger"] == self.ID) | (tags["Tagged"] == self.ID)).sum()
        self.transactions = int(count)

    def print_info(self):
        print(f"Player ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Total Time Tagged: {self.total_time_tagged}")
        print(f"Number of Transactions: {self.transactions}")

def to_utc(s):
    MONTH = {"oct": "10", "nov": "11"}
    m, d, t = MONTH[s[:3]], s[3:5], s[6:]
    return f"2025-{m}-{d}T{t}:00Z"


def load_tag_events():
    """Turns my strangely formatted main.txt into a reasonable DataFrame."""

    rows = []
    with open("files/main.txt") as f:
        for i, line in enumerate(f):
            if (
                i >= 3
                and line.strip()
                and not line.startswith("---")
                and line[19:25] == "tagged"
            ):
                parts = [p.strip() for p in line.split("|")]
                datetime = to_utc(parts[0])
                tagger = int(parts[1])
                tagged, color = parts[3].split(" with ")
                tagged = int(tagged)
                color = color.replace(" marker", "")
                rows.append([datetime, tagger, tagged, color])
    return pd.DataFrame(rows, columns=["Datetime", "Tagger", "Tagged", "Marker_Color"])


def compute_tag_lengths(df):
    df = df.sort_values("Datetime").reset_index(drop=True)
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    lengths = []
    for i in range(len(df) - 1):
        tagged_player = int(df.loc[i, "Tagged"])
        delta_minutes = (
            df.loc[i + 1, "Datetime"] - df.loc[i, "Datetime"]
        ).total_seconds() / 60
        lengths.append([tagged_player, delta_minutes])

    return lengths


def main():

    df = load_tag_events()
    print(df)
    ids = np.arange(1, 14)
    names = ['N. Brown', 'L. Cartwright', 'H. Claire', 'N. Eisenbarth', 'A. Kalagara', 'C. Kilday', 'I. Pyle', 'J. Rue', 'N. Schell', 'H. Shaw', 'H. Simon', 'C. Towlson', 'W. Wozny'] 
    players = [Player(ID, name) for ID, name in zip(ids, names)]
    for p in players:
        p.calculate_total_time_tagged()
        p.calculate_transactions()
        p.print_info()

if __name__ == "__main__":
    main()
