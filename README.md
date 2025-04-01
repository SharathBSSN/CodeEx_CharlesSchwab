# Code Challenge w/Charles_Schwab :- System Health Check API

This project implements a Python web API that analyzes the health of a system represented as a Directed Acyclic Graph (DAG). The system's structure and dependencies are defined in a JSON file, and the API provides a comprehensive health assessment, including a table of component health statuses and a visual representation of the DAG.

## Problem Statement

The goal is to develop a web API that:

1.  **Accepts a JSON file** describing a system's components and their dependencies in a DAG format.
2.  **Traverses the DAG** using Breadth-First Search (BFS).
3.  **Asynchronously checks** the health of each component.
4.  **Generates a table** displaying the health status of each component.
5.  **Visualizes the DAG** and highlights failed components in red, saving each visualization as a unique PNG file.

## Approach

The solution involves the following steps:

1.  **JSON Parsing and DAG Construction:**
    * The API receives a JSON file through a POST request.
    * The JSON data is parsed to create a dictionary.
2.  **Breadth-First Search (BFS) Traversal:**
    * BFS is used to traverse the DAG, ensuring all components are visited in a level-by-level order.
    * The traversal starts from the root nodes (nodes with no incoming edges).
3.  **Asynchronous Health Checks:**
    * For each component visited during BFS, an asynchronous call is made to a `check_component_health` function (or service).
    * `asyncio` is used to handle concurrent health checks, improving performance.
4.  **Health Result Storage:**
    * The health status of each component is stored in a dictionary, mapping component IDs to their health (True for healthy, False for unhealthy).
5.  **Table Output Generation:**
    * The health results are formatted into a human-readable table, displaying component IDs and their health statuses.
6.  **DAG Visualization:**
    * The `networkx` and `matplotlib` libraries are used to visualize the DAG.
    * Failed components (unhealthy) are highlighted in red.
    * Each visualization is saved as a unique PNG file in the `visualize_dag` folder, using a timestamp to generate unique filenames.

## Solution

The solution is implemented using Python with the following libraries:

* **`Flask`:** For creating the web API.
* **`asyncio`:** For asynchronous health checks.
* **`networkx`:** For graph operations and visualization.
* **`matplotlib`:** For plotting the graph.

### Code Structure

    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── test_app.py
    ├── curl_commands.txt
    └── (++ created result dirs -> health_results, visualize_dag)

* **`app.py`:** Contains the Flask application and the logic for parsing the JSON, traversing the DAG, checking health, and generating the output.
* **`README.md`:** This file.
* **`requirements.txt`:** Lists the project's dependencies.
* **`test_app.py`:** PyTest module containg test cases covering different scenarios and edge cases.
* **`curl_commands.txt`:** Lists the curl commands for pytest cases.

### Running the API

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd CodeEx_CharlesSchwab
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**

    ```bash
    python app.py
    ```

5.  **Run the pytest**

    ```bash
    pytest test_app.py
    ```
