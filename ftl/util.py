import functools
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

class cached_property(object):
    ''' A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property. '''

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class lazy_attribute(object):
    ''' A property that caches itself to the class object. '''
    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value
