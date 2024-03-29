
from ursina import *
from direct.stdpy import thread
from ursina.prefabs.health_bar import HealthBar


if __name__ == '__main__':
    app = Ursina()


class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(parent=self, model=Circle(24, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=2, texture='circle')
        self.point2 = Entity(parent=self, model=Circle(12, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=1, texture='circle')

        self.scale = .025
        self.text_entity = Text(world_parent=self, text='loading...', origin=(0,1.5), color=color.light_gray)
        self.y = -.25

        self.bg = Entity(parent=self, model='quad', scale_x=camera.aspect_ratio, color=color.black, z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3


class LoadingBar():
    def __init__(self, texture_to_load):
        super().__init__()
        
        self.texs = texture_to_load
        self.loading_screen = LoadingWheel(enabled=False)
    
    def load_textures(self):
        bar = HealthBar(max_value=len(self.texs), value=0, position=(-.5,-.35,-2), scale_x=1, animation_duration=0, world_parent=self.loading_screen, bar_color=color.gray)
        for i, t in enumerate(self.texs):
            load_texture(t)
            # print(t)
            bar.value = i+1
        print('loaded textures')
        self.loading_screen.enabled = False
    
    def start(self):
        self.loading_screen.enabled = True

        try:
            thread.start_new_thread(function=self.load_textures, args='')
        except Exception as e:
            print('error starting thread', e)

    
if __name__ == '__main__':
    app.run()