from itertools import product
from json import load
from math import comb, prod
from os import path
from random import choice
from time import time


class House(object):
    def __init__(
        self,
        x: int,
        y: int,
        possibility: float,
        situation: int,
        neighbors: list,
        actual: int = -1,
        potential: list | None = None,
    ) -> None:
        """
        x: int & y: int
            the house coordinates

        possibility: float
            the possibility of house being mine

        situation: int
            0 - 8: number of the house (0 is hole)
            9: mine (possibility is 1)
            -1: not specified
            -2: zero posibility

        neighbors: list
            [
                (x: int, y: int), ...
                neighbor coordinates
            ]

        actual: int
            remainig mine in the potential

        potential: list
            [
                (x: int, y: int), ...
            ]
            empty houses in the neighbor
        """
        self.x = x
        self.y = y
        self.possibility = possibility
        self.situation = situation
        self.neighbors = neighbors
        self.actual = actual
        self.potential = potential if potential else neighbors

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.situation))

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.situation == __o.situation

    def __str__(self) -> str:
        # TODO: in futur printing possibility with colorama
        match self.situation:
            case -2:
                return "."
            case -1:
                return " "
            case 9:
                return "*"
        return str(self.situation)

    def __repr__(self) -> str:
        return self.__str__()


class Map(object):
    def __init__(self, x: int, y: int, mines: int) -> None:
        """
        x: int
            xAxis size

        y: int
            yAxis size

        minse: int
            the number of mines in the map
        """
        self.x = x
        self.y = y
        self.mines = mines

        possibility = mines / x / y
        self.main_map = {
            (i, j): House(i, j, possibility, -1, self.neighbor(i, j), -1, -1)
            for i in range(x)
            for j in range(y)
        }
        self.possible_comb = list()
        self.grouping()

    def __setitem__(self, key, value) -> None:
        """
        self.main_map[key].situation = value
        """
        if self[key] not in [-1, -2] or self[key] == value:
            return
        self.main_map[key].situation = value
        if value == 9:
            self.main_map[key].possibility = 1
        else:
            self.main_map[key].possibility = 0
        self.potential_actual_update()
        self.grouping()
        while self.simple_id(key):
            pass
        for i in self.main_map[key].neighbors:
            while self.simple_id(i):
                pass

    def __getitem__(self, key) -> int:
        """
        self.main_map[key].situation
        """
        return self.main_map[key].situation

    def __str__(self) -> str:
        """return str(self)"""
        x, y, out = self.x - 1, self.y - 1, list()
        out.append("  ╔" + "═══╤" * x + "═══╗")
        for i in range(y):
            out.append(
                f"{y-i:<2}║"
                + "".join([f" {self.main_map[(j, y - i)]} │" for j in range(x)])
                + f" {self.main_map[(x, y - i)]} ║"
            )
            out.append("  ╟" + "───┼" * x + "───╢")
        out.append(
            f"{0} ║"
            + "".join([f" {self.main_map[(j, 0)]} │" for j in range(x)])
            + f" {self.main_map[(x, 0)]} ║"
        )
        out.append("  ╚" + "═══╧" * x + "═══╝")
        out.append("    " + "   ".join([str(i) for i in range(x + 1)]))
        return "\n".join(out)

    def __repr__(self) -> str:
        return self.__str__()

    def moves(self):
        p1 = [i for i in self.main_map if self.main_map[i].possibility == 1]
        p = [
            (i, self.main_map[i].possibility)
            for i in self.main_map
            if self.main_map[i].possibility not in [0, 1]
        ]
        p.sort(key=lambda x: x[1], reverse=True)
        p_max = [i[0] for i in p if i[1] == p[0][1]]
        anti_whole = [
            i for i in p_max if any([self[j] == 9 for j in self.main_map[i].neighbors])
        ]
        return p1 + [choice(anti_whole if anti_whole else p_max) if p_max else []]

    def neighbor(self, x: int, y: int) -> list:
        """
        return coordinate of neighbors of the house (x, y)
        """
        out = list()
        for neighbor_x in [-1, 0, 1]:
            for neighbor_y in [-1, 0, 1]:
                if (
                    self.x > x + neighbor_x >= 0
                    and self.y > y + neighbor_y >= 0
                    and (neighbor_x, neighbor_y) != (0, 0)
                ):
                    out.append((x + neighbor_x, y + neighbor_y))
        return out

    def potential_actual_update(self):
        for k, v in self.main_map.items():
            if v.situation in [-2, -1, 0, 9]:
                continue
            house_value = v.situation
            mine_possibility = list()
            for i in v.neighbors:
                if self[i] == 9:
                    house_value -= 1
                elif self[i] == -1:
                    mine_possibility.append(i)
            self.main_map[k].actual = house_value
            self.main_map[k].potential = mine_possibility

    def grouping(self) -> None:
        """
        group: list
            [
                [
                    {neighbor_house: House, ...},
                    [(x: int, y: int), ...],
                    [min_: int, ..., max_: int],
                ], ...
            ]
            min_: int & max_: int
                The minimum and maximum number
                of mines in this complex of houses
        """
        group = list()
        keys = list()
        house_groups = dict()
        for i in self.main_map:
            if self[i] != -1:
                continue
            neighbors = set(
                self.main_map[j]
                for j in self.main_map[i].neighbors
                if self[j] not in [-2, -1, 9]
            )

            try:
                index = keys.index(neighbors)
                group[index][1].append(i)
            except ValueError:
                index = len(group)
                keys.append(neighbors)
                group.append([neighbors, [i]])

            for j in neighbors:
                tmp = set()
                tmp.update(house_groups.get(j, set()), set([index]))
                house_groups[j] = tmp

        for i_, i in enumerate(group):
            group[i_].append([min([len(i[1]), self.mines] + [j.actual for j in i[0]])])

        # TODO: improve min and max
        for i_, i in enumerate(group):
            mins = [0]
            for j in i[0]:
                mins.append(
                    j.actual
                    - sum([group[k][2][-1] for k in house_groups[j] if k != i_])
                )
            min_ = max(mins)
            if min_ > group[i_][2][-1]:
                group[i_][2] = []
                self.group = group
                return
            group[i_][2] = list(range(min_ if min_ > 0 else 0, group[i_][2][-1] + 1))

        group.sort(key=lambda x: len(x[1]))
        self.group = group

    def homes_group_finder(self, inp: House) -> set:
        out = set()
        for i_, i in enumerate(self.group):
            if inp in i[0]:
                out.add(i_)
        return out

    def check(self) -> bool:
        # Check number of mines in house neighbors
        for i, house in self.main_map.items():
            if house.situation in [-2, -1, 0, 9]:
                continue
            if house.actual > len(house.potential) or house.actual < 0:
                return False

        # Check groups
        if not all([j[2] for j in self.group]):
            return False
        for i in self.main_map.values():
            groups_index = self.homes_group_finder(i)
            if i.situation in [-2, -1, 0, 9] or not groups_index:
                continue
            if not (
                sum([self.group[j][2][0] for j in groups_index])
                <= i.actual
                <= sum([self.group[j][2][-1] for j in groups_index])
            ):
                return False

        # Check number of mines
        mines = [self[i] for i in self.main_map].count(9)
        if (
            mines > self.mines
            or [self[i] for i in self.main_map].count(-1) < self.mines - mines
            or sum([i[2][0] for i in self.group]) + mines > self.mines
        ):
            return False

        return True

    def simple_id(self, inp: tuple) -> bool:
        """
        find 100% & 0% mine possibility in simple nieghbors of the house
        inp: tuple
            (x: int, y: int)
            the coordinate of the house
        """
        out = False
        if self[inp] in [-2, -1, 0, 9]:
            return out

        house = self.main_map[inp]
        if house.actual == 0:
            for i in house.neighbors:
                if self[i] == -1:
                    self[i] = -2
                    out = True
        elif len(house.potential) == house.actual:
            for i in house.neighbors:
                if self[i] == -1:
                    self[i] = 9
                    out = True
        return out

    def group_id(self) -> bool:
        for i in self.group:
            if len(i[2]) == 1:
                if i[2][0] == len(i[1]):
                    for j in i[1]:
                        self[j] = 9
                    return True
                elif i[2][0] == 0:
                    for j in i[1]:
                        self[j] = -2
                    return True
        return False

    def composite_id(self) -> bool:
        if not self.check():
            return False

        if self.group_id():
            return True

        non_negotiable = list()
        for i in self.group:
            if len(i[2]) == 1:
                non_negotiable += [(*j, 9) for j in i[1][: i[2][0]]] + [
                    (*j, -2) for j in i[1][i[2][0] :]
                ]

        for i in self.group:
            if len(i[2]) == 1:
                continue
            for j in i[2][::-1]:
                new = Map(self.x, self.y, self.mines)
                new.update(
                    [(*k, self[k]) for k in self.main_map]
                    + [(*k, 9) for k in i[1][:j]]
                    + [(*k, -2) for k in i[1][j:]]
                    + non_negotiable,
                    composite=False,
                )

                if not new.check():
                    i[2].remove(j)

            if self.group_id():
                return True

            if len(i[2]) == 1:
                non_negotiable += [(*k, 9) for k in i[1][: i[2][0]]] + [
                    (*k, -2) for k in i[1][i[2][0] :]
                ]

        self.possible_comb = list()
        rem = self.mines - [self[i] for i in self.main_map].count(9)

        def X(x):
            return rem - sum(x) in self.group[-1][2]

        for i in filter(X, product(*[i[2] for i in self.group[:-1]])):
            i = (*i, rem - sum(i))
            new = Map(self.x, self.y, self.mines)
            new.update(
                [(*k, self[k]) for k in self.main_map]
                + sum(
                    [
                        [(*k, 9) for k in self.group[j_][1][:j]]
                        + [(*k, -2) for k in self.group[j_][1][j:]]
                        for j_, j in enumerate(i)
                    ],
                    [],
                ),
                composite=False,
            )

            if new.check():
                self.possible_comb.append(i)

        for i_, i in enumerate(self.group):
            for j in i[2][::-1]:
                if j not in [k[i_] for k in self.possible_comb]:
                    i[2].remove(j)

        if self.group_id():
            return True

        group_num = [len(i[1]) for i in self.group]
        comb_num = [
            prod([comb(group_num[j_], j) for j_, j in enumerate(i)])
            for i in self.possible_comb
        ]
        for i_, i in enumerate(self.group):
            p = sum(
                [
                    j / group_num[i_] * comb_num[j_]
                    for j_, j in enumerate([k[i_] for k in self.possible_comb])
                ]
            ) / sum(comb_num)
            for j in i[1]:
                self.main_map[j].possibility = p

        return False

    def update(self, inp: list, composite: bool = True) -> None:
        """
        inp: list
            [
                (x: int, y:int, situation: int), ...
            ]
            x & y is the coordinates of the changed house
            situation is the situation in the House
        """
        for i in inp:
            if self[i[:2]] == i[2]:
                continue
            self[i[:2]] = i[2]

        while composite and self.composite_id():
            pass
        return self


if __name__ == "__main__":
    map = Map(7, 8, 15)
    # with open(path.join(".", "data_saver", "733292", "11.json"), "r") as f:
    with open(path.join(".", "data_saver", "753269", "05.json"), "r") as f:
        inp = [tuple(i) for i in load(f)]

    t1 = time()
    map.update(inp)
    t2 = time()

    print(map)
    print(map.moves())
    print(t2 - t1)
