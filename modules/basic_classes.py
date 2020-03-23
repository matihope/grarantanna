
class GameInstance:
    _reg = []

    def __init__(self):
        self._reg.append(self)
        self.parent = None

    def add_parent(self, parent):
        self.parent = parent


class DrawableObj(GameInstance):
    _reg = []

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._reg.append(self)

        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)

        self.visible = True
        self.x = x
        self.y = y
        self.sprites = kwargs.get('sprites', [])
        self.sprite_index = kwargs.get('sprite_index', 0)
        self.animation_speed = kwargs.get('animation_speed', 0)

    def draw(self, surface):
        if self.visible and len(self.sprites) > 0:
            index = min(int(self.sprite_index), len(self.sprites)-1)
            surface.blit(self.sprites[index], (self.x, self.y))
            self.sprite_index += self.animation_speed
            self.sprite_index %= len(self.sprites)


class UpdatableObj(DrawableObj):
    _reg = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reg.append(self)
        self.active = True

    def update(self, keys):
        if not self.active:
            return
