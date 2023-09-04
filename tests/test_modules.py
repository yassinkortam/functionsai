from functionsai import Function
import inspect

class TestModules:

    def test_modules_name(self, module, module_without_prompt):
        assert module_without_prompt.name == module.__name__
    
    def test_modules_description(self, module, module_without_prompt):
        assert module_without_prompt.description == module.__doc__
    
    def test_modules_module(self, module, module_without_prompt):
        assert module_without_prompt.module == module
    
    def test_modules_prompts(self, module_with_prompt, prompts):
        assert module_with_prompt.prompts == prompts
        
    def test_modules_without_prompt(self, module_without_prompt):
        assert module_without_prompt.prompts == None
    
    def test_modules_functions(self, module, module_without_prompt):
        assert module_without_prompt.functions == [Function(function) for name, function in inspect.getmembers(module, inspect.isfunction)]