# Data sources (HIT140 A3, Darwin Group 27) — all retrieved 2026-10-16 by `src/fetch_sources.py`

| File (data/raw) | Source | What we use | Notes |
|---|---|---|---|
| `openfootball_worldcup2026.json` | https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json | Date, round, teams, final score (after extra time) for all 104 matches | Open-data mirror of FIFA results. **Independently cross-checked**: all 208 team-match scores match eloratings.net exactly (assert in `prepare_data.py`). |
| `wikipedia_fifa_rank_pre_tournament.csv` | https://en.wikipedia.org/wiki/2026_FIFA_World_Cup (qualified-teams list, citing FIFA) | FIFA Men's World Ranking position before the tournament | Official FIFA ranking page is JS-rendered and blocked to scripts; Wikipedia's cited list used instead. |
| `transfermarkt_squads.csv` | https://www.transfermarkt.com/weltmeisterschaft-2026/teilnehmer/pokalwettbewerb/FIWC/saison_id/2025 | Average player market value, average age, WC participations | Lecturer-approved. **Caveat:** values are Transfermarkt's *current* (Oct 2026) figures; no pre-tournament snapshot was available (Wayback Machine had none). Average (not total) value used because squad-list sizes differ (e.g. Germany 43 listed). |
| `eloratings_team_histories.csv`, `eloratings_team_codes.csv` | https://www.eloratings.net/<Team>.tsv | Every international match per team: score, Elo change and post-match ratings → **pre-match Elo** and **last-10-match form** (goals for/against) | Not one of the four listed sources — flag to lecturer / justify in report. Gives genuine pre-tournament stats for teams' first matches (no imputation). |

FBref returned HTTP 403 to scripted requests and was not used. FIFA's statistics site is JS-rendered; the player-level FIFA snapshots from Assessment 2 (`../repo/data/raw`) are tournament totals (post-match information) so they were deliberately **not** used as predictors.

Definitions: goals include extra time, exclude penalty shoot-outs (9 matches went to extra time). Goal difference = team1 − team2 (openfootball listing order).
