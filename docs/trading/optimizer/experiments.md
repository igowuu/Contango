# Experiments

Experiments permit for many parameters to be run for a given strategy and the results to be easily obtainable afterwords for each backtest.

# Backtest Experiment

The `BacktestExperiment` is a tuple that allows the same strategy to be used with configurable parameters. It creates an instance of the same strategy per parameter combination given.

See [experiments reference](../../reference/trading/optimizer/experiments/backtest_experiment.md)

# Backtest Experiment Result

A `BacktestExperimentResult` is the resulting tuple after running an experiment. It contains the raw execution data (the raw events generated from the backtester), the metrics for the backtest (from the optimizer), and the underlying `BacktestExperiment` instance that it attaches to.

See [experiment result reference](../../reference/trading/optimizer/experiments/backtest_experiment_result.md)

# Backtest Experiment Runner

`BacktestExperimentRunner` loops through all the possible parameter combinations given a list of `BacktestExperiment` instances and returns a list of `BacktestExperimentResult` tuples. 

See [experiments reference](../../reference/trading/optimizer/experiments/backtest_experiment_runner.md)

This all essentially allows for a parameter grid to be easily tested through a grid of parameters, also wrapping the metric API and backtest API so that the user doesn't need to interact with low-level components themselves. 
