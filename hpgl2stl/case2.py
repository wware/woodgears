from case1 import *

"""
A polygon with a hole is made up of multiple non-overlapping closed paths, one
surrounding the others. Exactly one path is the outermost path, the periphery of
the object, and we can identify it because any ray originating anywhere inside it
(whether in a hole or in the interior) that goes out to infinity must cross the
outermost path last.

Now we take any other path and try to create a line segment that connects that
inner path with the outermost path without crossing any of the other paths. If
we succeed at that, we can treat say that topologically we have eliminated one
hole, as the inner path has now become part of the periphery - this will require
rewriting the orders of the paths, but is doable.

We keep chipping away, removing holes one by one, until no holes are left, and
then we can simply apply case 2.

There won't be a lot of these line segments (only one per hole) and they could
be set up manually. There would need to be some kind of UI to make that easy.
"""

def complex_triangulate(polygon, hints=None):
    """
    >>> polygon = [
    ...   [
    ...     Vertex('A', 0, 0),
    ...     Vertex('B', 1, 1),
    ...     Vertex('C', 2, 0),
    ...     Vertex('D', 3, 1),
    ...     Vertex('E', 4, 0),
    ...     Vertex('F', 4, 3),
    ...     Vertex('G', 3, 2),
    ...     Vertex('H', 2, 3),
    ...     Vertex('I', 1, 2),
    ...     Vertex('J', 0, 3),
    ...   ],
    ...   [
    ...     Vertex('K', 0.5, 1.5),
    ...     Vertex('L', 2, 1),
    ...     Vertex('M', 3.5, 1.5),
    ...     Vertex('N', 2, 2),
    ...   ]
    ... ]
    >>> # mesh = complex_triangulate(polygon, hints=[polygon[0][0], polygon[1][0]])
    >>> polygon = [
    ...   Vertex('A', 0, 0),
    ...   Vertex('B', 1, 1),
    ...   Vertex('C', 2, 0),
    ...   Vertex('D', 3, 1),
    ...   Vertex('E', 4, 0),
    ...   Vertex('F', 4, 3),
    ...   Vertex('G', 3, 2),
    ...   Vertex('H', 2, 3),
    ...   Vertex('I', 1, 2),
    ...   Vertex('J', 0, 3),
    ...   Vertex('A', 0, 0),
    ...   Vertex('K', 0.5, 1.5),
    ...   Vertex('N', 2, 2),
    ...   Vertex('M', 3.5, 1.5),
    ...   Vertex('L', 2, 1),
    ...   Vertex('K', 0.5, 1.5),
    ... ]
    >>> mesh = simple_triangulate(polygon)
    >>> len(mesh)
    14
    >>> mesh
    [(A, N, M), (L, K, K), (L, K, A), (L, A, B), (D, E, F), (D, F, G), (I, J, A), (I, A, M), (I, M, M), (I, M, L), (I, L, B), (I, B, D), (I, D, G), (I, G, H)]
    """
    if not hints:
        raise Exception("too dumb to work without hints")
    m = polygon[0].index(hints[0])
    n = polygon[1].index(hints[1])
    p1a = polygon[1][:n+1]
    p1a.reverse()
    p1b = polygon[1][n:]
    p1b.reverse()
    if m == 0:
        p0 = polygon[0] + p1a + p1b
    else:
        p0 = polygon[0][:m] + p1 + polygon[0][m:]
    #assert False, p0
    return simple_triangulate(p0)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
