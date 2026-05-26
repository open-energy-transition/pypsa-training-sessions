"""Temporary workarounds for pypsa 1.2.1 plotting bugs. Remove once fixed upstream."""

import pandas as pd
import plotly.graph_objects as go

_orig_show = go.Figure._ipython_display_


def _is_categorical(yaxis_name: str, fig: go.Figure) -> bool:
    ax = fig.layout[yaxis_name]
    if ax.type in ("category", "multicategory"):
        return True
    if ax.type in ("linear", "log", "date"):
        return False
    suffix = yaxis_name.removeprefix("yaxis")
    target = "y" + suffix
    for tr in fig.data:
        if (tr.yaxis or "y") == target and tr.y is not None and len(tr.y):
            return isinstance(tr.y[0], str)
    return False


def _show(self: go.Figure):
    for name in self.layout:
        if name.startswith("yaxis") and _is_categorical(name, self):
            self.layout[name].update(tickmode="linear", dtick=1)
    return _orig_show(self)


go.Figure._ipython_display_ = _show


def suppress_pypsa_copy_warning() -> None:
    import warnings
    warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning, module="pypsa")
