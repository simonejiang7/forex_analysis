"""Basic smoke tests for the package."""

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestSmoke(unittest.TestCase):
    def test_import_and_version(self) -> None:
        import forex_analysis

        self.assertEqual(forex_analysis.__version__, "0.1.0")

    def test_core_helper(self) -> None:
        from forex_analysis.core import package_name

        self.assertEqual(package_name(), "forex_analysis")

    def test_prepare_major_pairs(self) -> None:
        from forex_analysis.core import prepare_major_pairs

        try:
            import pandas as pd
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"pandas is not available in this environment: {exc}")

        df = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "dexeuus": [1.10, 1.11],
                "dexukus": [1.30, 1.31],
                "dexszus": [1.05, 1.04],
            }
        )
        out = prepare_major_pairs(df)
        self.assertEqual(list(out.columns), ["date", "eur", "gbp", "chf"])
        self.assertEqual(len(out), 2)


if __name__ == "__main__":
    unittest.main()
