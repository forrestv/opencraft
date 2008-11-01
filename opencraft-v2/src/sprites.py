"Use: sprites.sprite[name][frame][palette]"


import cdict

class Image(cdict.cdict):
    def __init__(self, name):
        self.name = name
        cdict.cdict.__init__(self, self.image_getter)
    def image_getter(frame):
        return Image(self)

class Sprite(cdict.cdict):
    def __init__(self, name):
        self.sprite = grp.load(frame)
        cdict.cdict.__init__(self, self.image_getter)
    def image_getter(frame):
        return Image(self)
        

def image_getter(n

def sprite_getter(name):
    sprite = grp.load(name)
    def image_getter(frame)
        image = sprite.get(frame)
        def subimage_getter(palette
            subimage = image.subsurface(image.get_rect())
            subimage.set_palette(palettes.palettes[palette])
            return subimage
        return cdict.cdict(subimage_getter)
    return cdict.cdict(image_getter)

sprites = cdict.cdict(Sprite)
