from .coreclass import (Edge, all_transport, city_ind, ind_city, ind_trans,
                        trans_ind)


def parse_line(split_line: list) -> list:
    values = []
    buffer = []
    for value in split_line:
        try:
            if '"' == value[0] == value[-1]:
                values.append(value.replace('"', ''))
            elif '"' == value[0] != value[-1]:
                buffer.append(value)
            elif '"' == value[-1]:
                values.append(f'{buffer.pop()} {value}'.replace('"', ''))
            elif '\n' == value[-1]:
                values.append(int(value[:-1]))
            else:
                values.append(int(value))
        except ValueError:
            break
    return values


def parse_file(file_path: str):
    edges = []
    id = 0
    id_t = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line[0] == "#" or len(line) == 1:
                continue
            split_line = line.split(" ")
            (from_city, to_city,
             transport_type, cruise_time, cruise_fare) = parse_line(split_line)
            if transport_type not in trans_ind:
                trans_ind[transport_type] = id_t
                ind_trans[id_t] = transport_type
                id_t += 1
            for city in [from_city, to_city]:
                if city not in city_ind:
                    city_ind[city] = id
                    ind_city[id] = city
                    id += 1
            edges.append(Edge(
                from_city=city_ind[from_city],
                to_city=city_ind[to_city],
                transport_type=trans_ind[transport_type],
                cruise_time=cruise_time,
                cruise_fare=cruise_fare
            ))
            if trans_ind[transport_type] not in all_transport:
                all_transport.append(trans_ind[transport_type])
    return edges
