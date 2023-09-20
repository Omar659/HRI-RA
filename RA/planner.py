from unified_planning.shortcuts import *
from unified_planning.engines import PlanGenerationResultStatus
import random
import copy
import sys
sys.path.append('./')
sys.path.append('./utils')
from utils.config import *

class Slide_tile_cell():
    def __init__(self, n, other=None):
        self.n = n
        self.other = other

class Slide_tile():
    def __init__(self, n_row, n_col, n_moves=100):
        self.n_row = n_row
        self.n_col = n_col
        self.tiles, self.b_x, self.b_y = self.__generate_tiles()
        self.shuffle(n_moves)

    def __generate_tiles(self):
        tiles = []
        for i in range(self.n_row):
            row = []
            for j in range(self.n_col):
                if i == self.n_row-1 and j == self.n_col-1:
                    c = Slide_tile_cell("-")
                else:
                    c = Slide_tile_cell(str(i*self.n_col + j))
                row.append(c)
            tiles.append(row)
        return tiles, i, j

    def return_tiles(self):
        tiles = []
        for i in range(self.n_row):
            row = []
            for j in range(self.n_col):
                row.append(self.tiles[i][j].n)
            tiles.append(row)
        return tiles

    def generate_tiles_from_mat(self, mat, bx, by):
        self.tiles = []
        self.b_x = bx
        self.b_y = by
        for i in range(self.n_row):
            row = []
            for j in range(self.n_col):
                c = Slide_tile_cell(str(mat[i][j]))
                row.append(c)
            self.tiles.append(row)

    def shuffle(self, n_moves=100):
        for i in range(n_moves):
            r = random.randint(0,3)
            if r == 0:
                self.move_up()
            if r == 1:
                self.move_down()
            if r == 2:
                self.move_right()
            if r == 3:
                self.move_left()
        return

    def move_down(self):
        if self.b_x != 0:
            tmp = self.tiles[self.b_x-1][self.b_y]
            self.tiles[self.b_x-1][self.b_y] = self.tiles[self.b_x][self.b_y]
            self.tiles[self.b_x][self.b_y] = tmp
            self.b_x -= 1

    def move_up(self):
        if self.b_x != self.n_row-1:
            tmp = self.tiles[self.b_x+1][self.b_y]
            self.tiles[self.b_x+1][self.b_y] = self.tiles[self.b_x][self.b_y]
            self.tiles[self.b_x][self.b_y] = tmp
            self.b_x += 1

    def move_right(self):
        if self.b_y != 0:
            tmp = self.tiles[self.b_x][self.b_y-1]
            self.tiles[self.b_x][self.b_y-1] = self.tiles[self.b_x][self.b_y]
            self.tiles[self.b_x][self.b_y] = tmp
            self.b_y -= 1

    def move_left(self):
        if self.b_y != self.n_col-1:
            tmp = self.tiles[self.b_x][self.b_y+1]
            self.tiles[self.b_x][self.b_y+1] = self.tiles[self.b_x][self.b_y]
            self.tiles[self.b_x][self.b_y] = tmp
            self.b_y += 1

    def __str__(self):
        s = ""
        for i in range(self.n_row):
            for j in range(self.n_col):
                s += self.tiles[i][j].n + " "
            s += "\n"
        s = s[:-1]
        return s

    def __repr__(self):
        return self.__str__()

