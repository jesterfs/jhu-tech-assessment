import unittest
from functions import analyzeVCF, loopOverFiles

class TestVCFAnalyzer(unittest.TestCase):

  def test_loopOverFiles(self):
    files = ["test_data/test1.vcf", "test_data/test2.vcf"]
    result = loopOverFiles(files)
    self.assertEqual(result["SNVs"], 192)
    self.assertEqual(result["indels"], 14)
    self.assertAlmostEqual(result["read_depth_mean"], 40.95, places=2)
    self.assertEqual(result["snv_by_chrom"], {"1": 192})
    self.assertEqual(result["concordance"], 100.0)

  def test_analyzeVCF_single(self):
    files = ["test_data/test1.vcf"]
    result = loopOverFiles(files)
    self.assertEqual(result["SNVs"], 96)
    self.assertEqual(result["indels"], 7)
    self.assertAlmostEqual(result["read_depth_mean"], 40.95, places=2)
    self.assertEqual(result["snv_by_chrom"], {"1": 96})

  def test_analyzeVCF_multiple(self):
    files = ["test_data/test1.vcf", "test_data/test2.vcf"]
    result = loopOverFiles(files)
    self.assertEqual(result["SNVs"], 192)
    self.assertEqual(result["indels"], 14)
    self.assertAlmostEqual(result["read_depth_mean"], 40.95, places=2)
    self.assertEqual(result["snv_by_chrom"], {"1": 192})
    self.assertEqual(result["concordance"], 100.0)

if __name__ == '__main__':
    unittest.main()
