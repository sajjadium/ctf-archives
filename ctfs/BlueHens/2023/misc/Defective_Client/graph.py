import typing
import json
import functools
from random import SystemRandom
import itertools
import base64
class UndirectedAdjacencyMatrix():
    matrix: typing.Tuple[typing.Tuple[int, ...], ...]
    _len: int = 0

    @classmethod
    def from_compressed(cls, vertices: int, compressed: typing.Tuple[bool, ...])->"UndirectedAdjacencyMatrix":
        matrix = []
        idx = 0
        for v in range(vertices):
            matrix.append(compressed[idx:idx+(vertices - v)])
            idx += (vertices - v)
        matrix = tuple(map(tuple,matrix))
        output = cls(vertices,[])
        output.matrix = matrix
        output._len = sum(map(int,compressed))
        return output

    def __init__(self, vertices: int, edges: typing.Iterable[typing.Tuple[int,int]]):
        matrix = []
        for v in range(vertices):
            matrix.append([False for _ in range(v,vertices)])
        for u, v in edges:
            row, col = min((u, v)), max((u, v))
            matrix[row][col - row] = True
            self._len += 1
        self.matrix = tuple(map(tuple,matrix))

    def compressed(self)->typing.Tuple[int, typing.Tuple[bool,...]]:
        output = []
        for row in self.matrix:
            output.extend(row)
        return len(self.matrix), tuple(output) 

    def __contains__(self, item: typing.Tuple[int,int])->bool:
        row, col = min(item), max(item) - min(item)
        if row < len(self.matrix) and col < len(self.matrix[row]):
            return self.matrix[row][col]
        else:
            raise ValueError(f"Edge {(row, col + row)} cannot exist in graph with {len(self.matrix)} vertices!")
    
    def __iter__(self)->"UndirectedAdjacencyMatrix":
        self._row = 0
        self._col = 0
        return self

    def __next__(self)->int:
        if self._row >= len(self.matrix):
                raise StopIteration()
        while not self.matrix[self._row][self._col]:
            if self._col >= len(self.matrix[self._row])-1:
                self._col = 0
                self._row += 1
            else:
                self._col += 1
            if self._row >= len(self.matrix):
                raise StopIteration()
        row, col = self._row, self._col
        if self._col >= len(self.matrix[self._row])-1:
            self._col = 0
            self._row += 1
        else:
            self._col += 1 
        return (row, col + row)

    def __len__(self)->int:
        return self._len
    
    def __eq__(self,other: "UndirectedAdjacencyMatrix"):
        if len(self.matrix) != len(other.matrix):
            return False
        output = True
        for row1, row2 in zip(self.matrix,other.matrix):
            output = output and functools.reduce(lambda x, y: x and y,[i == j for i, j in zip(row1,row2)])
        return output

    def __repr__(self):
        return repr(self.matrix)
    
    def __getitem__(self, idx: int)->typing.Iterable[int]:
        for b, i in zip(self.matrix[idx],itertools.count()):
            if b:
                yield (idx, idx+i)
        for row, i in zip(self.matrix[:idx],range(idx)):
            if row[idx-i]:
                yield (idx, i)

