from state import State


def is_code_identified(state:State):
    if not state.related_code :
        return "cultprit_identification"
    else:
        return "solution_generation"