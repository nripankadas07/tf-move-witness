import unittest
from tf_move_witness import analyze

def fixture(state,*moves):return {'state':state,'moves':[{'from':a,'to':b} for a,b in moves]}
class Behavior(unittest.TestCase):
    def test_chain(self):self.assertEqual(analyze(fixture(['aws_x.a'],('aws_x.a','aws_x.b'),('aws_x.b','aws_x.c')))['proposed'][0]['chain'],['aws_x.a','aws_x.b','aws_x.c'])
    def test_independent(self):self.assertEqual(analyze(fixture(['aws_x.a','aws_x.z'],('aws_x.a','aws_x.b')))['result_addresses'],['aws_x.b','aws_x.z'])
    def test_explicit_instance(self):self.assertEqual(analyze(fixture(['aws_x.a[0]'],('aws_x.a[0]','module.m.aws_x.b["key"]')))['result_addresses'],['module.m.aws_x.b["key"]'])
    def test_unused(self):self.assertEqual(analyze(fixture([],('aws_x.a','aws_x.b')))['unused_sources'],['aws_x.a'])
    def test_occupied(self):
        with self.assertRaises(ValueError):analyze(fixture(['aws_x.a','aws_x.b'],('aws_x.a','aws_x.b')))
    def test_intermediate_occupied(self):
        with self.assertRaises(ValueError):analyze(fixture(['aws_x.a','aws_x.b'],('aws_x.a','aws_x.b'),('aws_x.b','aws_x.c')))
    def test_merge_collision(self):
        with self.assertRaises(ValueError):analyze(fixture(['aws_x.a','aws_x.b'],('aws_x.a','aws_x.c'),('aws_x.b','aws_x.c')))
    def test_cycles_even_empty_state(self):
        with self.assertRaises(ValueError):analyze(fixture([],('aws_x.a','aws_x.b'),('aws_x.b','aws_x.a')))
    def test_cross_type(self):
        with self.assertRaises(ValueError):analyze(fixture(['aws_x.a'],('aws_x.a','aws_y.b')))
    def test_whole_indexed(self):
        with self.assertRaises(ValueError):analyze(fixture(['aws_x.a[0]'],('aws_x.a','aws_x.b')))
    def test_duplicate_source(self):
        with self.assertRaises(ValueError):analyze(fixture([],('aws_x.a','aws_x.b'),('aws_x.a','aws_x.c')))
    def test_data_unsupported(self):
        with self.assertRaises(ValueError):analyze(fixture(['data.aws_x.a']))
    def test_noncanonical_key_rejected(self):
        with self.assertRaises(ValueError):analyze(fixture([r'aws_x.a["\u0061"]']))

if __name__=="__main__":unittest.main()
