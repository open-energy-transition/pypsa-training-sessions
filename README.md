# PyPSA Statistics Training

A guided ~40-min Jupyter notebook session exploring `n.statistics` — PyPSA's high-level API for querying costs, capacities, energy flows, and market metrics from optimized networks.

Uses `pypsa.examples.carbon_management()`, a sector-coupled European energy system from a [Nature Energy paper](https://www.nature.com/articles/s41560-025-01752-6) on H₂/CO₂ network strategies (2164 buses, 89 carriers, 20 days at 3h resolution).

## Topics Covered

| Category | Methods |
|---|---|
| **Costs** | `capex()`, `opex()`, `system_cost()` |
| **Capacity** | `installed_capacity()`, `optimal_capacity()`, `expanded_capacity()`, `capacity_factor()` |
| **Energy** | `supply()`, `withdrawal()`, `energy_balance()`, `transmission()`, `curtailment()` |
| **Market** | `prices()`, `revenue()`, `market_value()` |
| **Groupby & Filtering** | `groupby`, `groupby_time`, `components`, `carrier`, custom groupers |
| **Plotting** | `.plot.bar()`, `.iplot.area()`, and more |

## Setup

```bash
uv sync
```

## Run

```bash
uv run jupyter lab notebooks/pypsa_statistics.ipynb
```

## Test

```bash
uv sync --extra dev
uv run pytest tests/
```
