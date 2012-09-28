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
        yield gx, gy, 0.0, None
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
        hv = hnext < vnext
        yield gx, gy, t, hv
        if hv:
            t = hnext
            hnext += dtdx
            gx += xstep
        else:
            t = vnext
            vnext += dtdy
            gy += ystep

    return




def point_near_line(x1, y1, x2, y2, px, py):
    ''' Return nearest point on a line segment and distance to that point '''
    # Movement vector  v1 -> v2
    dx, dy = x2-x1, y2-y1
    # Offset of point from movement start position: v1 -> p
    ptx, pty = px-x1, py-y1
    # Length of movement
    slen = (dx**2 + dy**2) ** 0.5
    # Normalized (length 1) movement vector
    ndx, ndy = dx/slen, dy/slen
    # Lengths of the projection of ptx/y onto dx/y
    projlen = ptx * ndx + pty * ndy
    # Closest point on line
    if projlen <= 0:
        cpx, cpy = x1, y1
    elif projlen >= slen:
        cpx, cpy = x2, y2
    else:
        cpx, cpy = ndx * projlen + x1, ndy * projlen + y1
    # Distance to line:
    dist = ((px-cpx)**2 + (py-cpy)**2) ** 0.5
    return cpx, cpy, dist

