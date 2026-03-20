## Forex Market Analysis and Trading Strategies

This project analyzes forex markets and explores potential trading ideas.

### Setup

```bash
uv sync
```

### Quick check

```bash
uv run python -c "import forex_analysis; print(forex_analysis.__version__)"
```

### Run from `src` (no notebook)

Put these files in `data/`:
- `fx_rate_daily.csv`
- `interest_rate_daily.csv`

Run:

```bash
uv run forex-analysis --data-dir data
```

Optional: save outputs

```bash
uv run forex-analysis --data-dir data --out-dir outputs
```

### Notebook usage

Notebook logic now uses reusable functions from `src/forex_analysis/core.py`.
Put your CSV files in a local `data/` folder (or edit the path in the notebook), then open:

```bash
uv run jupyter notebook forex_pair_trading.ipynb
```

### Run tests

```bash
uv run python -m unittest discover -s tests -v
```
