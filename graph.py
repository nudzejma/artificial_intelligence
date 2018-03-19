'''
Module containes class Graph and some of her necessery methods
'''

import math
from collections import deque


class Graph:
    def __init__(self, number_of_vertices: int) -> None:
        self.transition_matrix = [[-1 for i in range(number_of_vertices)] for i in range(number_of_vertices)]
        self.visited = [False] * number_of_vertices
        self.position_x = [None] * number_of_vertices
        self.position_y = [None] * number_of_vertices

    def add_edge(self, vertex_from: int, vertex_to: int, edge_weight: int) -> None:
        '''
        Addes edge between two vertices
        Args:
            vertex_from: vertex from who edge starts
            vertex_to: vertex to who edge ends
            edge_weight: weigth of adding edge

        Returns:

        '''

        self.transition_matrix[vertex_from][vertex_to] = self.transition_matrix[vertex_to][vertex_from] = edge_weight

    def set_position_of_vertex(self, vertex: int, x: int, y: int) -> None:
        '''
        Sets position of vertex
        Args:
            vertex: vertex whos coordinates are setting
            x: x coordinate
            y: y coordinate

        Returns:

        '''

        self.position_x[vertex] = x
        self.position_y[vertex] = y

    def euclidean_distance(self, vertex_from: int, vertex_to: int) -> float:
        '''
        Calculats euclidean distance between two vertices
        Args:
            vertex_from: first vertex
            vertex_to: second vertex

        Returns: Euclidean distance between this two vertices

        '''

        return math.sqrt((self.position_x[vertex_from]-self.position_x[vertex_to]) ** 2 +
                         (self.position_y[vertex_from] - self.position_y[vertex_to]) ** 2)

    def calculate_f(self, vertex_from: int, vertex_throw: int, goal_vertex: int) -> float:
        '''
        Calculates function f(n) = g(n) + h(n) where g(n) is weight of edge and h(n) is distance between start & end
        vertex
        Args:
            vertex_from: start vertex
            vertex_throw: middle vertex
            goal_vertex: end vertex

        Returns: Value of function f

        '''

        if self.transition_matrix[vertex_from][vertex_throw] == -1:
            raise ValueError

        return self.euclidean_distance(vertex_throw, goal_vertex) + self.transition_matrix[vertex_from][vertex_throw]

    def bfs(self, start_vertex: int) -> None:
        '''
        Breadth first search for graph
        Args:
            start_vertex: starting vertex for bfs

        Returns:

        '''

        for i, _ in enumerate(self.visited):
            self.visited[i] = False

        self.visited[start_vertex] = True

        list_of_frontiers = deque([start_vertex])
        # list_of_frontiers.put(start_vertex)

        while list_of_frontiers:

            sv = list_of_frontiers.popleft()
            print('Visiting', sv)

            for i, frontier_weight in enumerate(self.transition_matrix[sv]):

                if frontier_weight != -1 and not self.visited[i]:

                    self.visited[i] = True
                    list_of_frontiers.append(i)

    def get_smallest_comparing_f(self, start_vertex: int, goal_vertex: int, list_of_frontiers: deque) -> int:
        '''

        Args:
            start_vertex:
            goal_vertex:
            list_of_frontiers:

        Returns: smallest index which has the smallest value of function f

        '''

        # if len(list_of_frontiers) == 1:
        #     return 0

        curr_smallest = 10000
        curr_smallest_index = 0
        for i, frontier in enumerate(list(list_of_frontiers)):

            try:

                f = self.calculate_f(start_vertex, frontier, goal_vertex)
                if f < curr_smallest:

                    curr_smallest = f
                    curr_smallest_index = i

            except ValueError:
                continue

        return curr_smallest_index

    def a_star(self, start_vertex: int, goal_vertex: int) -> None:
        '''
        A* algorithm for graph
        Args:
            start_vertex: starting vertex
            goal_vertex: ending vertex

        Returns:

        '''

        for i, _ in enumerate(self.visited):
            self.visited[i] = False

        self.visited[start_vertex] = True

        list_of_frontiers = deque([start_vertex])

        while list_of_frontiers:

            index_of_smallest = self.get_smallest_comparing_f(start_vertex, goal_vertex, list_of_frontiers)

            pom = list_of_frontiers[0]
            list_of_frontiers[0] = list_of_frontiers[index_of_smallest]
            list_of_frontiers[index_of_smallest] = pom

            sv = list_of_frontiers.popleft()
            print('Visiting', sv)
            if sv == goal_vertex:
                return
            for i, frontier_weight in enumerate(self.transition_matrix[sv]):

                if frontier_weight != -1 and not self.visited[i]:

                    self.visited[i] = True
                    list_of_frontiers.append(i)


# example 1
g = Graph(6)
g.set_position_of_vertex(0, 0, 0)
g.set_position_of_vertex(1, 1, 1)
g.set_position_of_vertex(2, 3, 0)
g.set_position_of_vertex(3, 0, 5)
g.set_position_of_vertex(4, 3, 0)
g.set_position_of_vertex(5, -1, -2)

g.add_edge(0, 5, 10)
g.add_edge(0, 2, 10)
g.add_edge(0, 4, 10)
g.add_edge(1, 2, 10)
g.add_edge(2, 0, 10)
g.add_edge(2, 3, 10)
g.add_edge(3, 1, 10)
print('BFS from 0:')
g.bfs(0)
print('A* from 1 to 3:')
g.a_star(1, 3)
