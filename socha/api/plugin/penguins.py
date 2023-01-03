"""
This is the plugin for this year's game `Penguins`.
"""
import logging
import math
from enum import Enum
from typing import List, Optional


class Vector:
    """
    Represents a vector in the hexagonal grid. It can calculate various vector operations.
    """

    def __init__(self, d_x: int = 0, d_y: int = 0):
        """
        Constructor for the Vector class.

        :param d_x: The x-coordinate of the vector.
        :param d_y: The y-coordinate of the vector.
        """
        self.d_x = d_x
        self.d_y = d_y

    def magnitude(self) -> float:
        """
        Calculates the length of the vector.

        :return: The length of the vector.
        """
        return (self.d_x ** 2 + self.d_y ** 2) ** 0.5

    def dot_product(self, other: 'Vector'):
        """
        Calculates the dot product of two vectors.

        :param other: The other vector to calculate the dot product with.
        :return: The dot product of the two vectors.
        """
        return self.d_x * other.d_x + self.d_y * other.d_y

    def cross_product(self, other: 'Vector'):
        """
        Calculates the cross product of two vectors.

        :param other: The other vector to calculate the cross product with.
        :return: The cross product of the two vectors.
        """
        return self.d_x * other.d_y - self.d_y * other.d_x

    def scalar_product(self, scalar: int):
        """
        Extends the vector by a scalar.

        :param scalar: The scalar to extend the vector by.
        :return: The extended vector.
        """
        return Vector(self.d_x * scalar, self.d_y * scalar)

    def addition(self, other: 'Vector'):
        """
        Adds two vectors.

        :param other: The other vector to add.
        :return: The sum of the two vectors as a new vector object.
        """
        return Vector(self.d_x + other.d_x, self.d_y + other.d_y)

    def subtraction(self, other: 'Vector'):
        """
        Subtracts two vectors.

        :param other: The other vector to subtract.
        :return: The difference of the two vectors as a new vector object.
        """
        return Vector(self.d_x - other.d_x, self.d_y - other.d_y)

    def get_arc_tangent(self) -> float:
        """
        Calculates the arc tangent of the vector.

        :return: A radiant in float.
        """
        return math.degrees(math.atan2(self.d_y, self.d_x))

    def are_identically(self, other: 'Vector'):
        """
        Compares two vectors.

        :param other: The other vector to compare to.
        :return: True if the vectors are equal, false otherwise.
        """
        return self.d_x == other.d_x and self.d_y == other.d_y

    def are_equal(self, other: 'Vector'):
        """
        Checks if two vectors have the same magnitude and direction.

        :param other: The other vector to compare to.
        :return: True if the vectors are equal, false otherwise.
        """
        return self.magnitude() == other.magnitude() and self.get_arc_tangent() == other.get_arc_tangent()

    @property
    def directions(self) -> List['Vector']:
        """
        Gets the six neighbors of the vector.

        :return: A list of the six neighbors of the vector.
        """
        return [
            Vector(1, -1),  # UP RIGHT
            Vector(-2, 0),  # LEFT
            Vector(1, 1),  # DOWN RIGHT
            Vector(-1, 1),  # DOWN LEFT
            Vector(2, 0),  # Right
            Vector(-1, -1)  # UP LEFT
        ]

    def is_one_hex_move(self):
        """
        Checks if the vector points to a hexagonal field that is a direct neighbor.

        :return: True if the vector is a one hex move, false otherwise.
        """
        return abs(self.d_x) == abs(self.d_y) or (self.d_x % 2 == 0 and self.d_y == 0)

    def __str__(self) -> str:
        """
        Returns the string representation of the vector.

        :return: The string representation of the vector.
        """
        return f"Vector({self.d_x}, {self.d_x})"


