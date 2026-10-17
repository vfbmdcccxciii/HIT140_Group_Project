"""Download raw source snapshots into data/raw (run once; outputs are committed so analysis is reproducible offline).
Sources: openfootball (results), Wikipedia (pre-tournament FIFA ranking), Transfermarkt (squad value/age),
eloratings.net (pre-match Elo + each team's full international match history)."""
import json, time, datetime, re, html, io
import requests, pandas as pd
from common import RAW, TEAMS
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
TODAY = datetime.date.today().isoformat()

def get(url):
    r = requests.get(url, headers=UA, timeout=60); r.raise_for_status(); return r

def main():
    # 1. Match results (all 104 matches)
    (RAW / "openfootball_worldcup2026.json").write_bytes(get("https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json").content)
    # 2. Pre-tournament FIFA ranking from Wikipedia's qualified-teams list
    s = get("https://en.wikipedia.org/wiki/2026_FIFA_World_Cup").text
    i = s.find("Ranking before the tournament were")
    t = re.sub(r"<style.*?</style>|<sup.*?</sup>", "", s[i:i + 60000], flags=re.S)
    t = html.unescape(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", t)))
    t = t[:t.find("Draw Main article")]
    rows = [(n.strip(), int(r)) for n, r in re.findall(r"([A-Z][A-Za-zçã'. ]+?) \((\d+)[;)]", t) if n.strip() not in ("AFC","CAF","CONCACAF","CONMEBOL","OFC","UEFA")]
    pd.DataFrame(rows, columns=["wiki_name", "fifa_rank_pre"]).assign(source_url="https://en.wikipedia.org/wiki/2026_FIFA_World_Cup", retrieved_date=TODAY).to_csv(RAW / "wikipedia_fifa_rank_pre_tournament.csv", index=False)
    # 3. Transfermarkt participating teams table
    tm = get("https://www.transfermarkt.com/weltmeisterschaft-2026/teilnehmer/pokalwettbewerb/FIWC/saison_id/2025").text
    df = [x for x in pd.read_html(io.StringIO(tm)) if x.shape[0] == 48][0]
    # Transfermarkt's header row is offset by one column; rename explicitly.
    df = df.iloc[:, 1:8]; df.columns = ["tm_name", "squad_size", "avg_age", "wc_participations", "foreigners_pct", "total_value", "avg_value"]
    df.assign(source_url="https://www.transfermarkt.com/weltmeisterschaft-2026/teilnehmer/pokalwettbewerb/FIWC/saison_id/2025", retrieved_date=TODAY).to_csv(RAW / "transfermarkt_squads.csv", index=False)
    # 4. eloratings.net match histories for each team
    frames = []
    for of, (_, _, elo, _) in TEAMS.items():
        url = f"https://www.eloratings.net/{elo.replace(" ", "_").replace("ç", "c")}.tsv"
        txt = get(url).text
        d = pd.read_csv(io.StringIO(txt), sep="\t", header=None, dtype=str)
        d = d.iloc[:, :12]; d.columns = ["y","m","d","home","away","hg","ag","comp","venue","change","rating_home_post","rating_away_post"]
        d["team_file"] = of; frames.append(d); time.sleep(0.5)
    out = pd.concat(frames); out["source_url"] = "https://www.eloratings.net/<Team>.tsv"; out["retrieved_date"] = TODAY
    out.to_csv(RAW / "eloratings_team_histories.csv", index=False)
    pd.read_csv("https://www.eloratings.net/en.teams.tsv", sep="\t", header=None, usecols=[0,1], names=["code","name"], storage_options=UA).to_csv(RAW / "eloratings_team_codes.csv", index=False)

if __name__ == "__main__":
    main()
