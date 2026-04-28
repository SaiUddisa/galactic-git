from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from nodes.find_culprit_files import find_culprit_files
from state import State
from nodes.issue_selection_node import issue_selection_node 


workflow = StateGraph(State)

#node registration
workflow.add_node("selection", issue_selection_node)
workflow.add_node("cultprit_identification", find_culprit_files)
#node orchestration
workflow.add_edge(START, "selection")
workflow.add_edge("selection", "cultprit_identification")
workflow.add_edge("cultprit_identification", END)



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