class CartesianCoordinate:
    """
    Represents a coordinate in a normal cartesian coordinate system, that has been taught in school.
    This class is used to translate and represent a hexagonal coordinate in a cartesian and with that a 2D-Array.
    """

    def __init__(self, x: int, y: int):
        """
        Constructor for the CartesianCoordinate class.

        :param x: The x-coordinate on a cartesian coordinate system.
        :param y: The y-coordinate on a cartesian coordinate system.
        """
        self.x = x
        self.y = y

    def to_vector(self):
        """
        Converts the cartesian coordinate to a vector.
        """
        return Vector(d_x=self.x, d_y=self.y)

    def add_vector(self, vector: Vector) -> 'CartesianCoordinate':
        """
        Adds a vector to the cartesian coordinate.

        :param vector: The vector to add.
        :return: The new cartesian coordinate.
        """
        vector: Vector = self.to_vector().addition(vector)
        return CartesianCoordinate(x=vector.d_x, y=vector.d_y)

    def subtract_vector(self, vector: Vector) -> 'CartesianCoordinate':
        """
        Subtracts a vector from the cartesian coordinate.

        :param vector: The vector to subtract.
        :return: The new cartesian coordinate.
        """
        vector: Vector = self.to_vector().subtraction(vector)
        return CartesianCoordinate(x=vector.d_x, y=vector.d_y)

    def distance(self, other: 'CartesianCoordinate') -> float:
        """
        Calculates the distance between two cartesian coordinates.

        :param other: The other cartesian coordinate to calculate the distance to.
        :return: The distance between the two cartesian coordinates.
        """
        return self.to_vector().subtraction(other.to_vector()).magnitude()

    def to_hex(self) -> 'HexCoordinate':
        """
        Converts the cartesian coordinate to a hex coordinate.

        :return: The hex coordinate.
        """
        return HexCoordinate(x=self.x * 2 + (1 if self.y % 2 == 1 else 0), y=self.y)

    def to_index(self) -> Optional[int]:
        """
        Converts the cartesian coordinate to an index.

        :return: The index or None if the coordinate is not valid.
        """
        if 0 <= self.x <= 7 and 0 <= self.y <= 7:
            return self.y * 8 + self.x
        return None

    @staticmethod
    def from_index(index: int) -> Optional['CartesianCoordinate']:
        """
        Converts an index to a cartesian coordinate.

        :param index: The index to convert.
        :return: The cartesian coordinate.
        """
        if 0 <= index <= 63:
            return CartesianCoordinate(x=index % 8, y=int(index / 8))
        raise IndexError("Index out of range.")

    def __repr__(self) -> str:
        return f"CartesianCoordinate({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CartesianCoordinate) and self.x == other.x and self.y == other.y


class HexCoordinate:
    """
    Represents a coordinate in a hexagonal coordinate system, that differs from the normal cartesian one.
    This class is used to represent the hexagonal game board.
    """

    def __init__(self, x: int, y: int):
        """
        Constructor for the HexCoordinate class.

        :param x: The x-coordinate on a hexagonal coordinate system.
        :param y: The y-coordinate on a hexagonal coordinate system.
        """
        self.x = x
        self.y = y

    def to_cartesian(self) -> CartesianCoordinate:
        """
        Converts the hex coordinate to a cartesian coordinate.

        :return: The cartesian coordinate.
        """
        return CartesianCoordinate(x=math.floor((self.x / 2 - (1 if self.y % 2 == 1 else 0)) + 0.5), y=self.y)

    def to_vector(self) -> Vector:
        """
        Converts the hex coordinate to a vector.

        :return: The vector.
        """
        return Vector(d_x=self.x, d_y=self.y)

    def add_vector(self, vector: Vector) -> 'HexCoordinate':
        """
        Adds a vector to the hex coordinate.

        :param vector: The vector to add.
        :return: The new hex coordinate.
        """
        vector: Vector = self.to_vector().addition(vector)
        return HexCoordinate(x=vector.d_x, y=vector.d_y)

    def subtract_vector(self, vector: Vector) -> 'HexCoordinate':
        """
        Subtracts a vector from the hex coordinate.

        :param vector: The vector to subtract.
        :return: The new hex coordinate.
        """
        vector: Vector = self.to_vector().subtraction(vector)
        return HexCoordinate(x=vector.d_x, y=vector.d_y)

    def get_neighbors(self) -> List['HexCoordinate']:
        """
        Returns a list of all neighbors of the hex coordinate.

        :return: The list of neighbors.
        """
        return [self.add_vector(vector) for vector in self.to_vector().directions]

    def distance(self, other: 'HexCoordinate') -> float:
        """
        Calculates the distance between two hex coordinates.

        :param other: The other hex coordinate to calculate the distance to.
        :return: The distance between the two hex coordinates.
        """
        return self.to_vector().subtraction(other.to_vector()).magnitude()

    def __repr__(self) -> str:
        return f"HexCoordinate({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, HexCoordinate) and self.x == other.x and self.y == other.y


class TeamEnum(Enum):
    ONE = "ONE"
    TWO = "TWO"


