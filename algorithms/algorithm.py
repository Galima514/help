import heapq
import queue

from core import coreclass


def bfs(graph: coreclass.Graph, start: int, end: int,
        prohibited_transport: set):
    start = coreclass.city_ind[start]
    end = coreclass.city_ind[end]

    opt_dist = {vertex: 2**32 for vertex in graph.graph}
    visited = {}

    q = queue.Queue()
    q.put(start)

    opt_dist[start] = 0

    while not q.empty():
        current_vertex = q.get()
        for cruise in graph.get_cruises(current_vertex):
            if cruise.transport_type in prohibited_transport:
                continue
            elif opt_dist[cruise.to_city] == 2**32:
                q.put(cruise.to_city)
                opt_dist[cruise.to_city] = opt_dist[current_vertex] + 1
                visited[cruise.to_city] = cruise

    if end not in visited:
        return -1

    path = coreclass.Path()
    act = end
    while act != start:
        path.add_begin(visited[act])
        act = visited[act].from_city
    return path


def calc_dijkstra_time(graph: coreclass.Graph, start: int,
                       prohibited_transport: set):
    opt_dist = {vertex: 2**32 for vertex in graph.graph}
    visited = {}
    opt_dist[start] = 0
    pq = [(0, start)]
    while len(pq):
            current_time, current_vertex = heapq.heappop(pq)
            if current_time > opt_dist[current_vertex]:
                continue
            for cruise in graph.get_cruises(current_vertex):
                # если транспорт запрещен, то нам такой путь не нужен
                if cruise.transport_type in prohibited_transport:
                    continue
                distance = current_time + cruise.cruise_time
                if distance < opt_dist[cruise.to_city]:
                    opt_dist[cruise.to_city] = distance
                    visited[cruise.to_city] = cruise
                    heapq.heappush(pq, (distance, cruise.to_city))
    return (opt_dist, visited)


def restore_route_time(opt_dist, visited, from_city, to_city, lim_time=2**32):
        if to_city not in visited:
            return -1
        # гарантия того, что мы там были + чек на время
        if opt_dist[to_city] >= lim_time:
            return -1
        path = coreclass.Path()
        act = to_city
        while act != from_city:
            path.add_begin(visited[act])
            act = visited[act].from_city
        return path


def calc_dijkstra_cost(graph: coreclass.Graph, start: int,
                       prohibited_transport: set):

    opt_dist = {vertex: 2**32 for vertex in graph.graph}

    visited = {}
    opt_dist[start] = 0
    pq = [(0, start)]
    while len(pq):
            current_fare, current_vertex = heapq.heappop(pq)
            if current_fare > opt_dist[current_vertex]:
                continue
            for cruise in graph.get_cruises(current_vertex):
                # если транспорт запрещен, то нам такой путь не нужен
                if cruise.transport_type in prohibited_transport:
                    continue
                distance = current_fare + cruise.cruise_fare
                if distance < opt_dist[cruise.to_city]:
                    opt_dist[cruise.to_city] = distance
                    visited[cruise.to_city] = cruise
                    heapq.heappush(pq, (distance, cruise.to_city))
    return (opt_dist, visited)


def restore_route_cost(opt_dist, visited, from_city,
                       to_city, lim_cost=2**32):
        if to_city not in visited:
            return -1
        # гарантия того, что мы там были + чек на время
        if opt_dist[to_city] >= lim_cost:
            return -1
        path = coreclass.Path()
        act = to_city
        while act != from_city:
            path.add_begin(visited[act])
            act = visited[act].from_city
        return path


def calc_dijkstra_task1(graph: coreclass.Graph, start: int,
                        prohibited_transport: set):
    """среди быстрых самый дешевый """
    opt_dist = {vertex: 2**64 for vertex in graph.graph}
    visited = {}
    opt_dist[start] = 0
    pq = [(0, start)]
    while len(pq):
            current_dist, current_vertex = heapq.heappop(pq)
            if current_dist > opt_dist[current_vertex]:
                continue
            for cruise in graph.get_cruises(current_vertex):
                # если транспорт запрещен, то нам такой путь не нужен
                if cruise.transport_type in prohibited_transport:
                    continue
                # умножаем cruise_time*2^32 + cruise_fare
                distance = current_dist + (cruise.cruise_time << 32
                                           | cruise.cruise_fare)
                if distance < opt_dist[cruise.to_city]:
                    opt_dist[cruise.to_city] = distance
                    visited[cruise.to_city] = cruise
                    heapq.heappush(pq, (distance, cruise.to_city))
    return (opt_dist, visited)


def restore_route_task1(opt_dist, visited, from_city, to_city):
        if to_city not in visited:
            return -1
        # гарантия того, что мы там были + чек на время
        if opt_dist[to_city] >= 2**64:
            return -1
        path = coreclass.Path()
        act = to_city
        while act != from_city:
            path.add_begin(visited[act])
            act = visited[act].from_city
        return path


def dijkstra_pq(graph: coreclass.Graph, start: str, end: str,
                prohibited_transport: set, kind: str, lim=0):
    """
    в зависимости что от нас требуется, kind это fare или time
    ну и лимиткост в зависимости какой, но вычисления одинаковые
    """
    start = coreclass.city_ind[start]
    if end:
        end = coreclass.city_ind[end]

    if kind == 'time':
        opt_dist, visited = calc_dijkstra_time(graph, start,
                                               prohibited_transport)
        # если ограничений нет, то один путь
        if lim == 0:
            return restore_route_time(opt_dist, visited, start, end)
        allowed_citys = []
        for vertex in visited:
            if opt_dist[vertex] <= lim:
                allowed_citys.append(restore_route_time(opt_dist, visited,
                                                        start, vertex))
        return allowed_citys
    elif kind == 'fare':
        opt_dist, visited = calc_dijkstra_cost(graph, start,
                                               prohibited_transport)
        # если ограничений нет, то один путь
        if lim == 0:
            return restore_route_cost(opt_dist, visited, start, end)
        allowed_citys = []
        for vertex in visited:
            if opt_dist[vertex] <= lim:
                allowed_citys.append(restore_route_cost(opt_dist, visited,
                                                        start, vertex))
        return allowed_citys
    else:
        opt_dist, visited = calc_dijkstra_task1(graph,
                                                start, prohibited_transport)
        return restore_route_task1(opt_dist, visited, start, end)
