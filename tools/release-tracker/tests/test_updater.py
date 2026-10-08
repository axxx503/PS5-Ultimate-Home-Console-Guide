import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from updater import choose_asset,safe_name,PROJECTS
class TrackerTests(unittest.TestCase):
 def test_bin_asset_selected(self):
  assets=[{'name':'PS5CEMU-v3.zip','browser_download_url':'https://github.com/a/b/releases/download/v3/PS5CEMU-v3.zip'},
          {'name':'debug-symbols.zip','browser_download_url':'https://github.com/a/b/releases/download/v3/debug-symbols.zip'}]
  self.assertEqual(choose_asset({'assets':assets})['name'],'PS5CEMU-v3.zip')
 def test_does_not_choose_source_only(self):
  self.assertIsNone(choose_asset({'assets':[{'name':'source-code.zip','browser_download_url':'https://github.com/a/b/releases/download/a/source-code.zip'}]}))
 def test_spoofed_github_host_refused(self):
  self.assertIsNone(choose_asset({'assets':[{'name':'update.zip','browser_download_url':'https://github.com.evil.example/releases/download/a/update.zip'}]}))
 def test_traversal_refused(self):
  with self.assertRaises(ValueError):safe_name('../evil.zip')
 def test_allowlist(self): self.assertEqual(len(PROJECTS),5)
if __name__=='__main__': unittest.main()
