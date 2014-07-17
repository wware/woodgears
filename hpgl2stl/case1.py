# Write code to handle the convex polygon with no holes, and write tests for it.

import sys
from math import pi, sin, cos
from pprint import pprint

class Vertex:

    def __init__(self, x, y, extra=None):
        if extra is not None:
            self.name, self.x, self.y = x, y, extra
        else:
            self.x, self.y = x, y

    def __repr__(self):
        if hasattr(self, 'name'):
            return self.name
        return "<{0} {1}>".format(self.x, self.y)

    def __eq__(self, other):
        # allow for floating-point wiggliness
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) < 1.0e-10

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y)

    def cross(self, other):
        # the z component of a 3D cross product
        return self.x * other.y - other.x * self.y


def interior_to(edges):
    """
    >>> edges = [
    ...   (Vertex(0, 0), Vertex(1, 0)),
    ...   (Vertex(1, 0), Vertex(1, 1)),
    ...   (Vertex(1, 1), Vertex(0, 1)),
    ...   (Vertex(0, 1), Vertex(0, 0))
    ... ]
    >>> f = interior_to(edges)
    >>> f(Vertex(0.5, 0.5))
    True
    >>> f(Vertex(-0.5, 0.5))
    False
    >>> f(Vertex(1.5, 0.5))
    False
    >>> edges = [
    ...   (Vertex(0, 0), Vertex(1, 0)),
    ...   (Vertex(1, 0), Vertex(1, 1)),
    ...   (Vertex(1, 1), Vertex(0, 1)),
    ...   (Vertex(0, 1), Vertex(0, 0)),
    ...   (Vertex(0.2, 0.2), Vertex(0.8, 0.2)),
    ...   (Vertex(0.8, 0.2), Vertex(0.8, 0.8)),
    ...   (Vertex(0.8, 0.8), Vertex(0.2, 0.8)),
    ...   (Vertex(0.2, 0.8), Vertex(0.2, 0.2))
    ... ]
    >>> f = interior_to(edges)
    >>> f(Vertex(0.5, 0.5))
    False
    >>> f(Vertex(-0.5, 0.5))
    False
    >>> f(Vertex(1.5, 0.5))
    False
    >>> f(Vertex(0.1, 0.5))
    True
    >>> f(Vertex(0.9, 0.5))
    True
    >>> f(Vertex(0.5, 0.9))
    True
    >>> f(Vertex(0.1, 0.9))
    True
    >>> f(Vertex(0.9, 0.9))
    True
    """
    edges = edges[:]
    def func(pt, edges=edges):
        intersections = 0
        for edge in edges:
            if abs(edge[0].y - edge[1].y) < 1.0e-10:
                continue
            miny, maxy = min(edge[0].y, edge[1].y), max(edge[0].y, edge[1].y)
            if miny <= pt.y <= maxy:
                # compute the x on the edge for this y value
                t = 1. * (pt.y - edge[0].y) / (edge[1].y - edge[0].y)
                xvalue = t * edge[1].x + (1 - t) * edge[0].x
                if xvalue >= pt.x:
                    intersections += 1
        return (intersections % 2) == 1
    return func


