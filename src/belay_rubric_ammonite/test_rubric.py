import rubric as rubric
import unittest
import os


class ISOGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.sample_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'samples', '258.xml')
        self.sample_folder = os.path.join(os.path.dirname(__file__), 'fixtures', 'samples')

    def test_rubric_single(self):
        """Belay single record function"""
        doc = rubric.Evaluate(self.sample_file)
        assert isinstance(doc.master_score(), int)

    def test_rubric_batch(self):
        """Belay batch run function"""
        doc = rubric.Evaluate(self.sample_folder)
        assert isinstance(doc, rubric.BelayBatch)


if __name__ == '__main__':
    unittest.main()
