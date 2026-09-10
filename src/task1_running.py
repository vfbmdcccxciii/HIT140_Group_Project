"""Running distance: covered midfielders and forwards with at least 180 minutes."""
import pandas as pd
from analysis_common import ROOT, run_task

def main():
    d=pd.read_csv(ROOT/'data/processed/fifa_player_analysis.csv')
    d=d.loc[d.position.isin(['MF','FW']) & (d.minutes_played>=180) & d.total_distance_km_per90.notna()]
    return run_task(d,'task1_running','total_distance_km_per90','Distance covered (km per 90 minutes)',30)

if __name__=='__main__': main()
