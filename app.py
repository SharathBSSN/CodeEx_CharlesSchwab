from flask import Flask, request, Response
import asyncio
import networkx as nx
import matplotlib.pyplot as plt
import time
import os

app = Flask(__name__)

async def check_component_health(component_id):
    """Simulates checking the health of a component asynchronously."""
    await asyncio.sleep(0.1)
    import random
    return random.choice([True, False])

def build_dag(json_data):
    """Builds a DAG from the JSON data."""
    dag = {}
    for node, dependencies in json_data.items():
        dag[node] = dependencies
    return dag

async def get_system_health(dag):
    """Traverses the DAG and checks the health of each component."""
    visited = set()
    queue = [node for node, deps in dag.items() if not any(node in deps for deps in dag.values())]
    health_results = {}

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            health_results[node] = await check_component_health(node)
            for child, deps in dag.items():
                if child in dag[node]:
                    queue.append(child)

    return health_results

def format_health_results_csv(health_results):
    """Formats the health results into CSV data."""
    csv_data = "Component,Health\n"
    for component, health in health_results.items():
        csv_data += f"{component},{'Healthy' if health else 'Unhealthy'}\n"
    return csv_data

def visualize_dag(dag, health_results):
    """Visualizes the DAG with failed components highlighted in red."""
    G = nx.DiGraph(dag)
    pos = nx.spring_layout(G)
    colors = ['red' if not health_results.get(node, True) else 'lightblue' for node in G.nodes()]
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1500, arrowsize=20)
    
    folder_name = "visualize_dag"
    os.makedirs(folder_name, exist_ok=True)
    
    timestamp = int(time.time())
    filename = os.path.join(folder_name, f'dag_visualization_{timestamp}.png')
    
    plt.savefig(filename)
    plt.close()
    
    return filename

@app.route('/health', methods=['POST'])
async def health_check():
    """Web API endpoint for health check."""
    try:
        json_data = request.get_json()
        dag = build_dag(json_data)
        health_results = await get_system_health(dag)
        table = format_health_results_csv(health_results)

        csv_folder = "health_results"
        os.makedirs(csv_folder, exist_ok=True)

        csv_filename = os.path.join(csv_folder, f'health_results_{int(time.time())}.csv')

        with open(csv_filename, 'w') as csvfile:
            csvfile.write(table)

        visualization_filename = visualize_dag(dag, health_results)

        return Response(f"CSV Saved to: {csv_filename}\nVisualization Path: {visualization_filename}", mimetype="text/plain")

    except Exception as e:
        return Response(f"Error: {str(e)}", mimetype="text/plain"), 400

if __name__ == '__main__':
    app.run(debug=True)