class Team:
    """
    The Team class is useful for storing and manipulating information about teams in the game. It allows
    you to easily create objects for each team, keep track of their attributes, and compare them to their opponents.
    """

    def __init__(self, name: TeamEnum, penguins: Optional[List], fish: int):
        self.name = name
        self.penguins = penguins
        self.fish = fish

    def opponent(self) -> 'Team':
        if self.name == TeamEnum.ONE:
            return Team(TeamEnum.TWO, [], 0)
        else:
            return Team(TeamEnum.ONE, [], 0)

    def __repr__(self) -> str:
        return f"Team(name={self.name}, penguins={self.penguins}, fish={self.fish})"

    def __str__(self) -> str:
        return f"Team(name={self.name}, penguins={self.penguins}, fish={self.fish})"


class Move:
    """
        The Move class is a blueprint for creating objects that represent a move in a game. It has certain attributes
        that define what a move is and what it can do.

        The attributes of a Move object include the start position of the move (from_value), the end position of the
        move ( to_value), and the team making the move (team).

        The behaviors of a Move object include calculating the distance between the start and end positions (delta),
        creating a new Move object with the start and end positions reversed (reverse).

        You can create a Move object by calling the Move class and passing it the necessary information (the start
        and end positions and the team).
    """

    def __init__(self, from_value: Optional[HexCoordinate], to_value: HexCoordinate, team: TeamEnum):
        self.from_value = from_value
        self.to_value = to_value
        self.team = team

    def delta(self):
        if self.from_value is not None:
            return self.from_value.to_cartesian().distance(self.to_value.to_cartesian())
        return self.to_value.to_cartesian().distance(CartesianCoordinate(0, 0))

    def reverse(self):
        return Move(self.to_value, self.from_value if self.from_value is not None else HexCoordinate(0, 0), self.team)

    def __repr__(self):
        return f"Move(from={self.from_value}, to_value={self.to_value}, team={self.team})"

    def __str__(self):
        return f"Move(from={self.from_value}, to_value={self.to_value}, team={self.team})"


class Penguin:
    """
        The Penguin class is a blueprint for creating objects that represent a penguin in a game.

        You can create a Penguin object by calling the Penguin class and passing it the necessary information (the
        position and team). Once you have a Penguin object, you can use its attributes and methods to get information
        about the penguin or generate a string representation of the object.
    """

    def __init__(self, position: HexCoordinate, team: TeamEnum):
        self.position = position
        self.team = team

    def __repr__(self) -> str:
        return f"Penguin(position={self.position}, team={self.team})"

    def __str__(self) -> str:
        return f"Penguin(position={self.position}, team={self.team})"


class Field:
    """
        The Field class is a blueprint for creating objects that represent a field on a game board.

        You can create a Field object by calling the Field class and passing it the necessary information (the
        coordinate, penguin, and fish). Once you have a Field object, you can use its attributes and methods to get
        information about the field or generate a string representation of the object.
    """

    def __init__(self, coordinate: HexCoordinate, penguin: Optional[Penguin], fish: int):
        self.coordinate = coordinate
        self.penguin = penguin
        self.fish = fish

    def is_empty(self) -> bool:
        return self.fish == 0 and self.penguin is None

    def has_penguin(self) -> bool:
        return self.penguin is not None

    def get_team(self) -> Optional[TeamEnum]:
        if self.penguin:
            return self.penguin.team
        else:
            return None

    def __repr__(self) -> str:
        return f"Field(coordinate={self.coordinate}, penguin={self.penguin}, fish={self.fish})"

    def __str__(self) -> str:
        return f"Field(coordinate={self.coordinate}, penguin={self.penguin}, fish={self.fish})"


