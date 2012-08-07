from pyglet.gl import *

def pixelate( texture ):
    glBindTexture( texture.target, texture.id )
    glTexParameteri( texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glBindTexture( texture.target, 0 )
    
def normvec(v, n=1.0):
    f = float(n) / ((v[0]**2+v[1]**2)**.5) if v[0] or v[1] else 0
    return v[0]*f, v[1]*f
    
def center_image(img, dx=.5, dy=.5):
    img.anchor_x = img.width*dx
    img.anchor_y = img.height*dy
