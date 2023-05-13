import curses
import sys
from resource import RUSAGE_SELF, getrusage
from time import time_ns

from algorithms import algorithm
from core import coreclass, file

OPTIONS_NUM = 6

MINCOST_MINTIME_MODE = 0
MINCOST_MODE = 1
MINSTATIONSNUM_MODE = 2
LIMITCOST_MODE = 3
LIMITTIME_MODE = 4
WANT_TO_EXIT = 5


def get_time():
    return time_ns()


def get_mem():
    return getrusage(RUSAGE_SELF).ru_maxrss


def main(stdscr):
    edges = file.parse_file(sys.argv[1])
    g = coreclass.Graph()
    for edge in edges:
        g.add_node(edge)
    want_to_exit = False

    stdscr.scrollok(True)
    stdscr.keypad(True)

    while not want_to_exit:

        current_item_index = 0
        choice_made = False

        curses.noecho()

        choices = [
            "1). Нахождение пути минимальной стоимости среди кратчайших"
            "путей между двумя городами",
            "2). Нахождение пути минимальной стоимости между двумя городами",
            "3). Нахождение пути между двумя городами с минимальным "
            "числом пересадок",
            "4). Нахождение городов, достижимых из города отправления не более"
            " чем за лимит стоимости, и путей к ним",
            "5). Нахождение городов, достижимых из города отправления не более"
            " чем за лимит времени, и путей к ним",
            "Выйти из программы"
        ]

        while not choice_made:
            stdscr.clear()
            curses.curs_set(0)
            stdscr.addstr("Выберите желаемый режим работы программы:\n\n")
            stdscr.refresh()

            for i in range(OPTIONS_NUM):
                if i == current_item_index:
                    stdscr.attron(curses.A_STANDOUT)
                    stdscr.addstr(f"{choices[i]}\n")
                    stdscr.attroff(curses.A_STANDOUT)
                else:
                    stdscr.addstr(f"{choices[i]}\n")
                stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP:
                if current_item_index > 0:
                    current_item_index -= 1
                else:
                    current_item_index = OPTIONS_NUM - 1
            elif key == curses.KEY_DOWN:
                if current_item_index < OPTIONS_NUM - 1:
                    current_item_index += 1
                else:
                    current_item_index = 0
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                choice_made = True

        if current_item_index >= 0 and current_item_index <= OPTIONS_NUM - 2:
            flag_0 = False
            was_transport_error = False
            while not flag_0:
                stdscr.clear()
                if was_transport_error:
                    stdscr.addstr(f"Транспорта вида {transport_type} нет, "
                                  "повторите ввод\n")
                was_transport_error = False
                stdscr.addstr("Введите запрещенные виды транспорта "
                              "(через пробел). Если хотите разрешить "
                              "все виды транспорта, то просто нажмите "
                              "ENTER:\n\n")
                stdscr.refresh()
                curses.curs_set(1)
                curses.echo()

                prohibited_transport = str(stdscr.getstr(), "utf-8",
                                           errors="ignore")
                prohibited_transport = prohibited_transport.split(" ")
                if prohibited_transport == [""]:
                    prohibited_transport = set()
                    flag_0 = True
                else:
                    for transport_type in prohibited_transport:
                        if transport_type not in coreclass.trans_ind:
                            was_transport_error = True
                            break
                    if not was_transport_error:
                        flag_0 = True
                        prohibited_transport = {
                            coreclass.trans_ind[trans_name]
                            for trans_name in prohibited_transport}

        curses.echo()

        if current_item_index == MINCOST_MINTIME_MODE:
            flag_1 = False
            was_start_city_error = False
            while not flag_1:
                stdscr.clear()
                if was_start_city_error:
                    stdscr.addstr("Такого города нет, введите другой "
                                  "город отправления\n")
                stdscr.addstr("Введите город отправления:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                start_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if start_city not in coreclass.city_ind:
                    was_start_city_error = True
                else:
                    flag_1 = True
                    was_start_city_error = False

            flag_2 = False
            was_exit_city_error = False
            while not flag_2:
                stdscr.clear()
                if was_exit_city_error:
                    stdscr.addstr("Такого города нет, введите другой "
                                  "город прибытия\n")
                stdscr.addstr("Введите город прибытия:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                exit_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if exit_city not in coreclass.city_ind:
                    was_exit_city_error = True
                else:
                    flag_2 = True
                    was_exit_city_error = False

            # Запуск первого алгоритма
            time_work = get_time()
            result = algorithm.dijkstra_pq(g, start_city, exit_city,
                                           prohibited_transport, 'task1')
            time_work = get_time() - time_work
            stdscr.clear()
            if result == -1:
                stdscr.addstr("Нет пути между выбранными городами c "
                              "использованием указанных доступных "
                              "видов транспорта\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            else:
                stdscr.addstr(f"{result}\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            stdscr.addstr("Нажмите любую клавишу для перехода в меню\n")
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == MINCOST_MODE:
            flag_1 = False
            was_start_city_error = False
            while not flag_1:
                stdscr.clear()
                if was_start_city_error:
                    stdscr.addstr("Такого города нет, введите другой "
                                  "город отправления\n")
                stdscr.addstr("Введите город отправления:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                start_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if start_city not in coreclass.city_ind:
                    was_start_city_error = True
                else:
                    flag_1 = True
                    was_start_city_error = False

            flag_2 = False
            was_exit_city_error = False
            while not flag_2:
                stdscr.clear()
                if was_exit_city_error:
                    stdscr.addstr("Такого города нет, введите другой "
                                  "город прибытия\n")
                stdscr.addstr("Введите город прибытия:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                exit_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if exit_city not in coreclass.city_ind:
                    was_exit_city_error = True
                else:
                    flag_2 = True
                    was_exit_city_error = False

            # Запуск второго алгоритма
            time_work = get_time()
            result = algorithm.dijkstra_pq(g, start_city, exit_city,
                                           prohibited_transport, 'fare')
            time_work = get_time() - time_work
            stdscr.clear()
            if result == -1:
                stdscr.addstr("Нет пути между выбранными городами c "
                              "использованием указанных доступных "
                              "видов транспорта\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            else:
                stdscr.addstr(f"{result}\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            stdscr.addstr("Нажмите любую клавишу для перехода в меню\n")
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == MINSTATIONSNUM_MODE:
            flag_1 = False
            was_start_city_error = False
            while not flag_1:
                stdscr.clear()
                if was_start_city_error:
                    stdscr.addstr("Такого города нет, введите "
                                  "другой город отправления\n")
                stdscr.addstr("Введите город отправления:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                start_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if start_city not in coreclass.city_ind:
                    was_start_city_error = True
                else:
                    flag_1 = True
                    was_start_city_error = False

            flag_2 = False
            was_exit_city_error = False
            while not flag_2:
                stdscr.clear()
                if was_exit_city_error:
                    stdscr.addstr("Такого города нет, введите "
                                  "другой город прибытия\n")
                stdscr.addstr("Введите город прибытия:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                exit_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if exit_city not in coreclass.city_ind:
                    was_exit_city_error = True
                else:
                    flag_2 = True
                    was_exit_city_error = False

            # Запуск третьего алгоритма
            time_work = get_time()
            result = algorithm.bfs(g, start_city, exit_city,
                                   prohibited_transport)
            time_work = get_time() - time_work
            stdscr.clear()
            if result == -1:
                stdscr.addstr("Нет пути между выбранными городами c "
                              "использованием указанных доступных "
                              "видов транспорта\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            else:
                stdscr.addstr(f"{result}\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            stdscr.addstr("Нажмите любую клавишу для перехода в меню\n")
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == LIMITCOST_MODE:
            flag_1 = False
            was_start_city_error = False
            while not flag_1:
                stdscr.clear()
                if was_start_city_error:
                    stdscr.addstr("Такого города нет, введите "
                                  "другой город отправления\n")
                stdscr.addstr("Введите город отправления:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                start_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if start_city not in coreclass.city_ind:
                    was_start_city_error = True
                else:
                    flag_1 = True
                    was_start_city_error = False

            # Запуск четвертого алгоритма
            stdscr.clear()
            stdscr.addstr("Введите лимит стоимости:\n")
            stdscr.refresh()
            curses.curs_set(1)

            limit_cost = int(str(stdscr.getstr(), "utf-8", errors="ignore"))
            time_work = get_time()
            result = algorithm.dijkstra_pq(g, start_city, '',
                                           prohibited_transport,
                                           'fare', limit_cost)
            time_work = get_time() - time_work
            stdscr.clear()
            if result == -1:
                stdscr.addstr(f"Нет городов, достижимых из {start_city} за "
                              f"{limit_cost} рублей, c использованием "
                              "указанных доступных видов транспорта\n")
                stdscr.addstr(f"время{time_work/10**9} сек,"
                              f" память:{get_mem()}\n")
            else:
                stdscr.addstr(f"Города, достижимые из {start_city}"
                              f" за {limit_cost} рублей:\n")
                for city in result:
                    stdscr.addstr(f'{str(city)}\n')
            stdscr.addstr(f"время{time_work/10**9} сек, память:{get_mem()}\n")
            stdscr.addstr("Нажмите любую клавишу для перехода в меню\n")
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == LIMITTIME_MODE:
            flag_1 = False
            was_start_city_error = False
            while not flag_1:
                stdscr.clear()
                if was_start_city_error:
                    stdscr.addstr("Такого города нет, введите другой"
                                  " город отправления\n")
                stdscr.addstr("Введите город отправления:\n\n")
                stdscr.refresh()
                curses.curs_set(1)

                start_city = str(stdscr.getstr(), "utf-8", errors="ignore")
                if start_city not in coreclass.city_ind:
                    was_start_city_error = True
                else:
                    flag_1 = True
                    was_start_city_error = False

            # Запуск пятого алгоритма
            stdscr.clear()
            stdscr.addstr("Введите лимит времени:\n")
            stdscr.refresh()
            curses.curs_set(1)

            limit_time = int(str(stdscr.getstr(), "utf-8", errors="ignore"))

            time_work = get_time()
            result = algorithm.dijkstra_pq(g, start_city, '',
                                           prohibited_transport,
                                           'time', limit_time)
            time_work = get_time() - time_work
            stdscr.clear()
            if result == -1:
                stdscr.addstr(f"Нет городов, достижимых из {start_city} за "
                              f"{limit_cost} единицу времени, c использованием"
                              " указанных доступных видов транспорта\n")
                stdscr.addstr(f"время{time_work/10**9} сек, "
                              f"память:{get_mem()}\n")
            else:
                stdscr.addstr(f"Города, достижимые из {start_city} за"
                              f"{limit_time} единицу времени:\n")
                for city in result:
                    stdscr.addstr(f"{str(city)}\n")

            stdscr.addstr(f"время{time_work/10**9} сек, память:{get_mem()}\n")
            stdscr.addstr("Нажмите любую клавишу для перехода в меню\n")
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == WANT_TO_EXIT:
            want_to_exit = True

    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
