"""Build the two modelling datasets from raw snapshots in data/raw.
Outputs:
  data/processed/matches_104.csv          -> Model 2.1 (one row per match, target = goal difference team1 - team2)
  data/processed/team_matches_208.csv     -> Model 2.2 (one row per team per match, target = goals scored)
  data/processed/team_static.csv          -> pre-tournament team attributes
Every explanatory variable is known BEFORE kick-off:
  * static attributes (FIFA rank before tournament, Transfermarkt squad value/age, WC participations, host nation)
  * Elo rating immediately before the match (eloratings.net post-match rating minus that match's change)
  * form over the team's previous 10 internationals (includes pre-tournament matches, so a team's first WC
    match uses its pre-tournament form - no imputation)
  * rest days since the team's previous international, knockout-stage flag.
Goals = score after extra time where played (penalty shoot-outs excluded), consistent with FIFA's official goals."""
import json
import numpy as np, pandas as pd
from common import RAW, PROC, TEAMS, HOSTS

def money(s):
    s = str(s).replace("€", "")
    mult = 1e9 if s.endswith("bn") else 1e6 if s.endswith("m") else 1e3 if s.endswith("k") else 1
    return float(s.rstrip("bnmk")) * mult

def load_matches():
    d = json.load(open(RAW / "openfootball_worldcup2026.json"))["matches"]
    rows = []
    for i, m in enumerate(d, 1):
        sc = m["score"]; g = sc.get("et", sc["ft"])  # openfootball 'et' = cumulative score after extra time
        rows.append(dict(match_id=i, date=pd.Timestamp(m["date"]), round=m["round"], group=m.get("group", ""),
                         team1=m["team1"], team2=m["team2"], goals1=g[0], goals2=g[1],
                         knockout=int("Matchday" not in m["round"]), extra_time=int("et" in sc), venue=m.get("ground", "")))
    return pd.DataFrame(rows)

def load_static():
    rank = pd.read_csv(RAW / "wikipedia_fifa_rank_pre_tournament.csv")
    tm = pd.read_csv(RAW / "transfermarkt_squads.csv")
    rows = []
    for of, (tmn, wk, elo, conf) in TEAMS.items():
        r = rank.loc[rank.wiki_name == wk, "fifa_rank_pre"]; t = tm[tm.tm_name == tmn]
        assert len(r) == 1 and len(t) == 1, of
        t = t.iloc[0]
        rows.append(dict(team=of, confederation=conf, host=int(of in HOSTS), fifa_rank_pre=int(r.iloc[0]),
                         log_fifa_rank=np.log(int(r.iloc[0])), avg_player_value_eur=money(t.avg_value),
                         log_avg_value=np.log10(money(t.avg_value)), avg_age=float(t.avg_age),
                         wc_participations=int(t.wc_participations)))
    return pd.DataFrame(rows)

def load_elo():
    h = pd.read_csv(RAW / "eloratings_team_histories.csv", dtype=str)
    codes = pd.read_csv(RAW / "eloratings_team_codes.csv")
    code = {of: codes.loc[codes.name == elo, "code"].iloc[0] for of, (_, _, elo, _) in TEAMS.items()}
    h = h.drop_duplicates(subset=["y", "m", "d", "home", "away"])
    h = h[h.y.astype(int) >= 2018].copy()  # only recent history is needed
    h["date"] = pd.to_datetime(h.y + "-" + h.m + "-" + h.d.replace("00", "01"))
    for c in ["hg", "ag", "rating_home_post", "rating_away_post"]:
        h[c] = pd.to_numeric(h[c])
    h["change"] = pd.to_numeric(h["change"].str.replace("−", "-"))
    # one row per (team, match) from that team's perspective
    a = h.assign(code=h.home, opp=h.away, gf=h.hg, ga=h.ag, elo_pre=h.rating_home_post - h.change)
    b = h.assign(code=h.away, opp=h.home, gf=h.ag, ga=h.hg, elo_pre=h.rating_away_post + h.change)
    long = pd.concat([a, b])[["date", "code", "opp", "gf", "ga", "elo_pre", "comp"]].sort_values(["code", "date"])
    return long, code

def team_features(long, code, team, opp, date):
    hist = long[long.code == code[team]]
    row = hist[(hist.date == date) & (hist.opp == code[opp])]
    assert len(row) == 1, (team, opp, date)
    prev = hist[hist.date < date].tail(10)
    return dict(elo_pre=float(row.elo_pre.iloc[0]), gf10=prev.gf.mean(), ga10=prev.ga.mean(),
                rest_days=min((date - hist[hist.date < date].date.max()).days, 30),
                elo_gf=int(row.gf.iloc[0]), elo_ga=int(row.ga.iloc[0]))

def main():
    m, st = load_matches(), load_static()
    long, code = load_elo()
    st.to_csv(PROC / "team_static.csv", index=False)
    S = st.set_index("team")
    team_rows = []
    for _, r in m.iterrows():
        for t, o, gf, ga in [(r.team1, r.team2, r.goals1, r.goals2), (r.team2, r.team1, r.goals2, r.goals1)]:
            f = team_features(long, code, t, o, r.date)
            # cross-check results between two independent sources
            assert (f["elo_gf"], f["elo_ga"]) == (gf, ga), (r.match_id, t, gf, ga, f)
            team_rows.append(dict(match_id=r.match_id, date=r.date.date(), round=r["round"], team=t, opponent=o,
                                  knockout=r.knockout, goals=gf, goals_against=ga, **{k: v for k, v in f.items() if not k.startswith("elo_g")},
                                  **{c: S.loc[t, c] for c in ["host", "log_fifa_rank", "fifa_rank_pre", "log_avg_value", "avg_age", "wc_participations", "confederation"]}))
    tm = pd.DataFrame(team_rows)
    opp = tm[["match_id", "team", "elo_pre", "ga10", "gf10", "log_avg_value", "log_fifa_rank"]].rename(columns=lambda c: c if c == "match_id" else "opp_" + c)
    tm = tm.merge(opp, left_on=["match_id", "opponent"], right_on=["match_id", "opp_team"]).drop(columns="opp_team")
    tm.to_csv(PROC / "team_matches_208.csv", index=False)
    # Match-level (team1 perspective) differences
    t1 = tm.merge(m[["match_id", "team1"]], left_on=["match_id", "team"], right_on=["match_id", "team1"])
    t2 = tm.merge(m[["match_id", "team2"]], left_on=["match_id", "team"], right_on=["match_id", "team2"])
    t1, t2 = t1.set_index("match_id").sort_index(), t2.set_index("match_id").sort_index()
    mm = m.set_index("match_id").copy()
    mm["goal_diff"] = mm.goals1 - mm.goals2
    mm["elo_diff"] = t1.elo_pre - t2.elo_pre
    mm["log_rank_diff"] = t1.log_fifa_rank - t2.log_fifa_rank
    mm["log_value_diff"] = t1.log_avg_value - t2.log_avg_value
    mm["gf10_diff"] = t1.gf10 - t2.gf10
    mm["ga10_diff"] = t1.ga10 - t2.ga10
    mm["age_diff"] = t1.avg_age - t2.avg_age
    mm["wc_exp_diff"] = t1.wc_participations - t2.wc_participations
    mm["host_diff"] = t1.host - t2.host
    mm["rest_diff"] = t1.rest_days - t2.rest_days
    mm.reset_index().to_csv(PROC / "matches_104.csv", index=False)
    print("matches:", len(mm), "team-rows:", len(tm), "results cross-check vs eloratings: OK")

if __name__ == "__main__":
    main()
