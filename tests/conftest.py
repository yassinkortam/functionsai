import pytest
import pandas as pd
from functionsai import Function
from functionsai import Module

@pytest.fixture
def function():
    def plot(x : pd.Series)->None:
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
    class TestModule:
        def plot(x : pd.Series)->None:
            """
            This function plots a graph given a timeseries.
            """
            x.plot()
    return TestModule

@pytest.fixture
def module_with_prompt(module, prompts):
    return Module(module, prompts)

@pytest.fixture
def module_without_prompt(module):
    return Module(module)

