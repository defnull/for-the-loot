from math import floor

def grid_walk(x1, y1, x2, y2):
    ''' Compute the grid fields traversed by a line. Yield (gx, gy, t) tuples.
        gx and gy are the grid field indices (int) and t is the fraction of the
        line at which the grid field is entered. The first grid field (t=0) is
        always returned.'''

    gx = int(floor(x1))
    gy = int(floor(y1))
    t = 0.0

    if gx == floor(x2) and gy == floor(y2):
        yield gx, gy, 0.0
        return

    # Travel distances
    dx = abs(-x1+x2)
    dy = abs(-y1+y2)

    dtdx = 1.0 / dx if dx else 0
    dtdy = 1.0 / dy if dy else 0

    if x1 == x2:
        xstep = 0
        hnext = 10000000
    elif x2 > x1:
        xstep = 1
        hnext = dtdx * (1.0 - (x1%1))
    else:
        xstep = -1
        hnext = dtdx * ((x1%1))

    if y1 == y2:
        ystep = 0
        vnext = 10000000
    elif y2 > y1:
        ystep = 1
        vnext = dtdy * (1.0 - (y1%1))
    else:
        ystep = -1
        vnext = dtdy * ((y1%1))

    while t < 1:
        yield gx, gy, t
        if hnext < vnext:
            t = hnext
            hnext += dtdx
            gx += xstep
        else:
            t = vnext
            vnext += dtdy
            gy += ystep

    return

