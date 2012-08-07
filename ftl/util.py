from pyglet.gl import *

def pixelate( texture ):
    glBindTexture( texture.target, texture.id )
    glTexParameteri( texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glBindTexture( texture.target, 0 )
