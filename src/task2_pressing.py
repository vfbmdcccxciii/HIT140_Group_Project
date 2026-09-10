"""Direct-pressure share: covered midfielders and forwards with at least 90 minutes."""
import pandas as pd
from analysis_common import ROOT, run_task

def main():
    d=pd.read_csv(ROOT/'data/processed/fifa_player_analysis.csv')
    total=d.defensive_pressures_applied
    direct=d.defensive_pressures_directly_applied
    if ((direct<0)|(direct>total)).any(): raise ValueError('Invalid direct pressures')
    d['direct_pressure_share_pct']=100*direct/total.where(total>0)
    d=d.loc[d.position.isin(['MF','FW']) & (d.minutes_played>=90) & d.direct_pressure_share_pct.notna()]
    return run_task(d,'task2_pressing','direct_pressure_share_pct','Direct pressures (% of all pressures)',40)

if __name__=='__main__': main()
