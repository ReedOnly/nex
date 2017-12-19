import unittest
import os
import nex

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.spe1 = 'test-data/SPE1.plt'

    def test_load(self):
        plt = nex.load(self.spe1)
        classnames = plt.classname.unique()
        self.assertEqual(
            sorted(classnames),
            sorted([u'WELL', u'NODE', u'CONN', u'CONNLIST', u'FIELD', u'REGION'])
        )
        COP0 = plt.loc[
            (plt['classname'] == 'WELL') &
            (plt['instancename'] == '2') &
            (plt['varname'] == 'COP')
        ]['value'].tolist()
        COP1 = [
            659600.8125, 1168386.75, 1630246.875, 2055481.875, 2449533.25,
            2811901.0, 3147919.0, 3459321.25, 3748449.5, 4011785.75
        ]
        self.assertEqual(COP0, COP1)
