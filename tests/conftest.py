import pytest
import pandas as pd
import functionsai as fai
from functionsai import FunctionsAI, Function, Module, Scoring
import inspect


@pytest.fixture
def function():
    def plot(x: pd.Series) -> None:
        """
        This function plots a graph given a timeseries.
        """
        x.plot()

    return plot


@pytest.fixture
def prompts():
    return ["Make a plot of this timeseries"]


@pytest.fixture
def function_with_prompt(function, prompts):
    return Function(function, prompts)


@pytest.fixture
def function_without_prompt(function):
    return Function(function)


@pytest.fixture
def module():
    return fai


@pytest.fixture
def module_without_prompt(module):
    return Module(module)


@pytest.fixture
def functionsai(function):
    return FunctionsAI(fai, function)
