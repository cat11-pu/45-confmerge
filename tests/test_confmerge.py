import unittest

from confmerge import ConfigMerger
from configapi import Config


class TestConfigMerger(unittest.TestCase):
    def test_layers_count(self):
        merger = ConfigMerger()
        self.assertEqual(merger.load("base", {"a": 1})["layers"], 1)

    def test_shallow_override(self):
        merger = ConfigMerger()
        merger.load("base", {"a": 1})
        merger.load("prod", {"a": 2})
        self.assertEqual(merger.merged()["a"], 2)

    def test_diff_keys(self):
        merger = ConfigMerger()
        merger.load("base", {"a": 1})
        merger.load("prod", {"b": 2})
        self.assertEqual(merger.diff("base", "prod")["only_right"], ["b"])

    def test_stats_shape(self):
        self.assertIn("layers", ConfigMerger().stats())

    def test_config_wraps_merger(self):
        config = Config()
        config.load("base", {"a": 1})
        self.assertEqual(config.merger.stats()["layers"], 1)


if __name__ == "__main__":
    unittest.main()
