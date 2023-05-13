all_transport = []  # все виды транспорта
city_ind = {}  # city -> ind
ind_city = {}  # ind -> city
trans_ind = {}  # transport_type -> ind
ind_trans = {}  # ind -> transport_type


class Edge:
    def __init__(
            self,
            from_city,
            to_city,
            transport_type,
            cruise_time,
            cruise_fare):
        # тут передаются идентификаторы
        self.from_city = from_city
        self.to_city = to_city
        self.transport_type = transport_type
        self.cruise_time = cruise_time
        self.cruise_fare = cruise_fare


class Path:
    def __init__(self):
        self.path = []

    def __getitem__(self, index):
        return self.path[index]

    def __add__(self, edge):
        new_path = Path()
        new_path.path = self.path + [edge]
        return new_path

    def add_begin(self, edge):
        self.path.insert(0, edge)

    def __str__(self):
        str_route = []
        for r in self.path:
            str_route.append(
                f"{ind_city[r.from_city]} -> {ind_city[r.to_city]},"
                f" time: {r.cruise_time}; fare: {r.cruise_fare}"
            )
        return '\n'.join(str_route)


class Graph:
    def __init__(self):
        # словарь город: [рейсы]
        self.graph = {}

    def add_node(self, node: Edge):
        if node.from_city not in self.graph:
            self.graph[node.from_city] = []
        self.graph[node.from_city].append(node)

    def get_cruises(self, city_id):
        return self.graph[city_id]
