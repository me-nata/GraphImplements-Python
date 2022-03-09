from typing import final
from graph_structs import *


class Cell:
    def __init__(self):
        self.edges = []

    def exist(self):
        return self.edges != []

    def add_parallel(self, edge:Edge=Edge()):
        self.edges.append(edge)

    def delete(self, parallel:int=-1):
        if parallel == -1:
            self.edges.clear()
        else:
            self.edges.pop(parallel)

    def __str__(self) -> str:
        output = ''
        for e in self.edges:
            output += str(e)

        return output

class Graph:
    def __init__(self, directional=False) -> None:
        self.vertices=[];
        self.matrix=[];
        self.directional = directional

    def add(self, *args):
        for x in args:
            if type(x) is Vertice:
                self.vertices.append(x)
                self.matrix.append([Cell() for _ in self.vertices])
                for line in self.matrix[:-1]:
                    line.append(Cell())

            elif type(x) is EdgeEntry:
                self.matrix[x.i][x.j].add_parallel(x.e)

                if not self.directional:
                    self.matrix[x.j][x.i].add_parallel(x.e)

    def remove(self, v_index:int, edge:int=-1, parallel:int=-1):
        if edge == -1:
            self.vertices.pop(v_index)
            self.matrix.pop(v_index)
            for v in self.matrix:
                v.pop(v_index)
        else:
            if parallel == -1:
                self.matrix[v_index][edge].delete()
            else:
                self.matrix[v_index][edge].delete(parallel)


    def timer(self, start:int=0):
        #=================stack definitions
        stack = []
        new_cell      = lambda v: stack.insert(0, [v, 0])
        del_cell      = lambda: stack.pop(0)
        current_v     = lambda: stack[0][0]
        final_connec  = lambda: stack[0][1]
        #=================

        timer = 1
        resp = []
        pos_resp=0
        painted_count = 0
        new_cell(start)
        while painted_count < len(self.vertices):
            if len(stack) > 0:
                connections = self.matrix[current_v()]
                if not self.vertices[current_v()].painted(): 
                    self.vertices[current_v()].altern_color()
                    resp.append([timer])
                    painted_count+=1

                pos_connection=final_connec()
                for connection in connections[final_connec():]:
                    if connection.exist():
                        if not self.vertices[pos_connection].painted():
                            stack[0][1] = pos_connection+1
                            new_cell(pos_connection)
                            pos_resp+=1
                            break

                    pos_connection+=1

                # if not have more connections
                if pos_connection >= len(connections):
                    resp[pos_resp].append(timer)
                    del_cell()
                    pos_resp-=1

                timer+=1

            else:
                pos_v = 0
                for v in self.vertices:
                    if not v.painted():
                        new_cell(pos_v)

                    pos_v+= 1

        for v in self.vertices: 
            v.reset_color()

        return resp

    # def breadth(self, start:int=0):
    #     #================= queue definitions
    #     queue = []
    #     new_cell      = lambda v, l: queue.append((v, l))
    #     del_cell      = lambda: queue.pop(0)
    #     level         = lambda v: queue[v][1]
    #     back          = lambda: queue[0][0]
    #     front         = lambda: queue[-1][0]
    #     #=================

    #     VERTICE =  0
    #     LAST    = -1
    #     LEVEL   =  1

    #     resp = [[[], -1]]
    #     #start insertion
    #     new_cell(start, 0)
    #     self.vertices[start].altern_color()
    #     resp[0][0].append(start)
    #     resp[0][1] = 0

    #     resp.append([[], -1])                                                            

    #     current_level = 1
    #     painted_count = 1
    #     while painted_count < len(self.vertices):
    #         connections = self.matrix[back()]
    #         painted_count += 1
            
    #         pos_connec=0
    #         for connection in connections:
    #             if connection.exist():
    #                 if not self.vertices[pos_connec].painted():
    #                     self.vertices[pos_connec].altern_color()
    #                     new_cell(pos_connec, current_level+1)
    #                     resp[LAST][VERTICE].append(pos_connec)
    #                     painted_count+=1

    #             pos_connec+=1

    #         del_cell()
    #         if level(front()) != current_level:
    #             resp[LAST] = level(back())
    #             resp.append([[], -1])

    #     return resp

    def __str__(self):
        output  = '(\nis ' + '' if self.directional else 'not '
        output += 'directional\n'
        for pos_v in range(len(self.vertices)):
            output += f'v{pos_v}: '
            output += str(self.vertices[pos_v])
            output += f' to=> '
            pos_edge = 0
            for cell in self.matrix[pos_v]:
                output += f'v{pos_edge}: {cell} ' if cell.exist() else ''
                pos_edge+=1

            output += '\n'

        return output


g = Graph(directional=True)
g.add(
    Vertice(data=1.5),
    Vertice(data=5),
    Vertice(data=2),
    Vertice(data=1),
    EdgeEntry(0, 1, Edge(weight=5)),
    EdgeEntry(0, 2, Edge(weight=2.5)),
    EdgeEntry(1, 1, Edge(label='teste')),
    EdgeEntry(1, 2, Edge(weight=6)),
    EdgeEntry(3, 1, Edge(weight=6)),
)

print(g)
print(g.timer(0))
print(g.breadth(0))