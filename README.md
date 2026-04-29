```text
  ____       _            _   _        ____ _ _
 / ___| __ _| | __ _  ___| |_(_) ___  / ___(_) |_
| |  _ / _` | |/ _` |/ __| __| |/ __|| |  _| | __|
| |_| | (_| | | (_| | (__| |_| | (__ | |_| | | |_
 \____|\__,_|_|\__,_|\___|\__|_|\___| \____|_|\__|
```

Galactic Git is an automated issue resolution agent built with LangGraph, LangChain, and Ollama. It orchestrates an end-to-end workflow to autonomously identify, analyze, and fix code issues, ultimately pushing the applied changes to a repository.

## Features

- Automated Workflow: Leverages a state graph to sequentially handle issues from start to finish.
- Issue Selection: Extracts and processes the title and description of a given issue.
- Culprit Identification: Analyzes the project's directory structure to pinpoint related files and specific lines of code using grep commands.
- Solution Generation: Plans a strategy and formulates the exact sed commands required to fix the identified bugs.
- Application and Commit: Automatically applies the changes to the files, generates an appropriate commit message, and pushes the code to a new branch.

## Architecture

The project is structured as a LangGraph state machine with the following nodes:

1. Issue Selection: Initializes the state with issue details.
2. Culprit Identification: Finds the files causing the issue.
3. Solution Generation: Generates the necessary fixes (sed commands).
4. Apply Changes: Executes the fixes and commits/pushes the changes.

## Prerequisites

- Python 3.8+
- Ollama (running locally or accessible via network)
- Git installed and configured

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd galactic-git
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and add any necessary configuration keys (e.g., GitHub tokens, LLM API keys if extending beyond local Ollama).

## Usage

Run the main orchestrator script:

```bash
python main.py
```

The script will invoke the LangGraph workflow, process the initial state (which can be modified in `main.py`), and automatically iterate through the issue resolution steps.

## Sample .env

```
GITHUB_TOKEN=your-personal-access-token
OLLAMA_BASE_URL=your-ollama-url
PROJECT_PATH=project-path
OWNER=your-github-profile-name
REPO=your-repo-name
BASE_BRANCH=master/main/your-custom-branch
```

## Directory Structure

- `main.py`: Entry point for defining and running the LangGraph workflow.
- `state.py`: Defines the Pydantic data structures for the workflow state.
- `nodes/`: Contains the individual processing steps (issue selection, culprit identification, solution generation, etc.).
- `tools/`: Helper modules and tool implementations used by the nodes.
- `client/`: Client-side logic or UI components (if applicable).
