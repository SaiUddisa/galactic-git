from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from nodes.is_code_identified import is_code_identified
from nodes.fix_and_push import fix_and_push
from nodes.find_solution import find_solution
from nodes.find_culprit_files import find_culprit_files
from state import State
from nodes.issue_selection import issue_selection_node 


workflow = StateGraph(State)

#node registration
workflow.add_node("issue_selection", issue_selection_node)
workflow.add_node("cultprit_identification", find_culprit_files)
workflow.add_node("solution_generation", find_solution)
workflow.add_node("apply_changes",fix_and_push )
#node orchestration
workflow.add_edge(START, "issue_selection")
workflow.add_edge("issue_selection", "cultprit_identification")
workflow.add_conditional_edges(
    "cultprit_identification",is_code_identified  
)

workflow.add_edge("solution_generation", "apply_changes")
workflow.add_edge("apply_changes", END)



















app = workflow.compile()

ASCII_ART = r"""
  ____       _            _   _        ____ _ _   
 / ___| __ _| | __ _  ___| |_(_) ___  / ___(_) |_ 
| |  _ / _` | |/ _` |/ __| __| |/ __|| |  _| | __|
| |_| | (_| | | (_| | (__| |_| | (__ | |_| | | |_ 
 \____|\__,_|_|\__,_|\___|\__|_|\___| \____|_|\__|
"""

if __name__ == "__main__":
    load_dotenv()
    initial_state = {
        "issue_title": "", 
        "issue_description": ""
    }
    print(ASCII_ART) 
    final_state=app.invoke(initial_state)
    print("\n--- Workflow Complete ---")
    