class Board:
    """
        The Board class represents a board in a game where each field on the board is represented by a
        single bit in a 64-bit integer. The class has several methods that allow you to manipulate the board,
        such as moving pieces around or checking whether two boards are equivalent.

        The class has several instance variables, each of which is a 64-bit integer that represents a different
        aspect of the board. For example, one variable might represent which fields have penguins on them and which
        do not, while another variable might represent which fields have fish on them.

        One of the main purposes of the Board class is to allow you to quickly check whether certain conditions
        are true about the board. For example, you might want to know whether two boards are equivalent, or whether a
        particular field is occupied by a penguin or fish. The class has methods that allow you to do these kinds of
        checks quickly, by using bitwise operations on the integers that represent the board.

        Another purpose of the Board class is to allow you to make changes to the board. For example, you might
        want to move a penguin from one field to another, or place a new penguin on the board. The class has methods
        that allow you to do these kinds of actions, by changing the values of the instance variables that represent
        the board.

        Overall, the Board class is a useful tool for representing and manipulating game boards in a fast and
        efficient way. It is especially useful in situations where you need to perform many different kinds of
        operations on the board, or where you need to quickly check the state of the board in different ways.
    """

    def __init__(self, one: int, two: int, fish_0: int, fish_1: int, fish_2: int, fish_3: int, fish_4: int):
        """
            Inits Board with given bitmasks.

            Args:
                one (int): Bitmask representing the penguins of team ONE
                two (int): Bitmask representing the penguins of team TWO
                fish_0 (int): Bitmask representing set 0 fish
                fish_1 (int): Bitmask representing set 1 fish
                fish_2 (int): Bitmask representing set 2 fish
                fish_3 (int): Bitmask representing set 3 fish
                fish_4 (int): Bitmask representing set 4 fish
        """
        self.one = one
        self.two = two
        self.fish_0 = fish_0
        self.fish_1 = fish_1
        self.fish_2 = fish_2
        self.fish_3 = fish_3
        self.fish_4 = fish_4

    @staticmethod
    def width():
        """Returns the width of the board."""
        return 8

    @staticmethod
    def height():
        """Returns the height of the board."""
        return 8

    def equivalence(self, other: 'Board') -> bool:
        """
            Returns True if this Board is equivalent to the given Board.

            Args:
                other (Board): Board to compare against

            Returns:
                bool: True if equivalent, False otherwise
            """
        return (
                self.one == other.one and self.two == other.two and
                self.fish_0 == other.fish_0 and self.fish_1 == other.fish_1 and
                self.fish_2 == other.fish_2 and self.fish_3 == other.fish_3 and
                self.fish_4 == other.fish_4
        )

    def is_empty(self) -> bool:
        """
            Returns True if all bitmasks in this Board are empty.

            Returns:
                bool: True if all bitmasks are empty, False otherwise
        """
        return (
                self.one == 0 and self.two == 0 and
                self.fish_0 == 0 and self.fish_1 == 0 and
                self.fish_2 == 0 and self.fish_3 == 0 and
                self.fish_4 == 0
        )

    def intersection(self, other: 'Board') -> 'Board':
        """
            Returns a new Board containing the intersection of the bitmasks in this and the given Board.

            Args:
                other (Board): Board to intersect with

            Returns:
                Board: New Board with intersecting bitmasks
        """
        return Board(self.one & other.one, self.two & other.two, self.fish_0 & other.fish_0,
                     self.fish_1 & other.fish_1, self.fish_2 & other.fish_2, self.fish_3 & other.fish_3,
                     self.fish_4 & other.fish_4)

    def union(self, other: 'Board') -> 'Board':
        """
            Returns a new Board containing the union of the bitmasks in this and the given Board.

            Args:
                other (Board): Board to union with

            Returns:
                Board: New Board with united bitmasks
        """
        return Board(self.one | other.one, self.two | other.two, self.fish_0 | other.fish_0,
                     self.fish_1 | other.fish_1, self.fish_2 | other.fish_2, self.fish_3 | other.fish_3,
                     self.fish_4 | other.fish_4)

    def difference(self, other: 'Board') -> 'Board':
        """
            Returns a new Board containing the difference of the bitmasks in this and the given Board.

            Args:
                other (Board): Board to difference with

            Returns:
                Board: New Board with bitmasks representing the difference between this and the given Board
        """
        return Board(self.one & ~other.one, self.two & ~other.two, self.fish_0 & ~other.fish_0,
                     self.fish_1 & ~other.fish_1, self.fish_2 & ~other.fish_2, self.fish_3 & ~other.fish_3,
                     self.fish_4 & ~other.fish_4)

    def disjoint(self, other: 'Board') -> bool:
        """
            Returns True if the bitmasks in this and the given Board have no intersections.

            Args:
                other (Board): Board to check for intersection with

            Returns:
                bool: True if no intersection, False otherwise
        """
        return self.intersection(other).is_empty()

    def complement(self) -> 'Board':
        """
            Returns a new Board containing the complement of the bitmasks in this Board.

            Returns:
                Board: New Board with complemented bitmasks
        """
        return Board(~self.one, ~self.two, ~self.fish_0, ~self.fish_1, ~self.fish_2, ~self.fish_3, ~self.fish_4)

    def implication(self, other: 'Board') -> 'Board':
        """
            Returns a new Board containing the result of the implication of the bitmasks in this
            and the given Board.

            Args:
                other (Board): Board to perform implication with

            Returns:
                Board: New Board with bitmasks representing the implication of this and the given Board
        """
        return Board((~self.one) | other.one, (~self.two) | other.two, (~self.fish_0) | other.fish_0,
                     (~self.fish_1) | other.fish_1, (~self.fish_2) | other.fish_2, (~self.fish_3) | other.fish_3,
                     (~self.fish_4) | other.fish_4)

    def exclusive_or(self, other: 'Board') -> 'Board':
        """
            Returns a new Board containing the result of the exclusive or (XOR) of the bitmasks in this
            and the given Board.

            Args:
                other (Board): Board to perform exclusive or with

            Returns:
                Board: New Board with bitmasks representing the exclusive or of this and the given Board
        """
        return Board(self.one ^ other.one, self.two ^ other.two, self.fish_0 ^ other.fish_0,
                     self.fish_1 ^ other.fish_1, self.fish_2 ^ other.fish_2, self.fish_3 ^ other.fish_3,
                     self.fish_4 ^ other.fish_4)

    def empty_bitmask(self) -> int:
        """
            Returns an integer representing a bitmask with all bits set to 1 except for the bits
            set in any of the bitmasks in this Board.

            Returns:
                int: Bitmask with all bits set except those set in this Board
        """
        return ~(self.one | self.two | self.fish_0 | self.fish_1 | self.fish_2 | self.fish_3 | self.fish_4)

    def update(self, move: Move):
        """
            Updates this Board to reflect the given move.

            Args:
                move (Move): Move to reflect in this Board
        """
        if move.from_value is not None:
            from_coord = move.from_value.to_cartesian().to_index()
            to_coord = move.to_value.to_cartesian().to_index()
            if move.team == TeamEnum.ONE:
                self.one ^= 1 << from_coord
                self.one |= 1 << to_coord
            elif move.team == TeamEnum.TWO:
                self.two ^= 1 << from_coord
                self.two |= 1 << to_coord
        else:
            to_coord = move.to_value.to_cartesian().to_index()
            if move.team == TeamEnum.ONE:
                self.one |= 1 << to_coord
            elif move.team == TeamEnum.TWO:
                self.two |= 1 << to_coord

    def set_field(self, field: Field):
        """
            Sets the bitmasks in this Board to reflect the given field.

            Args:
                field (Field): Field to reflect in this Board
        """
        if field.penguin is not None:
            penguin = field.penguin
            index = penguin.position.to_cartesian().to_index()
            if penguin.team == TeamEnum.ONE:
                self.one |= 1 << index
            elif penguin.team == TeamEnum.TWO:
                self.two |= 1 << index
        else:
            fish = field.fish
            index = field.coordinate.to_cartesian().to_index()
            if fish == 0:
                self.fish_0 |= 1 << index
            elif fish == 1:
                self.fish_1 |= 1 << index
            elif fish == 2:
                self.fish_2 |= 1 << index
            elif fish == 3:
                self.fish_3 |= 1 << index
            elif fish == 4:
                self.fish_4 |= 1 << index
            else:
                raise Exception(f"Fish value not allowed.\nFish value was: {fish}")

    def get_penguin(self, coordinate: HexCoordinate) -> Optional[Penguin]:
        """
            Returns the penguin at the given coordinate, if any.

            Args:
                coordinate (HexCoordinate): Coordinate to get penguin at

            Returns:
                Optional[Penguin]: Penguin at the given coordinate, or None if no penguin present
        """
        index = coordinate.to_cartesian().to_index()
        if self.one & (1 << index) != 0:
            return Penguin(coordinate, TeamEnum.ONE)
        elif self.two & (1 << index) != 0:
            return Penguin(coordinate, TeamEnum.TWO)
        else:
            return None

    def get_fish(self, index: int) -> int:
        """
            Returns the value of the fish at the given index.

            Args:
                index (int): Index of fish to get value of

            Returns:
                int: Value of fish at the given index
        """
        if self.fish_0 & (1 << index) != 0:
            return 0
        elif self.fish_1 & (1 << index) != 0:
            return 1
        elif self.fish_2 & (1 << index) != 0:
            return 2
        elif self.fish_3 & (1 << index) != 0:
            return 3
        elif self.fish_4 & (1 << index) != 0:
            return 4
        else:
            return 0

    def get_field(self, index: int) -> Field:
        """
            Returns the field at the given index.

            Args:
                index (int): Index of field to get

            Returns:
                Field: Field at the given index
        """
        coordinate = CartesianCoordinate.from_index(index).to_hex()
        penguin = self.get_penguin(coordinate)
        fish = self.get_fish(coordinate.to_cartesian().to_index())
        field = Field(coordinate, penguin, fish)
        return field

    def is_occupied(self, index: int) -> bool:
        """
            Returns True if the field at the given index is occupied by a penguin.

            Args:
                index (int): Index of field to check

            Returns:
                bool: True if field is occupied, False otherwise
        """
        return (self.one & (1 << index) != 0) or (self.two & (1 << index) != 0)

    @staticmethod
    def is_valid(index: int) -> bool:
        """
            Returns True if the given index is valid (i.e., within the range of the board).

            Args:
                index (int): Index to check for validity

            Returns:
                bool: True if index is valid, False otherwise
        """
        return index < 64

    def contains_field(self, index: int) -> bool:
        """
            Returns True if the field at the given index is occupied or contains fish.

            Args:
                index (int): Index of field to check

            Returns:
                bool: True if field is occupied or contains fish, False otherwise
        """
        return (self.one & (1 << index) != 0) or (self.two & (1 << index) != 0) or (
                self.fish_0 & (1 << index) != 0) or (self.fish_1 & (1 << index) != 0) or (
                       self.fish_2 & (1 << index) != 0) or (self.fish_3 & (1 << index) != 0) or (
                       self.fish_4 & (1 << index) != 0)

    def contains(self, indexes: List[int]) -> bool:
        """
            Returns True if all the fields at the given indexes are occupied or contain fish.

            Args:
                indexes (List[int]): Indexes of fields to check

            Returns:
                bool: True if all fields are occupied or contain fish, False otherwise
        """
        for index in indexes:
            if not self.contains_field(index):
                return False
        return True

    def is_team(self, team: TeamEnum, index: int) -> bool:
        """
            Returns True if the field at the given index is occupied by a penguin of the given team.

            Args:
                team (TeamEnum): Team to check for
                index (int): Index of field to check

            Returns:
                bool: True if field is occupied by a penguin of the given team, False otherwise
        """
        if team == TeamEnum.ONE:
            return self.one & (1 << index) != 0
        elif team == TeamEnum.TWO:
            return self.two & (1 << index) != 0

    @staticmethod
    def get_coordinates(bitboard: int) -> List[HexCoordinate]:
        """
            Returns a list of the hexagonal coordinates occupied or containing fish in the given bitmask.

            Args:
                bitboard (int): Bitmask to get coordinates from

            Returns:
                List[HexCoordinate]: List of coordinates occupied or containing fish in the given bitmask
        """
        coordinates = []
        for index in range(64):
            if bitboard & (1 << index) != 0:
                coordinates.append(CartesianCoordinate.from_index(index).to_hex())
        return coordinates

    @staticmethod
    def get_bit_coordinate(field: 'Board') -> Optional[HexCoordinate]:
        """
            Returns the hexagonal coordinate occupied or containing fish in the given Board, if there is exactly one.

            Args:
                field (Board): Board to get coordinate from

            Returns:
                Optional[HexCoordinate]: Coordinate occupied or containing fish in the given Board,
                if there is exactly one

            Raises:
                ValueError: If there is not exactly one bit set in the given Board
        """
        fields = [field.one, field.two, field.fish_0, field.fish_1, field.fish_2, field.fish_3, field.fish_4]

        count = 0
        index = 0
        for i in range(64):
            for f in fields:
                if f & (1 << index) != 0:
                    count += 1
            index = i
        if count == 1:
            return CartesianCoordinate.from_index(index).to_hex()
        else:
            raise ValueError("More than one bit set in bitboards")

    def get_directive_moves(self, index: int, direction: Vector, team: TeamEnum) -> List[Move]:
        """
            Returns a list of moves that can be made in a given direction from a given index, for a given team.

            Moves are only returned if they are to an unoccupied field that contains fish.

            Args:
                index (int): Index to start from
                direction (Vector): Direction to move in
                team (TeamEnum): Team to make moves for

            Returns:
                List[Move]: List of moves that can be made in the given direction from the given index,
                            for the given team
        """
        moves = []
        origin = CartesianCoordinate.from_index(index).to_hex()
        if self.is_team(team, index):
            new_index = CartesianCoordinate.from_index(index).to_hex().add_vector(direction).to_cartesian().to_index()
            while new_index is not None and self.is_valid(new_index) and not self.is_occupied(
                    new_index) and self.get_fish(new_index) > 0:
                moves.append(Move(origin, CartesianCoordinate.from_index(new_index).to_hex(), team))
                new_index = CartesianCoordinate.from_index(new_index).to_hex().add_vector(
                    direction).to_cartesian().to_index()
        return moves

    def possible_moves_from(self, index: int, team: TeamEnum) -> List[Move]:
        """
            Returns a list of all possible moves that can be made from a given index, for a given team.

            Moves are to unoccupied fields that contain fish.

            Args:
                index (int): Index to start from
                team (TeamEnum): Team to make moves for

            Returns:
                List[Move]: List of all possible moves that can be made from the given index, for the given team
        """
        moves = []
        for direction in Vector().directions:
            moves += self.get_directive_moves(index, direction, team)
        return moves

    def move(self, move: Move) -> 'Board':
        """
            Returns a new Board object with a move applied to it.

            The move can involve moving a penguin to an unoccupied field, or placing a new penguin on the board.

            Args:
                move (Move): The move to apply to the board

            Returns:
                Board: A new Board object with the move applied
        """
        new_board = self
        origin = move.from_value
        destination = move.to_value
        origin_index = origin.to_cartesian().to_index()
        destination_index = destination.to_cartesian().to_index()
        origin_field = self.get_field(origin_index)
        destination_field = self.get_field(destination_index)
        new_board.set_field(origin_field)
        new_board.set_field(destination_field)

        return new_board

    def get_empty_fields(self) -> List[Field]:
        """
            Returns a list of Field objects representing the empty fields on the board.

            Returns:
                A list of Field objects that has 0 fish.
        """
        empty_fields = []
        empty_bits = self.empty_bitmask()
        for index in range(63):
            if empty_bits >> index & 1 != 0:
                coordinate = CartesianCoordinate.from_index(index).to_hex()
                fish = self.get_fish(coordinate.to_cartesian().to_index())
                field = Field(coordinate, None, fish)
                empty_fields.append(field)
        return empty_fields

    def get_penguins(self) -> List[Penguin]:
        """
            Returns a list of Penguin objects representing the penguins on the board.

            Returns:
                A list of Penguin objects.
        """
        penguins = []
        for index in range(64):
            if self.one >> index & 1 != 0:
                coordinate = CartesianCoordinate.from_index(index).to_hex()
                penguins.append(Penguin(coordinate, TeamEnum.ONE))
            if self.two >> index & 1 != 0:
                coordinate = CartesianCoordinate.from_index(index).to_hex()
                penguins.append(Penguin(coordinate, TeamEnum.TWO))
        return penguins

    def get_teams_penguins(self, team: TeamEnum) -> List[Penguin]:
        """
            Returns a list of Penguin objects representing the penguins belonging to the given team.

            Args:
                team: The team whose penguins should be returned.

            Returns:
                A list of Penguin objects belonging to the given team.
        """
        penguins = []
        for index in range(64):
            if team == TeamEnum.ONE and self.one >> index & 1 != 0:
                coordinate = CartesianCoordinate.from_index(index).to_hex()
                penguins.append(Penguin(coordinate, TeamEnum.ONE))
            if team == TeamEnum.TWO and self.two >> index & 1 != 0:
                coordinate = CartesianCoordinate.from_index(index).to_hex()
                penguins.append(Penguin(coordinate, TeamEnum.TWO))
        return penguins

    def get_most_fish(self) -> List[Field]:
        """
            Returns a list of fields containing the most fish

            This method returns a list of fields which contain the maximum number of fish
            across all fields.

            Returns:
                List[Field]: A list of fields containing the most fish
        """
        max_fish = max(self.fish_0, self.fish_1, self.fish_2, self.fish_3, self.fish_4)
        fields_with_most_fish = []
        for i in range(64):
            coordinate = CartesianCoordinate.from_index(i).to_hex()
            fish = self.get_fish(coordinate.to_cartesian().to_index())
            field = Field(coordinate, None, fish)
            if (self.fish_0 & (1 << i)) and self.fish_0 == max_fish:
                fields_with_most_fish.append(field)
            elif (self.fish_1 & (1 << i)) and self.fish_1 == max_fish:
                fields_with_most_fish.append(field)
            elif (self.fish_2 & (1 << i)) and self.fish_2 == max_fish:
                fields_with_most_fish.append(field)
            elif (self.fish_3 & (1 << i)) and self.fish_3 == max_fish:
                fields_with_most_fish.append(field)
            elif (self.fish_4 & (1 << i)) and self.fish_4 == max_fish:
                fields_with_most_fish.append(field)
        return fields_with_most_fish

    def __repr__(self) -> str:
        string = ""
        string += "\n"
        for index in range(64):
            if self.one & (1 << index) != 0:
                string += "□"
            elif self.two & (1 << index) != 0:
                string += "■"
            elif self.fish_0 & (1 << index) != 0:
                string += "0"
            elif self.fish_1 & (1 << index) != 0:
                string += "1"
            elif self.fish_2 & (1 << index) != 0:
                string += "2"
            elif self.fish_3 & (1 << index) != 0:
                string += "3"
            elif self.fish_4 & (1 << index) != 0:
                string += "4"
            else:
                string += "."
            string += "  "
            if index % 8 == 7:
                string += "\n"
        return string


