from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Percentage_Exact import Safe_Float__Percentage_Exact


class Safe_Float__Temperature(Safe_Float__Percentage_Exact):        # Temperature parameter for LLM (0.0 to 2.0 typically)
    min_value = 0.0
    max_value = 2.0