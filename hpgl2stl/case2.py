from case1 import simple_triangulate

"""
WORK IN PROGRESS
"""


def complex_triangulate(polygon, hints=None):
    """
    >>> from case1 import Vertex
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
    >>> mesh = complex_triangulate(polygon,
    ...                            hints=[polygon[0][0], polygon[1][0]])
    >>> len(mesh)
    14
    >>> mesh
    [(A, N, M), (L, K, K), (L, K, A), (L, A, B), (D, E, F), (I, G, H)]
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
    [(A, N, M), (L, K, K), (L, K, A), (L, A, B), (D, E, F), (D, F, G), \
        (I, J, A), (I, A, M), (I, M, M), (I, M, L), (I, L, B), \
        (I, B, D), (I, D, G), (I, G, H)]
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
        p0 = polygon[0][:m] + p1a + p1b + polygon[0][m:]
    return simple_triangulate(p0)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