class Fishes:
    """
    Represents the amount of fish each player has.
    """

    def __init__(self, fishes_one: int, fishes_two: int):
        self.fishes_one = fishes_one
        self.fishes_two = fishes_two

    def get_fish_by_team(self, team: Team):
        """
        Looks up the amount of fish a team has.

        :param team: A team object, that represents the team to get the fish amount of.
        :return: The amount of fish of the given team.
        """
        return self.fishes_one if team.name == TeamEnum.ONE else self.fishes_two

    def add_fish(self, team: Team, fish: int):
        if team.name == TeamEnum.ONE:
            self.fishes_one += fish
        elif team.name == TeamEnum.TWO:
            self.fishes_two += fish
        else:
            raise ValueError(f"Invalid team: {team}")
        return self


class GameState:
    """
    The GameState object is a central component of a game and stores important information about the current state of
    the game. This information includes:

    - The game board
    - The turn number and whose turn it is
    - The team that started the game
    - The number of fish each player has
    - The last move made

    In addition to storing this information, the GameState also provides helpful methods for:

    - Calculating available moves
    - Simulating future game states

    After each completed move, the game server sends a copy of the updated GameState to both participating players,
    keeping them informed about the current state of the game.
    """

    def __init__(self, board: Board, turn: int, start_team: Team, fishes: Fishes, last_move: Move = None):
        """
        Creates a new `GameState` with the given parameters.

        :param board: The board of the game.
        :param turn: The turn number of the game.
        :param start_team: The team that has the first turn.
        :param fishes: The number of fishes each team has.
        :param last_move: The last move made.
        """
        self.start_team = start_team
        self.board = board
        self.turn = turn
        self.round = int((self.turn + 1) / 2)
        self.current_team = self.current_team_from_turn()
        self.other_team = self.current_team_from_turn().opponent()
        self.last_move = last_move
        self.fishes = fishes
        self.current_pieces = self.board.get_teams_penguins(self.current_team.name)
        self.possible_moves = self._get_possible_moves(self.current_team)

    def _get_possible_moves(self, current_team: Team = None) -> List[Move]:
        current_team = current_team.name or self.current_team.name
        fields = [self.board.get_field(CartesianCoordinate(x, y).to_index()) for x in range(self.board.width()) for y in
                  range(self.board.height())]
        if len(self.board.get_teams_penguins(current_team)) < 4:
            moves = [Move(from_value=None, to_value=field.coordinate, team=current_team) for field in fields if
                     not field.penguin and field.fish == 1]
        else:
            moves = [move for penguin in self.board.get_teams_penguins(current_team) for move in
                     self.board.possible_moves_from(penguin)]
        return moves

    def current_team_from_turn(self) -> Team:
        """
        Calculates the current team from the turn number.

        :return: The team that has the current turn.
        """
        current_team_by_turn = self.start_team if self.turn % 2 == 0 else self.start_team.opponent()
        return current_team_by_turn.opponent() if not self._get_possible_moves(current_team_by_turn) else \
            current_team_by_turn

    def perform_move(self, move: Move) -> 'GameState':
        """
        Performs the given move on the current game state.

        :param move: The move to perform.
        :return: The new game state after the move has been performed.
        """
        if not self.is_valid_move(move):
            logging.error(f"Performed invalid move while simulating: {move}")
            raise Exception(f"Invalid move: {move}")

        new_board = self.board.move(move)
        new_fishes = self.fishes.add_fish(self.current_team,
                                          new_board.get_field(move.to_value.to_cartesian().to_index()).fish)
        return GameState(board=new_board, turn=self.turn + 1, start_team=self.start_team, fishes=new_fishes,
                         last_move=move)

    def is_valid_move(self, move: Move) -> bool:
        """
        Checks if the given move is valid.

        :param move: The move to check.
        :return: True if the move is valid, False otherwise.
        """
        return move in self.possible_moves
