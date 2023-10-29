import typing
import json
import functools
from random import SystemRandom
import itertools
import base64
class UndirectedAdjacencyMatrix():
    matrix: typing.List[typing.List[int]]

    @classmethod
    def from_compressed(cls, vertices: int, compressed: typing.List[bool])->"UndirectedAdjacencyMatrix":
        matrix = []
        idx = 0
        for v in range(vertices):
            matrix.append(compressed[idx:idx+(vertices - v)])
            idx += (vertices - v)
        output = cls(vertices,[])
        output.matrix = matrix
        return output
    
    @classmethod
    def loads(cls, vertices: int, serialized: str)->"UndirectedAdjacencyMatrix":
        raw = int.from_bytes(base64.urlsafe_b64decode(serialized),'big')
        compressed = []
        for i in range((vertices*(vertices+1))//2):
            compressed.insert(0,bool(1<<i & raw))
        return cls.from_compressed(vertices,compressed)


    def __init__(self, vertices: int, edges: typing.Iterable[typing.Tuple[int,int]]):
        matrix = []
        for v in range(vertices):
            matrix.append([False for _ in range(v,vertices)])
        for u, v in edges:
            row, col = min((u, v)), max((u, v))
            matrix[row][col - row] = True
        self.matrix = matrix

    def pop_edge(self, e: typing.Tuple[int,int]):
        if e in self:
            row, col = min(e), max(e) - min(e)
            self.matrix[row][col] = False
        else:
            raise KeyError(e)
        
    def pop_vertex(self, v: int):
        if v >= 0 and v < len(self.matrix):
            self.matrix.pop(v)
            for row, idx in zip(self.matrix[:v],itertools.count()):
                row.pop(v-idx)
        else:
            raise KeyError(v)

    def compressed(self)->typing.Tuple[int, typing.List[bool]]:
        output = []
        for row in self.matrix:
            output.extend(row)
        return len(self.matrix), tuple(output)
    
    def dumps(self)->str:
        x = 0
        for b, i in zip(self.compressed()[1][::-1],itertools.count()):
            x |= int(b)<<i
        return base64.urlsafe_b64encode(x.to_bytes((x.bit_length() // 8 + int(x.bit_length() % 8)),'big')).decode("utf-8")

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
        return len(self.matrix)
    
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
    _vertices: range
    _edges: UndirectedAdjacencyMatrix
    _labels: typing.Dict[int, int]
    _unlabels: typing.Dict[int, int]

    @classmethod
    def from_dict(cls, dct: dict)->"Graph":
        vertices = dct["V"]
        adj = UndirectedAdjacencyMatrix.loads(len(vertices), dct['E'])
        slf = cls(vertices,[])
        slf._edges = adj
        return slf

    @classmethod
    def loads(cls,serialized: str)->"Graph":
        return cls.from_dict(json.loads(serialized))
    
    @property
    def vertices(self)->typing.Iterable[int]:
        return self._labels.keys()
    
    @property
    def edges(self)->typing.Iterable[typing.Tuple[int,int]]:
        for edge in self._edges:
            yield (self._unlabels[edge[0]], self._unlabels[edge[1]])

    def __init__(self,vertices: typing.Iterable[int], edges: typing.Iterable[typing.Tuple[int, int]]):
        self._labels = {}
        self._unlabels = {}
        for v, i in zip(vertices,itertools.count()):
            if type(v) == tuple:
                raise TypeError("Vertex labels cannot be tuples.")
            self._labels[v] = i
            self._unlabels[i] = v

        new_edges = []
        for edge in edges:
            new_edges.append((self._labels[edge[0]], self._labels[edge[1]]))
        num_vertices = len(self._labels.keys())
        self._vertices = range(num_vertices)
        self._edges = UndirectedAdjacencyMatrix(num_vertices,new_edges)

    def map_vertices(self, mapping: "Isomorphism")->"Graph":
        new_edges = []
        for edge in self.edges:
            new_edges.append((mapping[edge[0]],mapping[edge[1]]))
        return Graph(mapping.vertices,new_edges)

    def check_mapping(self, other: "Graph", mapping: "Isomorphism")->bool:
        return self.map_vertices(mapping) == other
    
    def neighbors(self, idx: int)->typing.Set[int]:
        return set(map(lambda t: self._unlabels[t[1]],self._edges[self._labels[idx]]))
    
    def is_automorphism(self, mapping: "Isomorphism")->bool:
        return self.map_vertices(mapping) == self
    
    def pop(self, item: typing.Union[int,typing.Tuple[int,int]]):
        if isinstance(item,tuple) and len(item) == 2:
            self._edges.pop_edge((self._labels[item[0]], self._labels[item[1]]))
        elif isinstance(item,tuple):
            raise ValueError(f"Edge must have exactly two endpoints, not {len(item)}!")
        else:
            x = self._labels[item]
            self._edges.pop_vertex(x)

            self._unlabels.pop(x)
            self._labels.pop(item)

            new_unlabels = {}
            new_labels = {}

            for idx in self._unlabels.keys():
                label = self._unlabels[idx]
                new_idx = idx if idx < x else idx-1
                new_unlabels[new_idx] = label
                new_labels[label] = new_idx

            self._unlabels = new_unlabels
            self._labels = new_labels
    
    def to_dict(self)->dict:
        lst = list(self._unlabels.keys())
        lst.sort()
        V = list(map(lambda v: self._unlabels[v],lst))
        return {
            "V": V,
            'E': self._edges.dumps()
        }

    def dumps(self)->str:
        return json.dumps(self.to_dict())
    
    def __eq__(self, other: "Graph")->bool:
        for v in self.vertices:
            if v not in other:
                return False
        for v in other.vertices:
            if v not in self:
                return False
        for edge in self.edges:
            if edge not in other:
                return False
        for edge in other.edges:
            if edge not in self:
                return False
        return True
    
    def copy(self)->"Graph":
        return Graph(self.vertices,self.edges)
    
    def isomorphism(self, mapping: typing.Dict[int,int])->"Isomorphism":
        return Isomorphism(self.vertices,mapping)

    def __repr__(self)->str:
        return repr({"V": self.vertices, "E": list(self.edges)})
    
    def __contains__(self, item: any)->bool:
        if isinstance(item, tuple) and len(item) == 2:
            return (self._labels[item[0]], self._labels[item[1]]) in self._edges
        elif isinstance(item,tuple):
            raise ValueError("An edge can only have two end points!")
        return item in self.vertices


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

    def __str__(self)->str:
        return str(self._mapping)
    
    def __repr__(self)->str:
        return repr(self._mapping)
    
    def dumps(self)->str:
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