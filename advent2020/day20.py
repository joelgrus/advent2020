from __future__ import annotations
from typing import NamedTuple, List, Tuple, Iterator, Dict, Set, Optional
from collections import Counter
import math

Edge = str

class Edges(NamedTuple):
    top: Edge
    bottom: Edge
    left: Edge
    right: Edge

Pixels = List[List[str]]

class Tile(NamedTuple):
    tile_id: int
    pixels: Pixels

    def rotate(self, n: int) -> Tile:
        """
        Rotate the tile clockwise n times
        and return a new Tile object
        """
        pixels = self.pixels
        for _ in range(n):
            rotated = []
            for c in range(len(pixels[0])):
                rotated.append([row[c] for row in reversed(pixels)])
            pixels = rotated
        return self._replace(pixels=pixels)

    def flip_horizontal(self, do: bool = False) -> Tile:
        """
        Flip the tile horizontally and return a new tile object
        """
        pixels = [list(reversed(row)) for row in self.pixels] if do else self.pixels
        return self._replace(pixels=pixels)

    def flip_vertical(self, do: bool = False) -> Tile:
        """
        Flip the tile vertically and return a new tile object
        """
        pixels = list(reversed(self.pixels)) if do else self.pixels
        return self._replace(pixels=pixels)

    def all_rotations(self) -> Iterator[Tile]:
        """
        Return the 8 tiles I can get from this one 
        by doing rotations and flips
        """
        for flip_h in [True, False]:
            for rot in [0, 1, 2, 3]:
                yield (self
                    .flip_horizontal(flip_h)
                    .rotate(rot)
                )
                        

    def show(self) -> None:
        for row in self.pixels:
            print(''.join(row))

    @property
    def top(self) -> str:
        return ''.join(self.pixels[0])

    @property
    def bottom(self) -> str:
        return ''.join(self.pixels[-1])

    @property
    def left(self) -> str:
        return ''.join([row[0] for row in self.pixels])

    @property
    def right(self) -> str:
        return ''.join([row[-1] for row in self.pixels])

    def edges(
        self,
        reverse: bool = False
    ) -> Edges:
        """
        Returns the edges of the tile as strings.
        If reverse == True, rotates the tile by 180 degrees first,
        which results in all the edges being in the opposite direction
        """
        if reverse:
            return self.rotate(2).edges()
        return Edges(
            top=self.top, bottom=self.bottom, right=self.right, left=self.left
        )

    @staticmethod
    def parse(raw_tile: str) -> Tile:
        lines = raw_tile.split("\n")
        tile_id = int(lines[0].split()[-1][:-1])
        pixels = [list(line) for line in lines[1:]]
        return Tile(tile_id, pixels)

def make_tiles(raw: str) -> List[Tile]:
    tiles_raw = raw.split("\n\n")
    return [Tile.parse(tile_raw) for tile_raw in tiles_raw]


def find_corners(tiles: List[Tile]) -> List[Tile]:
    """
    Return corners oriented so that
    they would be the top left corner
    """
    # count up all the edges / reverse edges that occur
    # for example, if a tile had the top edge "ABCD",
    # we would count "ABCD" once and also "DCBA" once
    edge_counts = Counter(
        edge 
        for tile in tiles 
        for reverse in [True, False]
        for edge in tile.edges(reverse)
    )

    corners = []

    for tile in tiles:
        sides_with_no_matches = 0
        for edge in tile.edges():
            if edge_counts[edge] == 1 and edge_counts[edge[::-1]] == 1:
                sides_with_no_matches += 1

        if sides_with_no_matches == 2:
            # rotate to get corner edges at top and left
            for rot in [0, 1, 2, 3]:
                tile = tile.rotate(rot)
                edges = tile.edges()

                if edge_counts[edges.left] == 1 and edge_counts[edges.top] == 1:
                    corners.append(tile)
                    break

    return corners


Assembly = List[List[Optional[Tile]]] 

class Constraint(NamedTuple):
    """
    Says that the tile at location (i, j)
    must have sides that match the specified
    top / bottom / left / right
    """
    i: int
    j: int
    top: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None

    def satisfied_by(self, tile: Tile) -> bool:
        """
        Does the tile satisfy this constraint
        """
        if self.top and tile.top != self.top:
            return False
        if self.bottom and tile.bottom != self.bottom:
            return False
        if self.left and tile.left != self.left:
            return False
        if self.right and tile.right != self.right:
            return False
        return True
        
    @property
    def num_constraints(self) -> int:
        return (
            (self.top is not None) +
            (self.bottom is not None) + 
            (self.left is not None) + 
            (self.right is not None)
        )

