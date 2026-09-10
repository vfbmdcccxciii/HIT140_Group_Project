import unittest
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analysis_common import compare_means, mean_confidence_interval, random_sample_by_group, ROOT

class InferenceTests(unittest.TestCase):
    def test_unequal_variances_and_course_df(self):
        a=np.array([1,2,4,8,16.])
        b=np.array([2,3,4,5,6,7.])
        actual=compare_means(a,b)
        reference=stats.ttest_ind(a,b,equal_var=False)
        self.assertAlmostEqual(actual['t_statistic'],reference.statistic)
        self.assertEqual(actual['degrees_of_freedom'],4)
        self.assertAlmostEqual(actual['p_value_two_sided'],2*stats.t.sf(abs(reference.statistic),4))
        reverse=compare_means(b,a)
        self.assertAlmostEqual(reverse['p_value_two_sided'],actual['p_value_two_sided'])
        self.assertAlmostEqual(reverse['mean_difference_MF_minus_FW'],-actual['mean_difference_MF_minus_FW'])
    def test_ci_known_symmetric_case(self):
        lo,hi=mean_confidence_interval([1,2,3,4,5])
        margin=stats.t.ppf(.975,4)*np.sqrt(.5)
        self.assertAlmostEqual(lo,3-margin)
        self.assertAlmostEqual(hi,3+margin)
    def test_invalid_input_rejected(self):
        for x in [[1],[1,np.nan],[1,np.inf]]:
            with self.assertRaises(ValueError): mean_confidence_interval(x)
        with self.assertRaises(ValueError): compare_means([1,1],[2,2])
    def test_source_and_sample_integrity(self):
        original=pd.read_csv(ROOT/'data/raw/fifa_player_minutes_2026-08-31.csv')
        supplement=pd.read_csv(ROOT/'data/raw/fifa_player_minutes_supplement_2026-09-10.csv')
        self.assertEqual(len(supplement),281)
        combined=pd.concat([original,supplement])
        self.assertEqual(len(combined),1033)
        self.assertFalse(combined.duplicated(['player','team','position']).any())
        d=pd.read_csv(ROOT/'data/processed/fifa_player_analysis.csv')
        for name,metric,threshold,n in [('task1_running','total_distance_km_per90',180,30),('task2_pressing','direct_pressure_share_pct',90,40)]:
            frame=d.loc[d.position.isin(['MF','FW']) & (d.minutes_played>=threshold) & d[metric].notna()]
            expected=random_sample_by_group(frame,n)
            actual=pd.read_csv(ROOT/f'outputs/{name}_sample.csv')
            self.assertEqual(actual.player.tolist(),expected.player.tolist())
            self.assertEqual(actual.groupby('position').size().tolist(),[n,n])
            self.assertFalse(actual.duplicated(['player','team','position']).any())
        ratio=d.direct_pressure_share_pct.dropna()
        self.assertTrue(ratio.between(0,100).all())

if __name__=='__main__': unittest.main()
