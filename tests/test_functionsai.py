import inspect
from functionsai import Function


class TestFunctionsAI:
    def test_functions(self, function_without_prompt, functionsai):
        assert all(
            [
                f1 == f2
                for f1, f2 in zip(
                    functionsai.functions, [function_without_prompt]
                )
            ]
        )

    def test_modules(self, module_without_prompt, functionsai):
        assert all(
            [
                m1 == m2
                for m1, m2 in zip(functionsai.modules, [module_without_prompt])
            ]
        )

    def test_sort_functions(self, function, module, functionsai):
        sorted_functions = functionsai.sort_functions(
            "Get the callable function"
        )
        sorted_functions_list = [func for func, score in sorted_functions]

        module_functions = [
            Function(member)
            for name, member in inspect.getmembers(module)
            if inspect.isfunction(member) and not name.startswith("_")
        ]
        all_functions = module_functions + [Function(function)]

        assert len(all_functions) == len(sorted_functions_list)
