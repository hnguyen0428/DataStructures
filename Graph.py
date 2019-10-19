import sys
from collections import Iterable, deque, defaultdict
from DataStructures import PriorityQueue, LinkedDict

class GraphEdge(object):
    def __init__(self, id1, id2, weight=1):
        self.src = id1
        self.dest = id2
        self.weight = weight

    def __lt__(self, other):
        return self.dest < other.dest

    def __eq__(self, other):
        return self.dest == other.dest

    def __gt__(self, other):
        return self.dest > other.dest

    def __str__(self):
        return '(%s, %s)' % (str(self.src), str(self.dest))

    def __repr__(self):
        return self.__str__()

class GraphNode(object):
    def __init__(self, id):
        self.id = id
        self.data = {}
        self.edges = {}

    def __hash__(self):
        return hash(self.id)

    def addEdge(self, edge):
        assert isinstance(edge, GraphEdge)
        self.edges[edge.dest] = edge
        return self

    def hasEdge(self, dest):
        return dest in self.edges

    def getEdge(self, dest):
        return self.edges[dest]

    def setData(self, key, val):
        self.data[key] = val
        return self

    def removeData(self, key):
        del self.data[key]
        return self

    def iteredges(self, inorder=False, reverse=False):
        if inorder:
            sorted_edges = sorted(self.edges.itervalues(), reverse=reverse)
            return iter(sorted_edges)
        else:
            return self.edges.itervalues()

class Graph(object):
    ID_NOT_IN_GRAPH = 0

    def __init__(self):
        self.nodes = {}

    def __iter__(self):
        return iter(self.nodes.itervalues())

    def __getitem__(self, key):
        return self.nodes[key]

    def error(self, code, data):
        if code == Graph.ID_NOT_IN_GRAPH:
            raise Exception("Node with id %s is not in the graph" % str(data['id']))
        else:
            raise Exception("Unknown error")

    def checkValidIdsOrException(self, ids):
        for id in ids:
            if id not in self.nodes:
                self.error(Graph.ID_NOT_IN_GRAPH, {'id': id})

    def setNodeData(self, id, data):
        if id in self.nodes:
            for key, val in data.iteritems():
                self.nodes[id].setData(key, val)
        else:
            self.error(Graph.ID_NOT_IN_GRAPH, {'id': id})

    def removeNodeData(self, id, keys):
        if id in self.nodes:
            for key in keys:
                self.nodes[id].removeData(key)
        else:
            self.error(Graph.ID_NOT_IN_GRAPH, {'id': id})

    def addNodeIfNotExist(self, id):
        if id not in self.nodes:
            newNode = GraphNode(id)
            self.nodes[id] = newNode

    def addEdge(self, id1, id2, weight=1):
        self.checkValidIdsOrException([id1, id2])
        edge = GraphEdge(id1, id2, weight)
        self.nodes[id1].addEdge(edge)

    def addEdgeUndirected(self, id1, id2, weight=1):
        self.checkValidIdsOrException([id1, id2])
        for_edge = GraphEdge(id1, id2, weight)
        back_edge = GraphEdge(id2, id1, weight)
        self.nodes[id1].addEdge(for_edge)
        self.nodes[id2].addEdge(back_edge)

    def hasEdge(self, id1, id2):
        self.checkValidIdsOrException([id1, id2])
        return self.nodes[id1].hasEdge(id2)

    def printNodeId(self, node):
        print(node.id)

    def printGraph(self):
        self.dfs(f=self.printNodeId)

    def bfsWithStart(self, start_id, visited=set(), f=None):
        queue = deque([start_id])
        og_visited = set(visited)
        while len(queue) != 0:
            node_id = queue.popleft()
            node = self.nodes[node_id]
            visited.add(node_id)

            if f: f(node)

            for edge in node.iteredges():
                if edge.dest not in visited:
                    queue.append(edge.dest)

        # Return all nodes visited in this bfs iteration
        return visited - og_visited

    def dfsWithStart(self, start_id, visited=set(), f=None):
        stack = [start_id]
        og_visited = set(visited)
        while len(stack) != 0:
            node_id = stack.pop()
            node = self.nodes[node_id]
            visited.add(node_id)

            if f: f(node)

            for edge in node.iteredges():
                if edge.dest not in visited:
                    stack.append(edge.dest)
        # Return all nodes visited in this dfs iteration
        return visited - og_visited

    def dfs(self, f=None):
        visited = set()
        for id in self.nodes:
            if id not in visited:
                self.dfsWithStart(id, visited, f=f)

    def bfs(self, f=None):
        visited = set()
        for id in self.nodes:
            if id not in visited:
                self.bfsWithStart(id, visited, f=f)

    def dijkstra(self, start_id):
        start = self.nodes[start_id]
        visited = set([start_id])
        distance = defaultdict(lambda: sys.maxint)
        distance[start_id] = 0
        prev = dict()
        pq = PriorityQueue()
        for edge in start.iteredges():
            pq.enqueue((edge.weight, edge.src, edge.dest))

        while len(pq) != 0:
            (weight, src, dest) = pq.dequeue()
            if dest not in visited:
                visited.add(dest)
                prev[dest] = src
                distance[dest] = distance[src] + self.nodes[src].getEdge(dest).weight
                for edge in self.nodes[dest].iteredges():
                    total_distance = distance[dest] + edge.weight
                    pq.enqueue((total_distance, dest, edge.dest))

    def reverse_graph(self):
        """
        Return the reversed graph (all edges are reversed).
        """
        new_graph = Graph()
        for node in self:
            new_graph.addNodeIfNotExist(node.id)

        for node in self:
            for edge in node.iteredges():
                src, dest, weight = edge.src, edge.dest, edge.weight
                new_graph.addEdge(dest, src, weight)
        return new_graph

    def pre_post_dfs(self):
        """
        Return the pre and post labels table of the nodes.
        The table maps pre/post number -> node id
        """
        def pre_post_dfs_helper(start_id, visited, pre_table, post_table, clock):
            stack = [start_id]
            while len(stack) != 0:
                node_id = stack[-1]
                if node_id not in visited:
                    # If we have not visited this node, that means this node
                    # has not been pre visited
                    visited.add(node_id)
                    pre_table[clock[0]] = node_id
                    clock[0] += 1

                    for edge in self.nodes[node_id].iteredges():
                        if edge.dest not in visited:
                            stack.append(edge.dest)
                else:
                    # We have finished visiting all neighbors of this node, so
                    # we post visit it. We set the post number only if it has
                    # not been set before.
                    stack.pop()
                    if node_id not in post_table:
                        post_table[clock[0]] = node_id
                        clock[0] += 1

        pre_table = LinkedDict()
        post_table = LinkedDict()
        visited = set()
        clock = [1]
        for node_id in self.nodes:
            if node_id not in visited:
                pre_post_dfs_helper(node_id, visited, pre_table, post_table, clock)
        return pre_table, post_table

    def scc(self):
        """
        Return the list of all strongly connected components. Each scc is a set
        """
        all_sccs = []
        gr = self.reverse_graph()
        pre_table, post_table = gr.pre_post_dfs()
        visited = set()
        for post_num, node_id in post_table.iteritems(reverse=True):
            if node_id not in visited:
                scc = self.dfsWithStart(node_id, visited)
                all_sccs.append(scc)

        return all_sccs

    def topological_order(self):
        """
        Return the list of ids in topological order
        """
        top_order = []
        _, post_table = self.pre_post_dfs()
        for post_num, node_id in post_table.iteritems(reverse=True):
            top_order.append(node_id)

        return top_order

    def spanning_tree(self):
        pass