def single_collision(edge1, edge2, h=1.0e-10):
    """
    >>> def reverse(edge):
    ...     return (edge[1], edge[0])
    >>> edge1 = Vertex(0, 0), Vertex(1, 1)
    >>> edge2 = Vertex(1, 0), Vertex(0, 1)
    >>> single_collision(edge1, edge2)
    True
    >>> single_collision(edge2, edge1)
    True
    >>> single_collision(reverse(edge1), reverse(edge2))
    True
    >>> single_collision(reverse(edge2), reverse(edge1))
    True
    >>> edge1 = Vertex(0, 0), Vertex(0, 1)
    >>> edge2 = Vertex(1, 0), Vertex(1, 1)
    >>> single_collision(edge1, edge2)
    False
    >>> single_collision(edge2, edge1)
    False
    >>> single_collision(reverse(edge1), reverse(edge2))
    False
    >>> single_collision(reverse(edge2), reverse(edge1))
    False
    >>> edge1 = Vertex(0, 0), Vertex(0, 1)
    >>> edge2 = Vertex(0, 0), Vertex(1, 1)
    >>> single_collision(edge1, edge2)
    False
    >>> single_collision(edge2, edge1)
    False
    >>> single_collision(reverse(edge1), reverse(edge2))
    False
    >>> single_collision(reverse(edge2), reverse(edge1))
    False
    >>> edge1 = Vertex(0, 0), Vertex(2, 0)
    >>> edge2 = Vertex(1, 1), Vertex(1, 2)
    >>> single_collision(edge1, edge2)
    False
    >>> single_collision(edge2, edge1)
    False
    >>> single_collision(reverse(edge1), reverse(edge2))
    False
    >>> single_collision(reverse(edge2), reverse(edge1))
    False
    """
    a, b = edge1
    c, d = edge2
    t, u, v, w = c - a, b - c, d - b, a - d
    # compute product of cross products
    xp0, xp1, xp2, xp3 = t.cross(u), u.cross(v), v.cross(w), w.cross(t)
    return ((xp0 > h and xp1 > h and xp2 > h and xp3 > h) or
        (xp0 < -h and xp1 < -h and xp2 < -h and xp3 < -h))

def collision_detector(edges):
    def func(edge, edges=edges):
        return filter(lambda e, edge=edge: single_collision(e, edge), edges)
    return func

# A simple polygon (or path) is a list of vertices. It is assumed to be closed,
# so the first and last won't be the same point.

def simple_triangulate(polygon, mesh=None):
    """
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
    ... ]
    >>> mesh = simple_triangulate(polygon)
    >>> len(mesh)
    8
    >>> mesh
    [(B, C, D), (D, E, F), (D, F, G), (D, G, H), (D, H, I), (I, J, A), (I, A, B), (I, B, D)]
    >>> polygon = [
    ...   Vertex('A', 1, 0),
    ...   Vertex('B', 2, 0),
    ...   Vertex('C', 3, 1),
    ...   Vertex('D', 3, 2),
    ...   Vertex('E', 1.5, 4),
    ...   Vertex('F', 0, 2),
    ...   Vertex('G', 1, 2),
    ...   Vertex('H', 1.5, 3),
    ...   Vertex('I', 2, 2),
    ...   Vertex('J', 2, 1),
    ...   Vertex('K', 1.5, 0.5),
    ...   Vertex('L', 1, 1),
    ...   Vertex('M', 0, 1),
    ... ]
    >>> mesh = simple_triangulate(polygon)
    >>> len(mesh)
    11
    >>> mesh
    [(A, B, C), (C, D, E), (E, F, G), (E, G, H), (E, H, I), (K, L, M), (K, M, A), (K, A, C), (C, E, I), (C, I, J), (C, J, K)]
    """
    edges = [(u, v) for u, v in zip(polygon, polygon[1:] + polygon[:1])]
    edge_collisions = collision_detector(edges)
    interior = interior_to(edges)
    if mesh is None:
        mesh = []
    """
    The strategy is to find three consecutive points along the path that can be used
    to form a triangle that is interior to the shape, so its third side doesn't
    collide with any other edges and doesn't have any vertices in it.
    """

    def centroid(polygon):
        x = y = 0.
        n = len(polygon)
        for pt in polygon:
            x += pt.x
            y += pt.y
        return Vertex(x / n, y / n)

    def is_good(triangle, interior=interior,
                centroid=centroid, edge_collisions=edge_collisions):
        if not interior(centroid(triangle)):
            return False
        # TODO make sure no vertices are internal to this triangle, besides those
        # that are vertices of the triangle itself
        return not edge_collisions((triangle[0], triangle[2]))

    countdown = len(polygon) + 2
    while True:
        if len(polygon) == 3:
            mesh.append(tuple(polygon))
            return mesh
        triangle = tuple(polygon[:3])
        if not is_good(triangle):
            print >> sys.stderr, triangle, 'bad'
            countdown -= 1
            assert countdown > 0, polygon
            polygon = polygon[1:] + polygon[:1]
        else:
            print >> sys.stderr, triangle, 'good'
            mesh.append(triangle)
            polygon = polygon[:1] + polygon[2:]
            countdown = len(polygon) + 2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
