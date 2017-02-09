from nose.tools import eq_
from pyculiarity import detect_vec
from unittest import TestCase
import pandas as pd
import os

class TestVec(TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.raw_data = pd.read_csv(os.path.join(self.path,
                                                 'raw_data.csv'),
                                    usecols=['timestamp', 'count'])

    def test_both_directions_with_plot(self):
        results = detect_vec(self.raw_data.iloc[:,1], max_anoms=0.02,
                                     direction='both', period=1440,
                                     only_last=True, plot=False)
        eq_(len(results['anoms'].columns), 2)
        eq_(len(results['anoms'].iloc[:,1]), 25)

    def test_both_directions_e_value_longterm(self):
        results = detect_vec(self.raw_data.iloc[:,1], max_anoms=0.02,
                                     direction='both', period=1440,
                                     longterm_period=1440*14, e_value=True)
        eq_(len(results['anoms'].columns), 3)
        eq_(len(results['anoms'].iloc[:,1]), 131)


    def test_both_direction_e_value_longterm_anomaly_in_last_longterm(self):
        data = [5, 20, 25, 30, 35, 25, 5] * 88
        data = data[:-4]
        data[587] = 100000
        results = detect_vec(data, max_anoms=0.1, direction='both', period=7, longterm_period=7 * 4, e_value=True)
        eq_(len(results['anoms'].columns), 3)
        eq_(len(results['anoms'].iloc[:,1]), 2)
        eq_(int(results['anoms'].iloc[0]['expected_value']), 5)
        eq_(int(results['anoms'].iloc[1]['expected_value']), 50229)


    def test_both_directions_e_value_threshold_med_max(self):
        results = detect_vec(self.raw_data.iloc[:,1], max_anoms=0.02,
                                     direction='both', period=1440,
                                     threshold="med_max", e_value=True)
        eq_(len(results['anoms'].columns), 3)
        eq_(len(results['anoms'].iloc[:,1]), 6)


