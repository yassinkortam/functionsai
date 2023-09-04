class TestFunction:

    def test_function_name(self, function, function_without_prompt):
        assert function_without_prompt.name == function.__name__

    def test_function_description(self, function, function_without_prompt):
        assert function_without_prompt.description == function.__doc__

    def test_function_prompts(self, function_with_prompt, prompts):
        assert function_with_prompt.prompts == prompts
    
    def test_function_function(self, function, function_without_prompt):
        assert function_without_prompt.function == function

    def test_function_without_prompt(self, function_without_prompt):
        assert function_without_prompt.prompts == None
    
    def test_function_equivalence(self, function_with_prompt, function_without_prompt):
        assert function_without_prompt != function_with_prompt
        assert function_without_prompt == function_without_prompt
        assert function_with_prompt == function_with_prompt
