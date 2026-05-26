# PyPSA Training Sessions

This repo serves as a collection point for different PyPSA training sessions. It is organized into several notebooks, each focusing on a specific aspect of PyPSA.


## 1. PyPSA Statistics Training (40 min)

A guided ~40-min Jupyter notebook session exploring `n.statistics` — PyPSA's high-level API for querying costs, capacities, energy flows, and market metrics from optimized networks.

Uses `pypsa.examples.carbon_management()`, a sector-coupled European energy system from a [Nature Energy paper](https://www.nature.com/articles/s41560-025-01752-6) on H₂/CO₂ network strategies (2164 buses, 89 carriers, 20 days at 3h resolution).

### Topics Covered

| Category | Methods |
|---|---|
| **Costs** | `capex()`, `opex()`, `system_cost()` |
| **Capacity** | `installed_capacity()`, `optimal_capacity()`, `expanded_capacity()`, `capacity_factor()` |
| **Energy** | `supply()`, `withdrawal()`, `energy_balance()`, `transmission()`, `curtailment()` |
| **Market** | `prices()`, `revenue()`, `market_value()` |
| **Groupby & Filtering** | `groupby`, `groupby_time`, `components`, `carrier`, custom groupers |
| **Plotting** | `.plot.bar()`, `.iplot.area()`, and more |

## 2. Statistics Plotting (40 min)

A follow-up ~40-min notebook on the `.plot` (matplotlib/seaborn) and `.iplot` (plotly) accessors that every `n.statistics.<method>` exposes. Same `carbon_management()` network as session 1.

### Topics Covered

| Category | Details |
|---|---|
| **`.plot` vs `.iplot`** | backend comparison, supported plot types |
| **Bar / Line / Area** | horizontal/stacked bars, time-series lines, stacked dispatch areas |
| **Filtering & Layout** | `carrier`, `bus_carrier`, `query`, `x`/`y`/`color`/`facet_col`/`facet_row` |
| **Extra kwargs** | sizing (`height`, `aspect`, `width`), faceting (`facet_col_wrap`), labels, titles |
| **Drop to axes** | unpacking `(fig, ax, g)` / plotly `Figure` for post-hoc customization |
| **Spatial maps** | `.plot.map` — bus circles, branch widths, flow arrows, split half-circles, legend control |

## Setup

```bash
uv sync
```

## Run

```bash
uv run jupyter lab notebooks/pypsa_statistics.ipynb        # session 1
uv run jupyter lab notebooks/pypsa_statistics_plotting.ipynb  # session 2
```

## Test

```bash
uv sync --extra dev
uv run pytest tests/
```