def find_constraints(assembly: Assembly) -> Iterator[Constraint]:
    """
    Create constraints from a (partially filled in) Assembly.
    No constraints for already-filled-in tiles or unconstrained locations.
    """
    n = len(assembly)

    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            # already have a tile here
            if assembly[i][j]:
                continue
            constraints: Dict[str, str] = {}
            if i > 0 and (nbr := assembly[i-1][j]):
                constraints["top"] = nbr.bottom
            if i < n-1 and (nbr := assembly[i+1][j]):
                constraints["bottom"] = nbr.top 
            if j > 0 and (nbr := assembly[i][j-1]):
                constraints["left"] = nbr.right
            if j < n-1 and (nbr := assembly[i][j+1]):
                constraints["right"] = nbr.left

            if constraints:
                yield Constraint(i, j, **constraints)


def assemble_image(tiles: List[Tile]) -> Assembly:
    """
    Take the tiles and figure out how to stick them together
    """
    num_tiles = len(tiles)
    side_length = int(math.sqrt(num_tiles))
    corners = find_corners(tiles)

    # Pick a corner, any corner
    tile = corners[0]

    # Create an empty assembly
    assembly: Assembly = [[None for _ in range(side_length)] for _ in range(side_length)]

    # Put this corner tile in the top left
    assembly[0][0] = tile

    # Keep track of which tiles I've already placed
    placed: Dict[int, Tuple[int, int]] = {tile.tile_id: (0, 0)}

    # Repeat until all tiles have been placed
    while len(placed) < num_tiles:
        # Just care about unplaced tiles
        tiles = [t for t in tiles if t.tile_id not in placed]

        # Find the constraints based on all the tiles placed so far
        # and order them by descending # of constraints
        constraints = list(find_constraints(assembly))
        constraints.sort(key=lambda c: c.num_constraints, reverse=True)

        # Did I find a tile to add, so we can break out of inner loops
        found_one = False

        # Try constraints one at a time and see if we can find a tile
        # that satisfies them
        for constraint in constraints:
            for tile in tiles:
                # try all rotations for this tile, to see if any satisfies this constraint
                for rot in tile.all_rotations():
                    if constraint.satisfied_by(rot):
                        # place this rotation (which is a tile) at i, j
                        assembly[constraint.i][constraint.j] = rot 
                        placed[rot.tile_id] = (constraint.i, constraint.j)
                        found_one = True
                        break
                if found_one:
                    break
            if found_one:
                break

    return assembly

def glue(assembly: Assembly) -> Pixels:
    """
    Glue together the Tiles into a single grid of pixels,
    removing the edges of each tile
    """
    N = len(assembly)
    n = len(assembly[0][0].pixels)
    nout = (n - 2) * N
    glued = [['' for _ in range(nout)] for _ in range(nout)]
    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            cropped = [line[1:-1] for line in tile.pixels[1:-1]]
            for ii, crow in enumerate(cropped):
                for jj, pixel in enumerate(crow):
                    glued[i * (n-2) + ii][j * (n-2) + jj] = pixel

    return glued

SEA_MONSTER_RAW = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #"""   

# offsets for a sea monster
SEA_MONSTER = [
    (i, j) 
    for i, row in enumerate(SEA_MONSTER_RAW.split("\n"))
    for j, c in enumerate(row)
    if c == '#']

def find_sea_monsters(pixels: Pixels) -> Iterator[Tuple[int, int]]:
    """
    Return the indices of the top left corner of each sea monster
    """
    for i, row in enumerate(pixels):
        for j, c in enumerate(row):
            try:
                if all(pixels[i + di][j + dj] == '#' for di, dj in SEA_MONSTER):
                    yield (i, j)
            except IndexError:
                continue

def roughness(glued: Pixels) -> int:
    """
    Count the #s that are not part of a sea monster
    """
    # put the pixels in a Tile so we can use Tile methods
    tile = Tile(0, glued)

    # for each of the 8 rotation/flips, find the list of sea monster top lefts
    finds = [(t, list(find_sea_monsters(t.pixels))) for t in tile.all_rotations()]

    # only keep the ones that had sea monsters
    finds = [(t, sm) for t, sm in finds if sm]

    # hopefully only one of them had sea monsters
    assert len(finds) == 1

    # and that's our tile (and sea monster locations)
    t, sms = finds[0]

    # now we can computer all pixels that are showing a sea monster
    sea_monster_pixels = {(i + di, j + dj)
                          for i, j in sms
                          for di, dj in SEA_MONSTER}  

    # and count all the '#'s that are not sea monster pixels
    return sum(c == '#' and (i, j) not in sea_monster_pixels
               for i, row in enumerate(t.pixels)
               for j, c in enumerate(row))

#
# unit tests
#

RAW = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

TILES = make_tiles(RAW)
CORNERS = find_corners(TILES)
assert len(CORNERS) == 4
assert math.prod(tile.tile_id for tile in CORNERS) == 20899048083289

IMAGES = assemble_image(TILES)
GLUED = glue(IMAGES)
assert roughness(GLUED) == 273

#
# problem
#

with open('inputs/day20.txt') as f:
    raw = f.read()

tiles = make_tiles(raw)
corners = find_corners(tiles)
assert len(corners) == 4
print(math.prod(tile.tile_id for tile in corners))
images = assemble_image(tiles)
glued = glue(images)
print(roughness(glued))