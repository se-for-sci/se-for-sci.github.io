def simple_typed_function(x: float) -> float:
    return x * 2


def simple_untyped_function(x):
    return x * 2


input_value = ["hi"]
print(simple_typed_function(input_value))
print(simple_untyped_function(input_value))