class Graph():
    vertices: range
    edges: UndirectedAdjacencyMatrix

    @classmethod
    def from_dict(cls, dct: dict)->"Graph":
        vertices = dct["V"]
        E = []
        decoded_E = int.from_bytes(base64.urlsafe_b64decode(dct['E']),'big')
        for edge in range(((vertices * (vertices - 1))//2) + vertices):
            E.insert(0,bool(decoded_E & 1<<edge))

        adj = UndirectedAdjacencyMatrix.from_compressed(vertices, E)
        output = cls(len(adj.matrix),[])
        output.edges = adj
        return output

    @classmethod
    def loads(cls,serialized: str)->"Graph":
        return cls.from_dict(json.loads(serialized))

    def __init__(self,vertices: int, edges: typing.Iterable[typing.Tuple[int,int]]):
        self.vertices = range(vertices)
        self.edges = UndirectedAdjacencyMatrix(vertices,edges)
    
    def isomorphism(self, mapping: typing.Dict[int,int])->"Isomorphism":
        return Isomorphism(self.vertices,mapping)

    def map_vertices(self, mapping: "Isomorphism")->"Graph":
        new_edges = set()
        for edge in self.edges:
            new_edges.add((mapping[edge[0]],mapping[edge[1]]))
        return Graph(len(self.vertices),new_edges)

    def check_mapping(self, other: "Graph", mapping: "Isomorphism")->bool:
        return self.map_vertices(mapping) == other
    
    def neighbors(self, idx: int)->typing.Set[int]:
        return set(map(lambda t: t[1],self.edges[idx]))
    
    def is_automorphism(self, mapping: "Isomorphism")->bool:
        return self.map_vertices(mapping) == self
    
    def to_dict(self)->dict:
        sz, lst = self.edges.compressed()
        x = 0
        for b, i in zip(lst[::-1],itertools.count()):
            x |= int(b)<<i #I sincerely apologize for the bit math. This is the most efficient way by far to store this information.
        return {
            "V": sz,
            'E': base64.urlsafe_b64encode(x.to_bytes((x.bit_length() // 8 + int(x.bit_length() % 8)),'big')).decode("utf-8")
        }

    def dumps(self)->str:
        return json.dumps(self.to_dict())
    
    def __eq__(self, other: "Graph")->bool:
        return self.edges == other.edges

    def __repr__(self):
        return repr({"V": self.vertices, "E": self.edges})
    
    def __contains__(self, item: typing.Union[typing.Tuple[int,int],int]):
        if isinstance(item,int):
            return item in self.vertices
        elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[0],int) and isinstance(item[1],int):
            return item in self.edges
        elif isinstance(item,tuple):
            raise ValueError("Expected an int or tuple of two ints!")
        else:
            raise TypeError("Graph can only contain a numeric vertex or an edge between them") 

class Isomorphism():
    vertices: typing.Set[int]
    _mapping: typing.Dict[int,int]

    @classmethod
    def loads(cls, graph: Graph, data: str)->"Isomorphism":
        data = json.loads(data)
        if not isinstance(data,dict):
            raise ValueError("Isomorphisms are supposed to be in dictionary format.")
        mapping = {}
        for key in data.keys():
            if not isinstance(key,str) or not isinstance(data[key],int):
                raise ValueError("Could not decode isomorphism")
            mapping[int(key)] = data[key]
        return cls(graph.vertices,mapping)
        
    def __init__(self, vertices: typing.Set[int], mapping: typing.Dict[int,int]):
        self.vertices = set(vertices)
        for vertex in vertices:
            if vertex == None:
                raise TypeError("Vertices cannot be labeled with None.")
        self._mapping = dict(mapping)
        for v in self._mapping.keys():
            if not v in self.vertices:
                raise ValueError(f"Mapping contains nonexistent vertex {v}")
        found = set()
        for vertex in self.vertices:
            if vertex in self._mapping.keys() and self._mapping[vertex] == vertex:
                self._mapping.pop(vertex)
            elif vertex in self._mapping.keys():
                if self._mapping[vertex] in found:
                    raise ValueError(f"Invalid permutation: {self._mapping[vertex]} has multiple vertices mapped to it!")
                found.add(self._mapping[vertex])
        
    def __getitem__(self, key: int)->int:
        if key in self._mapping.keys():
            return self._mapping[key]
        elif key in self.vertices:
            return key
        else:
            raise KeyError(key)
    
    def _check_vertices(self, other: "Isomorphism")->None:
        for vertex in self.vertices:
            if not vertex in other.vertices:
                raise ValueError("Cannot create composition from isomorphisms with different vertex sets")
        for vertex in other.vertices:
            if not vertex in self.vertices:
                raise ValueError("Cannot create composition from isomorphisms with different vertex sets")

    def __add__(self, other: "Isomorphism")->"Isomorphism":
        self._check_vertices(other)
        new_mapping = dict()
        for v in self.vertices:
            new_mapping[v] = other[self[v]]
        return Isomorphism(self.vertices,new_mapping)
    
    def __neg__(self)->"Isomorphism":
        new_mapping = dict()
        for v in self.vertices:
            new_mapping[self[v]] = v
        return Isomorphism(self.vertices,new_mapping)
    
    def __sub__(self, other: "Isomorphism")->"Isomorphism":
        self._check_vertices(other)
        return self + (-other)

    def __eq__(self, other: "Isomorphism")->"Isomorphism":
        for vertex in self.vertices:
            if not vertex in other.vertices:
                return False
        for vertex in other.vertices:
            if not vertex in self.vertices:
                return False
            
        for vertex in self.vertices:
            if self[vertex] != other[vertex]:
                return False
        return True

    def __str__(self):
        return json.dumps(self._mapping)

def random_graph(min_vertices: int = 256, max_vertices: int = 512)->Graph:
    r = SystemRandom()
    num_vertices = r.randint(min_vertices,max_vertices)
    edge_space = []
    edges = set()
    for i in range(num_vertices):
        for j in range(i,num_vertices):
            edge_space.append((i,j))
    edges = set(r.sample(edge_space,r.randint(min_vertices,len(edge_space))))
    return Graph(num_vertices,edges)

def random_isomorphism(graph: Graph)->Isomorphism:
    r = SystemRandom()
    vertices = list(graph.vertices)
    newVertices = list(vertices)
    r.shuffle(newVertices)
    transformation = dict([(u, v) for u, v in zip(vertices,newVertices)])
    return graph.isomorphism(transformation)


if __name__ == "__main__":
    g = Graph(4,set([(0,1),(0,2),(2,3),(1,2)]))
    assert 0 in g
    assert 1 in g
    assert 2 in g
    assert 3 in g
    assert 4 not in g
    assert (0, 1) in g
    assert (0, 2) in g
    assert (2, 3) in g
    assert (1, 2) in g
    assert (1, 3) not in g
    assert (1, 0) in g
    assert (2, 0) in g
    assert (3, 2) in g
    assert (2, 1) in g
    assert (3, 1) not in g

    Ne = g.neighbors(0)

    assert 1 in Ne
    assert 2 in Ne
    assert 3 not in Ne

    Ne = g.neighbors(2)
    assert 0 in Ne
    assert 2 in Ne
    assert 1 in Ne

    try: 
        "1" in g
        raise AssertionError("Graphs should not accept strings!")
    except TypeError:
        pass
    assert len(g.edges) == 4
    print(g)
    tst = g.edges.from_compressed(*g.edges.compressed())
    assert len(tst) == 4
    assert tst == g.edges
    g2 = Graph.loads(g.dumps())
    print(g2)
    assert g == g2
    assert g.is_automorphism(g.isomorphism({0: 1, 1: 0})) #Check that it correctly detects an automorphism
    g3 = g.map_vertices(g.isomorphism({0: 1, 1: 2, 2: 3, 3: 0})) #generate an isomorphic graph
    print(g3)
    assert g.check_mapping(g3,g.isomorphism({0: 1, 1: 2, 2: 3, 3: 0})) #validate the isomorphism
    assert g.check_mapping(g3,g.isomorphism({0:1, 1:0}) + g.isomorphism({0: 1, 1: 2, 2: 3, 3: 0})) #The same as the automorphism above followed by the isomorphism.
    G = random_graph(128,256)
    print(len(G.dumps()))
    print(len(json.dumps(G.edges.matrix)))