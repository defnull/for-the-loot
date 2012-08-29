import pyglet
from pyglet.gl import *

class ZSpriteGroup(pyglet.graphics.Group):
    '''Shared sprite rendering group.

    The group is automatically coalesced with other sprite groups sharing the
    same parent group, texture and blend parameters.
    '''
    def __init__(self, texture, blend_src, blend_dest, parent=None):
        '''Create a sprite group.

        The group is created internally within `Sprite`; applications usually
        do not need to explicitly create it.

        :Parameters:
            `texture` : `Texture`
                The (top-level) texture containing the sprite image.
            `blend_src` : int
                OpenGL blend source mode; for example,
                ``GL_SRC_ALPHA``.
            `blend_dest` : int
                OpenGL blend destination mode; for example,
                ``GL_ONE_MINUS_SRC_ALPHA``.
            `parent` : `Group`
                Optional parent group.

        '''
        super(ZSpriteGroup, self).__init__(parent)
        self.texture = texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glAlphaFunc(GL_GREATER, 0.5);
        glEnable(GL_ALPHA_TEST);
        glDepthFunc(GL_LEQUAL)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.texture)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))


class ZSprite(object):

    def __init__(self, img, x, y, batch):
        self.img = img
        self.texture = self.img.get_texture()
        self.x = x
        self.y = y
        self.batch = batch
        self.vertex_list = None
        self.rgba = [255,255,255,255]
        self._make_vertex_list()

    def _make_vertex_list(self):
        if self.vertex_list:
            self.vertex_list.delete()
        self.group = ZSpriteGroup(self.texture,
                        blend_src=pyglet.gl.GL_SRC_ALPHA,
                        blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.vertex_list = self.batch.add(4, GL_QUADS, self.group,
            'v3i', 'c4B', 't3f',)
        self.vertex_list.tex_coords[:] = self.texture.tex_coords
        self._update_position()
        self._update_color()

    def _update_position(self):
        img = self.texture
        x1 = int(self.x - img.anchor_x)
        y1 = int(self.y - img.anchor_y)
        x2 = x1 + img.width
        y2 = y1 + img.height
        self.vertex_list.vertices[:] = [
            x1, y1, -y1,
            x2, y1, -y1,
            x2, y2, -y1,
            x1, y2, -y1,
        ]

    def _update_color(self):
        self.vertex_list.colors[:] = self.rgba * 4

    def __del__(self):
        try:
            if self.vertex_list is not None:
                self.vertex_list.delete()
        except:
            pass
