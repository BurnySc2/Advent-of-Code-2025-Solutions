import grilops
from grilops.geometry import Point, RectangularLattice, Vector
from grilops.shapes import Shape, ShapeConstrainer

GRID = [
    "OOOOO",
    "OOOOO",
    "OOOOO",
    "OOOOO",
    "OOOOO",
]


def main():
    """Shape solver example."""
    points = []
    for y, row in enumerate(GRID):
        for x, c in enumerate(row):
            if c == "O":
                points.append(Point(y, x))
    lattice = RectangularLattice(points)

    shapes = [
        Shape([Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(3, 0)]),  # I
        Shape([Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(3, 0)]),  # I
        Shape([Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(2, 1)]),  # L
        Shape([Vector(0, 1), Vector(0, 2), Vector(1, 0), Vector(1, 1)]),  # S
    ]

    sym = grilops.SymbolSet([("B", chr(0x2588) * 2), ("W", "  ")])
    sg = grilops.SymbolGrid(lattice, sym)
    sc = ShapeConstrainer(
        lattice,
        shapes,
        sg.solver,
        complete=False,
        allow_rotations=True,
        allow_reflections=True,
        allow_copies=False,
    )
    # for p in points:
    #     sg.solver.add(sg.cell_is(p, sym.W) == (sc.shape_type_grid[p] == -1))
    if sg.solve():
        sg.print()
        print()
        sc.print_shape_types()
        print()
        if sg.is_unique():
            print("Unique solution")
        else:
            print("Alternate solution")
            sg.print()
    else:
        print("No solution")


if __name__ == "__main__":
    main()