class Slide_tile_PDDL():
    def __init__(self, difficult="easy", optimal_plan = False, verbose = True):
        up.shortcuts.get_environment().credits_stream = None
        self.difficult = difficult
        self.verbose = verbose
        self.optimal_plan = optimal_plan
        # Slide tile init
        if self.difficult.lower() == "easy":
            self.slide_tile = Slide_tile(3, 3)
        if self.difficult.lower() == "medium":
            self.slide_tile = Slide_tile(3, 4, 80)
        if self.difficult.lower() == "hard":
            self.slide_tile = Slide_tile(4, 4, 80)
        if self.verbose:
            print("GAME")
            print(self.slide_tile)
            print()
        # Types
        self.Tile = UserType("Tile")
        self.Position = UserType("Position")
        # Fluents
        self.is_tile = Fluent("is_tile", BoolType(), t=self.Tile)
        self.is_position = Fluent("is_position", BoolType(), p=self.Position)
        self.blank = Fluent("blank", BoolType(), bx=self.Position, by=self.Position)
        self.at = Fluent("at", BoolType(), t=self.Tile, px=self.Position, py=self.Position)
        self.dec = Fluent("dec", BoolType(), p1=self.Position, p2=self.Position)
        self.inc = Fluent("inc", BoolType(), p1=self.Position, p2=self.Position)
        # Problem
        self.create_problem()
        # Plan
        self.solve_problem()

    def __move_up(self):
        # SET VALUE
        up = InstantaneousAction("Move Up", t=self.Tile, px=self.Position, py=self.Position, bx=self.Position)
        t = up.parameter("t")
        px = up.parameter("px")
        py = up.parameter("py")
        bx = up.parameter("bx")
        # Preconditions
        up.add_precondition(self.is_tile(t))
        up.add_precondition(self.is_position(px))
        up.add_precondition(self.is_position(py))
        up.add_precondition(self.is_position(bx))
        up.add_precondition(self.inc(bx, px))
        up.add_precondition(self.blank(bx, py))
        up.add_precondition(self.at(t, px, py))
        # Effects
        up.add_effect(self.blank(bx, py), False)
        up.add_effect(self.at(t, px, py), False)
        up.add_effect(self.blank(px, py), True)
        up.add_effect(self.at(t, bx, py), True)
        return up

    def __move_down(self):
        down = InstantaneousAction("Move Down", t=self.Tile, px=self.Position, py=self.Position, bx=self.Position)
        # Parameters
        t = down.parameter("t")
        px = down.parameter("px")
        py = down.parameter("py")
        bx = down.parameter("bx")
        # Preconditions
        down.add_precondition(self.is_tile(t))
        down.add_precondition(self.is_position(px))
        down.add_precondition(self.is_position(py))
        down.add_precondition(self.is_position(bx))
        down.add_precondition(self.dec(bx, px))
        down.add_precondition(self.blank(bx, py))
        down.add_precondition(self.at(t, px, py))
        # Effects
        down.add_effect(self.blank(bx, py), False)
        down.add_effect(self.at(t, px, py), False)
        down.add_effect(self.blank(px, py), True)
        down.add_effect(self.at(t, bx, py), True)
        return down

    def __move_left(self):
        left = InstantaneousAction("Move Left", t=self.Tile, px=self.Position, py=self.Position, by=self.Position)
        # Parameters
        t = left.parameter("t")
        px = left.parameter("px")
        py = left.parameter("py")
        by = left.parameter("by")
        # Preconditions
        left.add_precondition(self.is_tile(t))
        left.add_precondition(self.is_position(px))
        left.add_precondition(self.is_position(py))
        left.add_precondition(self.is_position(by))
        left.add_precondition(self.inc(by, py))
        left.add_precondition(self.blank(px, by))
        left.add_precondition(self.at(t, px, py))
        # Effects
        left.add_effect(self.blank(px, by), False)
        left.add_effect(self.at(t, px, py), False)
        left.add_effect(self.blank(px, py), True)
        left.add_effect(self.at(t, px, by), True)
        return left

    def __move_right(self):
        right = InstantaneousAction("Move Right", t=self.Tile, px=self.Position, py=self.Position, by=self.Position)
        # Parameters
        t = right.parameter("t")
        px = right.parameter("px")
        py = right.parameter("py")
        by = right.parameter("by")
        # Preconditions
        right.add_precondition(self.is_tile(t))
        right.add_precondition(self.is_position(px))
        right.add_precondition(self.is_position(py))
        right.add_precondition(self.is_position(by))
        right.add_precondition(self.dec(by, py))
        right.add_precondition(self.blank(px, by))
        right.add_precondition(self.at(t, px, py))
        # Effects
        right.add_effect(self.blank(px, by), False)
        right.add_effect(self.at(t, px, py), False)
        right.add_effect(self.blank(px, py), True)
        right.add_effect(self.at(t, px, by), True)
        return right

    def create_problem(self):
        # PROBLEM
        self.problem = Problem('problem')
        if self.optimal_plan:
            metric = MinimizeSequentialPlanLength()
            self.problem.add_quality_metric(metric)

        # FLUENT
        # Type checks
        self.problem.add_fluent(self.is_tile, default_initial_value=False)
        self.problem.add_fluent(self.is_position, default_initial_value=False)
        # Positions
        self.problem.add_fluent(self.blank, default_initial_value=False)
        self.problem.add_fluent(self.at, default_initial_value=False)
        # Connections
        self.problem.add_fluent(self.dec, default_initial_value=False)
        self.problem.add_fluent(self.inc, default_initial_value=False)

        # OBJECTS
        self.x_coordinates = []
        self.y_coordinates = []
        self.tiles = []
        # x-coordinates
        for i in range(self.slide_tile.n_row):
            self.x_coordinates.append(Object("x" + str(i), self.Position))
            self.problem.add_object(self.x_coordinates[-1])
        # y-coordinates
        for i in range(self.slide_tile.n_col):
            self.y_coordinates.append(Object("y" + str(i), self.Position))
            self.problem.add_object(self.y_coordinates[-1])
        # Tiles
        tiles_counter = 0
        for i in range(self.slide_tile.n_row):
            for j in range(self.slide_tile.n_col):
                if (i == self.slide_tile.n_row-1 and j == self.slide_tile.n_col-1):
                    continue
                self.tiles.append(Object("t" + str(tiles_counter), self.Tile))
                self.problem.add_object(self.tiles[-1])
                tiles_counter += 1

        # FLUENTS INIT
        # Position check for x-coordinates
        for x_coordinate in self.x_coordinates:
            self.problem.set_initial_value(self.is_position(x_coordinate), True)
        # Position check for y-coordinates
        for y_coordinate in self.y_coordinates:
            self.problem.set_initial_value(self.is_position(y_coordinate), True)
        # Position check for tiles
        for tile in self.tiles:
            self.problem.set_initial_value(self.is_tile(tile), True)
        # Connection increment x-coordinates
        for i, x_coordinate in enumerate(self.x_coordinates[:-1]):
            self.problem.set_initial_value(self.inc(x_coordinate, self.x_coordinates[i+1]), True)
        # Connection decrement x-coordinates
        for i, x_coordinate in enumerate(self.x_coordinates[1:]):
            self.problem.set_initial_value(self.dec(x_coordinate, self.x_coordinates[i]), True)
        # Connection increment y-coordinates
        for i, y_coordinate in enumerate(self.y_coordinates[:-1]):
            self.problem.set_initial_value(self.inc(y_coordinate, self.y_coordinates[i+1]), True)
        # Connection decrement y-coordinates
        for i, y_coordinate in enumerate(self.y_coordinates[1:]):
            self.problem.set_initial_value(self.dec(y_coordinate, self.y_coordinates[i]), True)
        # Tiles positions
        for i in range(self.slide_tile.n_row):
            for j in range(self.slide_tile.n_col):
                t = self.slide_tile.tiles[i][j].n
                if t != "-":
                    self.problem.set_initial_value(self.at(self.tiles[int(t)],
                                                      self.x_coordinates[i],
                                                      self.y_coordinates[j]), True)
        # Tiles positions
        self.problem.set_initial_value(self.blank(self.x_coordinates[self.slide_tile.b_x],
                                             self.y_coordinates[self.slide_tile.b_y]), True)

        # ACTION
        self.problem.add_action(self.__move_up())
        self.problem.add_action(self.__move_down())
        self.problem.add_action(self.__move_right())
        self.problem.add_action(self.__move_left())

        # GOAL
        tiles_idx = 0
        for i in range(self.slide_tile.n_row):
            for j in range(self.slide_tile.n_col):
                if (i == self.slide_tile.n_row-1 and j == self.slide_tile.n_col-1):
                    continue
                self.problem.add_goal(self.at(self.tiles[tiles_idx],
                                         self.x_coordinates[i],
                                         self.y_coordinates[j]))
                tiles_idx += 1

        # PRINT
        if self.verbose:
            print("PROBLEM INITIALIZATION IN PDDL")
            print(self.problem)
            print()

    def solve_problem(self, timeout=False):
        opt = PlanGenerationResultStatus.SOLVED_OPTIMALLY if (self.optimal_plan and not timeout) else None
        with OneshotPlanner(problem_kind=self.problem.kind, optimality_guarantee=opt) as planner:
            if self.optimal_plan and not timeout:
                if self.verbose:
                    print("Searching for optimal plan...")
                result = planner.solve(self.problem, timeout=TIMEOUT)
                if result.status == PlanGenerationResultStatus.TIMEOUT:
                    if self.verbose:
                        print("Optimal plan not fond in less than", TIMEOUT, "seconds")
                        print("Searching for non optimal plan...")
                    self.solve_problem(timeout=True)
                    return
            else:
                result = planner.solve(self.problem)
            if self.verbose:
                print(result)
            self.plan = result.plan
            if self.plan is None and self.verbose:
                print("No plan found.")

    def check_plan(self):
        if self.plan is None:
            print("No plan to check")
        else:
            if self.verbose:
                print("\nCHECK THE PLAN")
                st = copy.deepcopy(self.slide_tile)
                for action in self.plan.actions:
                    move = str(action).split("(")[0].split(" ")[1]
                    print(move)
                    if move == "Up":
                        st.move_up()
                    elif move == "Down":
                        st.move_down()
                    elif move == "Right":
                        st.move_right()
                    else:
                        st.move_left()
                    print(st)
                    print()
            else:
                print("Verbose setted to False")