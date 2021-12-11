# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年12月10日13时
"""


class Graph:
    """使用邻接图简单地表示图"""

    class Vertex:
        """图的顶点结构设计"""

        __slots__ = '_element'

        def __init__(self, element):
            """不应直接调用构造方法生成顶点"""
            self._element = element

        def element(self):
            """返回这个顶点上的元素"""
            return self._element

        def __eq__(self, other):
            return self._element == other.element()

        def __hash__(self):
            return hash(id(self))

    class Edge:
        """图的边结构设计"""

        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, origin, destination, element):
            """不应直接调用构造方法生成边"""
            self._origin = origin
            self._destination = destination
            self._element = element

        def endpoints(self) -> tuple:
            """
            对于这条边的起点和终点，返回一个形如(origin,destination)的元组。
            对于无向图而言，方向是任意的。
            """
            return self._origin, self._destination

        def opposite(self, x):
            """
            假设顶点x是边上的一个端点(起点或终点)，返回另外一个端点。
            :param x: 这条边上的一个端点
            :return: 这条边上的另外一个端点
            """
            return self._destination if x is self._origin else self._origin

        def element(self):
            """返回这条边上的元素"""
            return self._element

        def origin(self):
            """返回这条边的起点"""
            return self._origin

        def destination(self):
            """返回这条边的终点"""
            return self._destination

        def __eq__(self, other):
            return self._element == other.element()

        def __hash__(self):
            return hash((self._origin, self._destination))

    def __init__(self, directed=False):
        """
        创建一个空图，默认是无向图
        :param directed: 当创建的是有向图时，将其设置为True
        """
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """

        :return: 该图是否是一个有向图，如果是无向图则返回False
        """
        return self._incoming is not self._outgoing

    def vertex_count(self):
        """

        :return: 图中顶点的总数
        """
        return len(self._outgoing)

    def vertices(self):
        """

        :return: 图中所有顶点的一个列表
        """
        return self._outgoing.keys()

    def edge_count(self):
        """

        :return: 图中边的总数
        """
        edge_total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # 有向图会将一条边重复计算一次，因此需要整除一次2
        return edge_total if self.is_directed() else edge_total // 2

    def edge(self):
        """

        :return: 图中所有边的一个集合
        """
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """

        :param u: 起点
        :param v: 终点
        :return: 从u到v的边，如果没有相邻则返回None
        """
        return self._outgoing[u].get(v)

    def degree(self, v, out=True):
        """
        对于无向图而言，返回边入射到顶点v的数目。
        对于有向图而言，返回顶点v的出/入度，默认返回出度。
        :param v: 顶点
        :param out: 选择返回出度还是入度
        :return: 无向图返回边入射到顶点v的数量，有向图根据选择返回顶点v的出度/入度。
        """
        ch = self._outgoing if out else self._incoming
        return len(ch[v])

    def incident_edges(self, v, out=True):
        """
        对于无向图而言，返回边入射到顶点v的迭代对象
        对于有向图而言，返回顶点v上的输出（或输入）边，默认输出输出边
        :param v: 顶点
        :param out: 选择返回输出还是输入
        :return: 无向图返回顶点v上所有边的迭代对象，有向图返回顶点v上的输出（或输出）边的迭代对象
        """
        ch = self._outgoing if out else self._incoming
        for edge in ch[v].values():
            yield edge

    def insert_vertex(self, element=None):
        """
        插入并返回一个包含元素的新顶点
        :param element:顶点内内容，默认为空
        :return:顶点
        """
        v = self.Vertex(element)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, element=None):
        """
        插入并返回一个带有元素的边
        :param u: 起点
        :param v: 终点
        :param element:边内元素，默认为空
        :return: 边
        """
        e = self.Edge(u, v, element)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def kruskal(self):
        """
        最小生成树Kruskal
        :return:
        """
        edges = list(self.edge())
        edges.sort(key=lambda edge: edge.element())
        connect = {}  # 避免环的产生
        res = []
        vertices = self.vertices()
        for v in vertices:
            connect[v] = v
        for e in edges:
            origin, destination, weight = e.origin(), e.destination(), e.element()
            if connect[origin] != connect[destination]:
                res.append(([origin, destination], weight))
                if len(res) == self.vertex_count() - 1:
                    break
                a, b = connect[origin], connect[destination]
                for key in connect:
                    if connect[key] == b:
                        connect[key] = a
        return res

    def prim(self):
        """
        最小生成树prim
        :return:
        """
        edges = list(self.edge())
        edges.sort(key=lambda edge: edge.element())
        vertices = list(self.vertices())
        v = vertices[0]
        visited = set()
        visited.add(v)
        res = []
        while len(res) < self.vertex_count() - 1:
            for e in edges:
                origin, destination, weight = e.origin(), e.destination(), e.element()
                if origin in visited:
                    if destination not in visited:
                        visited.add(destination)
                        res.append(([origin, destination], weight))
                        break
                if destination in visited:
                    if origin not in visited:
                        visited.add(origin)
                        res.append(([origin, destination], weight))
                        break
        return res


def DFS(g, u, visited):
    """
    深度优先搜索DFS
    :param g: 图
    :param u: 初始顶点
    :param visited:遍历过的各顶点的路径
    :return:
    """
    for x in g.incident_edges(u):
        v = x.opposite(u)
        if v not in visited:
            visited[v] = x
            DFS(g, v, visited)


def construct_path(g, u, v, visited):
    """
    根据深度优先搜索DFS或广度优先搜索BFS得到顶点u到顶点v是否可达，根据DFS遍历期间的记录可以对路径进行重建。
    :param g: 图
    :param u: 起点
    :param v: 终点
    :param visited:DFS/BFS之后各顶点的路径
    :return: 起点u到终点v的路径
    """
    path = []
    DFS(g, u, visited)
    if v in visited:
        path.append(v)
        walk = v
        while walk is not u:
            e = visited[walk]
            parent = e.opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()
    return path


def BFS(g, x, visited):
    """
    广度优先搜索BFS
    :param g: 图
    :param x: 顶点
    :param visited: 遍历过的各顶点的路径
    :return:
    """
    level = [x]
    while len(level) > 0:
        next_level = []
        for u in level:
            for e in g.incident_edges(u):
                v = e.opposite(u)
                if v not in visited:
                    visited[v] = e
                    next_level.append(v)
        level = next_level


def topological_sort(g) -> list:
    """
    拓扑排序。
    如果图中有环，则无法进行拓扑排序！
    :param g: 图
    :return: 拓扑排序列表
    """
    topo = []
    ready = []
    count = {}
    for u in g.vertices():
        count[u] = g.degree(u, False)
        if count[u] == 0:
            ready.append(u)
    while len(ready) > 0:
        u = ready.pop()
        topo.append(u)
        for e in g.incident_edges(u):
            v = e.opposite(u)
            count[v] -= 1
            if count[v] == 0:
                ready.append(v)
    return topo


if __name__ == '__main__':
    # myGraph = Graph(directed=True)
    #
    # A = myGraph.insert_vertex('A')
    # B = myGraph.insert_vertex('B')
    # C = myGraph.insert_vertex('C')
    # D = myGraph.insert_vertex('D')
    # E = myGraph.insert_vertex('E')
    # F = myGraph.insert_vertex('F')
    #
    # E1 = myGraph.insert_edge(A, B, 'Eab')
    # E2 = myGraph.insert_edge(A, C, 'Eac')
    # E3 = myGraph.insert_edge(C, D, 'Ecd')
    # E4 = myGraph.insert_edge(D, E, 'Ede')
    # E5 = myGraph.insert_edge(E, A, 'Eea')
    # E6 = myGraph.insert_edge(B, D, 'Ebd')
    # E7 = myGraph.insert_edge(D, F, 'Edf')
    # E8 = myGraph.insert_edge(F, B, 'Efb')

    # visited = {}
    # DFS(myGraph, A, visited)
    # for k, v in visited.items():
    #     print(str(k.element()) + ':' + str(v.element()))

    # path = construct_path(myGraph, B, C, visited)
    # for i in path:
    #     print(i.element(), end=' ')

    # print(myGraph.edge_count())

    # print()

    # for v in topological_sort(myGraph):
    #     print(v.element())

    # ---------------------------------------------------------------------------------------------------------------
    udGraph = Graph()

    A = udGraph.insert_vertex('A')
    B = udGraph.insert_vertex('B')
    C = udGraph.insert_vertex('C')
    D = udGraph.insert_vertex('D')
    E = udGraph.insert_vertex('E')
    F = udGraph.insert_vertex('F')
    G = udGraph.insert_vertex('G')

    E1 = udGraph.insert_edge(A, B, 5)
    E2 = udGraph.insert_edge(A, C, 11)
    E3 = udGraph.insert_edge(A, D, 6)
    E4 = udGraph.insert_edge(B, D, 3)
    E5 = udGraph.insert_edge(B, G, 7)
    E6 = udGraph.insert_edge(B, E, 9)
    E7 = udGraph.insert_edge(C, D, 7)
    E8 = udGraph.insert_edge(C, F, 6)
    E9 = udGraph.insert_edge(F, G, 8)
    E10 = udGraph.insert_edge(D, G, 20)
    E11 = udGraph.insert_edge(G, E, 8)

    kruskal = udGraph.kruskal()
    for i in kruskal:
        print(i[0][0].element(), end=' ')
        print(i[0][1].element(), end=' ')
        print(i[1])

    print('-' * 20)

    prim = udGraph.prim()
    for i in prim:
        print(i[0][0].element(), end=' ')
        print(i[0][1].element(), end=' ')
        print(i[1])
