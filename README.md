# 10-day tag, Season 2

I hosted a game of 10-day tag with 13 of my friends from Oct 27 to Nov 6, 2025. You can read more at [njbrown.com/blog/75](https://njbrown.com/blog/75). If you're confused about what's in this repo, you should probably go read it.

## Explanations
- `python/marker_vs_time.py` generates `python/charts/marker_vs_time.png`, which displays a cool visual of the taggers over the course of the game.
- `python/stats.py` helps calculate some of the values (really, columns A-D) for `stats.xlsx`.
- `python/points_vs_time.py` generates 13 images in `python/charts` that show the progression of each player's points over the game.
- `rules.pdf` are the published rules.
- `python/files/main.txt` is the complete log I kept for Season 2.

## Further notes
- Yes, 10-day tag happened during the Daylight Savings Time shift, which means that _technically_ the game lasted 239 hours instead of 240 hours. But I'm going to ignore that fact and say it was 240 hours, because I don't care.
- I define a transaction in `stats.xlsx` as every time a player's state flips from `tagger -> not tagger` or vice versa. Each player has an even number of transactions. Why is that true? Exercise for the reader :)
- There were 80 tags. Yes, there were 166 transactions, but 6 of those transactions occurred when the null player (00) tagged a real player, or vice versa. (Look at `python/files/main.txt`.) Thus (166 - 6) / 2 = 80.
- If you have ideas for more cool graphs I should add, email me at `njbrown@utexas.edu`.
