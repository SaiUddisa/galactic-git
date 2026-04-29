from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from nodes.find_solution import find_solution
from nodes.find_culprit_files import find_culprit_files
from state import State
from nodes.issue_selection import issue_selection_node 


workflow = StateGraph(State)

#node registration
workflow.add_node("issue_selection", issue_selection_node)
workflow.add_node("cultprit_identification", find_culprit_files)
workflow.add_node("solution_generation", find_solution)
#node orchestration
workflow.add_edge(START, "issue_selection")
workflow.add_edge("issue_selection", "cultprit_identification")
workflow.add_edge("cultprit_identification", "solution_generation")
workflow.add_edge("solution_generation", END)



app = workflow.compile()


if __name__ == "__main__":
    load_dotenv()
    initial_state = {
        "issue_title": "", 
        "issue_description": ""
    }
    
    final_state=app.invoke(initial_state)
    print("\n--- Workflow Complete ---")
    print(f"Final Status: {final_state}")
#     # This prints a text-based ASCII representation of your flow
# print(app.get_graph().draw_ascii())