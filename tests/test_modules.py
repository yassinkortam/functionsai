from functionsai import Function, Module
import inspect


class TestModules:
    def test_modules_name(self, module, module_without_prompt):
        assert module_without_prompt.name == module.__name__

    def test_modules_description(self, module, module_without_prompt):
        assert module_without_prompt.description == module.__doc__

    def test_modules_module(self, module, module_without_prompt):
        assert module_without_prompt.module == module

    def test_modules_without_prompt(self, module_without_prompt):
        assert module_without_prompt.prompts == None

    def test_modules_structure(self, module, module_without_prompt):
        # Check top-level properties
        assert module_without_prompt.name == module.__name__
        assert module_without_prompt.description == module.__doc__

        # Check top-level functions
        module_functions = [
            member
            for name, member in inspect.getmembers(module, inspect.isfunction)
        ]
        assert len(module_functions) == len(module_without_prompt.functions)
        for func in module_functions:
            assert any(
                isinstance(f, Function) and f.function == func
                for f in module_without_prompt.functions
            )

        # Check submodules
        submodules = [
            member
            for name, member in inspect.getmembers(module, inspect.ismodule)
            if member.__name__.startswith(module.__name__)
        ]
        assert len(submodules) == len(module_without_prompt.submodules)
        for sub in submodules:
            assert any(
                isinstance(m, Module) and m.module == sub
                for m in module_without_prompt.submodules
            )

    def test_modules_equivalence(self, module, module_without_prompt):
        new_module = Module(module)
        assert module_without_prompt == module_without_prompt
        assert module_without_prompt == new_module
