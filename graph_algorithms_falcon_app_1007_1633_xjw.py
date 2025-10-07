# 代码生成时间: 2025-10-07 16:33:00
import falcon
from falcon import API
from collections import defaultdict
import heapq

# Define a graph class to handle graph operations
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # defaultdict for adjacency list

    # Function to add an edge to the graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)  # Since the graph is undirected

    # Implementation of Dijkstra's algorithm
    def dijkstra(self, src):
        '''
        This function performs Dijkstra's algorithm to find the shortest distance from the source vertex to all other vertices.
        It returns a dictionary with vertices as keys and their shortest distances as values.
        '''
        dist = {node: float("inf") for node in self.graph}
        dist[src] = 0
        pq = [(0, src)]  # min-heap

        while pq:
            d, u = heapq.heappop(pq)
            for v in self.graph[u]:
                new_dist = d + 1  # Distance to v is sum of distances of u and edge (u, v)
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))

        return dist

# Falcon API resource for graph
class GraphResource:
    def on_get(self, req, resp):
        '''
        Handles GET requests to demonstrate the graph with its vertices and edges.
        '''
        graph = Graph(5)  # Example graph with 5 vertices
        graph.addEdge(0, 1)
        graph.addEdge(0, 4)
        graph.addEdge(1, 2)
        graph.addEdge(1, 3)
        graph.addEdge(1, 4)
        graph.addEdge(2, 3)
        graph.addEdge(3, 4)

        resp.media = {
            "vertices": list(graph.graph.keys()),
            "edges": [(u, v) for u in graph.graph for v in graph.graph[u]]
        }

    def on_post(self, req, resp):
        '''
        Handles POST requests to run Dijkstra's algorithm.
        The request body should contain the source vertex from which to start the algorithm.
        '''
        try:
            data = req.media or {}
            src = data.get("src", None)
            if src is None:
                raise ValueError("Source vertex is required")
            graph = Graph(5)  # Example graph with 5 vertices
            graph.addEdge(0, 1)
            graph.addEdge(0, 4)
            graph.addEdge(1, 2)
            graph.addEdge(1, 3)
            graph.addEdge(1, 4)
            graph.addEdge(2, 3)
            graph.addEdge(3, 4)

            shortest_distances = graph.dijkstra(src)
            resp.media = shortest_distances
            resp.status = falcon.HTTP_200
        except ValueError as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400

# Create an API instance
api = API()

# Add the GraphResource to the API
api.add_route("/graph", GraphResource())
