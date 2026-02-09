import matplotlib.pyplot as plt
import pandas as pd
import pytest

import pypsa


@pytest.fixture(scope="module")
def n() -> pypsa.Network:
    return pypsa.examples.carbon_management()


def test_network_loads(n: pypsa.Network) -> None:
    assert len(n.buses) > 2000
    assert len(n.carriers) > 50
    assert len(n.snapshots) > 0


def test_statistics_summary(n: pypsa.Network) -> None:
    s = n.statistics()
    assert isinstance(s, pd.DataFrame)
    assert s.shape[0] > 10
    for col in ["Capital Expenditure", "Optimal Capacity", "Supply"]:
        assert col in s.columns


def test_capex_nonnegative(n: pypsa.Network) -> None:
    capex = n.statistics.capex()
    assert (capex >= 0).all()


def test_opex_finite(n: pypsa.Network) -> None:
    opex = n.statistics.opex()
    assert opex.notna().all()
    assert len(opex) > 0


def test_energy_balance_sums(n: pypsa.Network) -> None:
    eb = n.statistics.energy_balance()
    total = eb.sum()
    assert abs(total) < abs(eb).sum() * 0.01


def test_capacity_factor_range(n: pypsa.Network) -> None:
    cf = n.statistics.capacity_factor().dropna()
    assert len(cf) > 0
    assert (cf >= 0).all()
    assert (cf <= 1).all()


def test_groupby_variants(n: pypsa.Network) -> None:
    by_carrier = n.statistics.capex(groupby="carrier")
    assert isinstance(by_carrier, pd.Series)
    assert len(by_carrier) > 0
    assert by_carrier.index.get_level_values(-1).name == "carrier"

    by_country = n.statistics.capex(groupby="country")
    assert isinstance(by_country, pd.Series)
    assert len(by_country) > 0
    assert by_country.index.get_level_values(-1).name == "country"

    by_multi = n.statistics.capex(groupby=["bus_carrier", "carrier"])
    assert isinstance(by_multi, pd.Series)
    assert len(by_multi) > 0
    assert "bus_carrier" in by_multi.index.names and "carrier" in by_multi.index.names


def test_time_series_mode(n: pypsa.Network) -> None:
    ts = n.statistics.energy_balance(groupby_time=False)
    assert isinstance(ts, pd.DataFrame)
    assert isinstance(ts.columns, pd.DatetimeIndex)
    assert ts.shape[1] == len(n.snapshots)


def test_component_filter(n: pypsa.Network) -> None:
    gen_only = n.statistics.supply(components=["Generator"])
    assert all(c == "Generator" for c, _ in gen_only.index)


def test_carrier_filter(n: pypsa.Network) -> None:
    cf = n.statistics.capacity_factor(carrier="solar")
    assert len(cf) > 0
    assert all("Solar" in str(idx) for idx in cf.index)


def test_plotting_methods_exist(n: pypsa.Network) -> None:
    assert callable(n.statistics.capex.plot.bar)
    assert callable(n.statistics.energy_balance.plot.bar)
    assert callable(n.statistics.energy_balance.iplot.area)
    assert callable(n.statistics.optimal_capacity.plot.bar)


def test_system_cost_consistency(n: pypsa.Network) -> None:
    capex = n.statistics.capex()
    opex = n.statistics.opex()
    system_cost = n.statistics.system_cost()
    combined = capex.add(opex, fill_value=0)
    common = system_cost.index.intersection(combined.index)
    pd.testing.assert_series_equal(
        system_cost.loc[common], combined.loc[common], rtol=1e-5
    )


def test_installed_and_expanded_capex(n: pypsa.Network) -> None:
    installed = n.statistics.installed_capex()
    expanded = n.statistics.expanded_capex()
    capex = n.statistics.capex()
    assert (installed >= 0).all()
    assert (expanded >= 0).all()
    combined = installed.add(expanded, fill_value=0)
    common = capex.index.intersection(combined.index)
    pd.testing.assert_series_equal(
        capex.loc[common], combined.loc[common], rtol=1e-5
    )


def test_capacity_relationship(n: pypsa.Network) -> None:
    installed = n.statistics.installed_capacity()
    optimal = n.statistics.optimal_capacity()
    expanded = n.statistics.expanded_capacity()
    combined = installed.add(expanded, fill_value=0)
    common = optimal.index.intersection(combined.index)
    pd.testing.assert_series_equal(
        optimal.loc[common], combined.loc[common], rtol=1e-5
    )


def test_transmission(n: pypsa.Network) -> None:
    tr = n.statistics.transmission()
    assert len(tr) > 0
    assert tr.notna().all()


def test_curtailment_nonnegative(n: pypsa.Network) -> None:
    curt = n.statistics.curtailment()
    assert (curt >= 0).all()


def test_prices_structure(n: pypsa.Network) -> None:
    prices = n.statistics.prices()
    assert isinstance(prices, pd.Series)
    assert len(prices) > 0
    assert prices.dropna().size > 100


def test_revenue_and_market_value(n: pypsa.Network) -> None:
    rev = n.statistics.revenue()
    mv = n.statistics.market_value()
    assert len(rev) > 0
    assert len(mv) > 0
    assert rev.notna().all()
    assert mv.dropna().notna().all()


def test_custom_grouper(n: pypsa.Network) -> None:
    from pypsa.statistics import groupers

    def simple_type(n, c, port=""):
        return pd.Series("all", index=n.c[c].static.index, name="type")

    groupers.add_grouper("simple_type", simple_type)
    result = n.statistics.capex(groupby="simple_type")
    assert len(result) > 0
    assert result.index.get_level_values("type").unique().tolist() == ["all"]


def test_groupby_time_variants(n: pypsa.Network) -> None:
    s_sum = n.statistics.supply(groupby_time="sum")
    s_mean = n.statistics.supply(groupby_time="mean")
    assert len(s_sum) > 0
    assert len(s_mean) > 0
    assert not s_sum.equals(s_mean)


def test_plotting_renders(n: pypsa.Network) -> None:
    n.statistics.capex.plot.bar()
    plt.close("all")
