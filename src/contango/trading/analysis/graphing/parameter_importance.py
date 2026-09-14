# parameter_importance.py
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.express as px  # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


def compute_parameter_importance(
    df: pd.DataFrame,
    target_metric: str,
    param_columns: list[str],
) -> pd.DataFrame:
    """
    Scores each parameter's importance to target_metric using an
    eta-squared measure.

    Args:
        df: Experiment DataFrame.
        target_metric: The metric column to explain (e.g. "calmar_ratio").
        param_columns: Parameter columns to score.

    Returns:
        DataFrame with columns ["parameter", "importance"], sorted descending.
    """
    plot_df = df.dropna(subset=[target_metric])
    grand_mean = plot_df[target_metric].mean()
    ss_total = ((plot_df[target_metric] - grand_mean) ** 2).sum()

    scores: list[dict[str, str | float]] = []
    for param in param_columns:
        group_stats = plot_df.groupby(param)[target_metric].agg(["mean", "count"])
        ss_between = (group_stats["count"] * (group_stats["mean"] - grand_mean) ** 2).sum()
        importance = float(ss_between / ss_total) if ss_total > 0 else 0.0
        scores.append({"parameter": param, "importance": importance})

    return pd.DataFrame(scores).sort_values("importance", ascending=False).reset_index(drop=True)


@dataclass(frozen=True, slots=True)
class ParameterImportanceConfig(GraphConfig):
    """
    A graph configuration specific to the parameter importance graph.

    Attributes:
        param_columns: The parameter columns to score.
        target_metric: The name for the targeted metric to explain.
    """
    param_columns: list[str]
    target_metric: str = "calmar_ratio"


@register_graph("parameter_importance")
class ParameterImportance(GraphType[ParameterImportanceConfig]):
    """
    A graph type that shows the sensitivity of a metric to each swept parameter.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds the parameter importance bar chart.

        Args:
            df: The tidy experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        importance_df = compute_parameter_importance(df, self.config.target_metric, self.config.param_columns)

        fig = px.bar(   # type: ignore[unknownMemberType]
            importance_df,
            x="importance",
            y="parameter",
            orientation="h",
            title=f"Parameter Importance: sensitivity of {self.config.target_metric} to each parameter",
            labels={"importance": "Relative Importance (eta²)", "parameter": "Parameter"},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})  # type: ignore[unknownMemberType]
        return fig
