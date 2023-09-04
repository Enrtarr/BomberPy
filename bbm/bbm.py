
import glob
from ursina import *

import splashscreen
import loadingmenu


titre="AA Games Bomberman"
# app = Ursina(title=titre)
if __name__ == '__main__':
    app = Ursina(title=titre)
# app = Ursina(title=titre,development_mode=False)

input_mode = ''
# application.paused = True
# SC_duration = 4
# SplashScreen(overlay_color=color.white,logo_texture='./textures/logo_aa.png',delay_time=SC_duration,audio='./audio/Tetris.mp3',audio_volume=1)
# invoke(setattr, application, 'paused', False, delay=1.2*SC_duration)


# explo_tex = glob.glob('./textures/explosion/*.png')
# barre = LoadingBar(texture_to_load=explo_tex)
# invoke(barre.start, delay=1.2*SC_duration)


pause_handler = Entity(ignore_paused=True)
pause_text = Text('PAUSED', origin=(0,0), scale=2, enabled=False)
def pause_handler_input(key):
    if key == (Keys.gamepad_start or Keys.escape):
    # if key == Keys.escape:
        application.paused = not application.paused
        pause_text.enabled = application.paused
pause_handler.input = pause_handler_input


# print(camel_to_snake('CamelToSnake'))
# print(snake_to_camel('snake_to_camel'))
# test_var = 'test_str'
# printvar(test_var)
# info_var = 'info_str'
# print_info(info_var)
# warning_var = 'warning_str'
# print_warning(warning_var)


class Player(Entity): 
    def __init__(self, **kwargs): 
        super().__init__() 
        # self.model = 'quad'
        self.scale_y = 2 
        self.rotation_x = -90
        # self.texture = '/textures/vide'
        self.always_on_top = True
        self.collider = 'box'
        self.speed = 2
        self.stunned = False
        self.bombed = False
        self.__anims = SpriteSheetAnimation(
            texture='/textures/new_bbm_sheet3.png',
            tileset_size=(18,5),
            fps=4,
            model='plane',
            animations={
                'idle': ((7,2), (8,2)),
                'walk_right': ((9,4),(10,4)),
                'walk_left': ((3,4),(4,4)),
                'walk_down': ((6,4),(7,4)),
                'walk_up': ((0,4),(1,4)),
                'interact': ((0,5),(0,5))
            }
        )
        self.__anims.parent = self
        self.__anims.play_animation('idle')

        for key, value in kwargs.items(): 
            setattr(self, key, value) 
        
    def __animer(self, direction: Vec2 = Vec2(0,0)):
        if direction.x > 0:
            if self.__anims.animations['walk_right'].paused:
                self.__anims.play_animation('walk_right')
        elif direction.x < 0:
            if self.__anims.animations['walk_left'].paused:
                self.__anims.play_animation('walk_left')
        elif direction.y > 0:
            if self.__anims.animations['walk_up'].paused:
                self.__anims.play_animation('walk_up')
        elif direction.y < 0:
            if self.__anims.animations['walk_down'].paused:
                self.__anims.play_animation('walk_down')
        elif direction.x == 0 and direction.y == 0:
            if self.__anims.animations['idle'].paused:
                self.__anims.play_animation('idle')

    def input(self, key):
        # if key == Keys.gamepad_x:
        if key == 'x' and not self.bombed:
            self.bombed = True
            bombe=Bomb(x=round(self.x),y=round(self.y),longueur=3)
            invoke(bombe.explode, delay=3)
            invoke(destroy, bombe, delay=3)
            invoke(setattr, self, 'bombed', False, delay=3)
            # @after(3)
            # def unbomb():
            #     self.bombed = False
    
    def update(self):
        self.direction = Vec2(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']).normalized()
        # self.direction = Vec2(held_keys[Keys.gamepad_left_stick_x], held_keys[Keys.gamepad_left_stick_y]).normalized()
        if not self.stunned:
            hit_map = raycast(self.position , self.direction, traverse_target=carte, distance=.5, debug=False)
            if not hit_map:
                self.position += self.direction * time.dt * self.speed
            self.__animer(self.direction)
        if self.intersects(bombes).hit:
            self.stunned = True
        elif self.stunned:
            # invoke(setattr, self, 'stunned', False, delay=2)
            self.stunned = False
            print('aïe')
            


class Bomb(Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        # self.model="quad"
        # self.texture="./textures/vide"
        self.rotation_x = -90
        self.scale=1
        self.__tex_folder = './textures/explosion/'
        self.longueur = 3

        self.__anims = SpriteSheetAnimation(
            texture='./textures/bomb_flash.png',
            tileset_size=(6,1),
            fps=6,
            model='plane',
            animations={
                'flash': ((0,0), (5,0)),
            }
        )
        self.__anims.parent = self
        self.__anims.play_animation('flash')
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)
    
    def explode(self):
        duration = .3
        wt1 = duration/3
        wt2 = 2 * duration/3
        wt3 = duration
        wt4 = duration + duration/3

        m1 = Entity(scale=self.scale,model='quad',position=self.position,collider='box') ; m1.texture = self.__tex_folder + 'm11'
        invoke(setattr, m1, 'texture', self.__tex_folder+'m21', delay=wt1)
        invoke(setattr, m1, 'texture', self.__tex_folder+'m31', delay=wt2)
        invoke(setattr, m1, 'texture', self.__tex_folder+'m41', delay=wt3)
        destroy(m1, delay=wt4)
        
        bombe_d = Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = raycast(bombe_d.position, (1,0), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = raycast(bombe_d.position, (1,0), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_d) ; new_sprite.x += i+1
                new_sprite.texture = self.__tex_folder + 'd12'
                new_sprite.name = 'bout'
                destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_d) ; new_sprite.x += i+1 ; new_sprite.texture = self.__tex_folder + 'd11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'd12'
                    new_sprite.name = 'bout'
        for sprite in bombe_d.children:
            if sprite.name != 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d21', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d31', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d41', delay=wt3)
                destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d22', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d32', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'d42', delay=wt3)
                destroy(sprite, delay=wt4)
        
        bombe_g = Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = raycast(bombe_g.position, (-1,0), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = raycast(bombe_g.position, (-1,0), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_g) ; new_sprite.x -= i+1
                new_sprite.texture = self.__tex_folder + 'g12'
                new_sprite.name = 'bout'
                destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_g) ; new_sprite.x -= i+1 ; new_sprite.texture = self.__tex_folder + 'g11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'g12'
                    new_sprite.name = 'bout'
        for sprite in bombe_g.children:
            if sprite.name != 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g21', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g31', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g41', delay=wt3)
                destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g22', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g32', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'g42', delay=wt3)
                destroy(sprite, delay=wt4)
        
        bombe_h = Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = raycast(bombe_h.position, (0,1), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = raycast(bombe_h.position, (0,1), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_h) ; new_sprite.y += i+1
                new_sprite.texture = self.__tex_folder + 'h12'
                new_sprite.name = 'bout'
                destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_h) ; new_sprite.y += i+1 ; new_sprite.texture = self.__tex_folder + 'h11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'h12'
                    new_sprite.name = 'bout'
        for sprite in bombe_h.children:
            if sprite.name != 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h21', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h31', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h41', delay=wt3)
                destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h22', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h32', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'h42', delay=wt3)
                destroy(sprite, delay=wt4)
        
        bombe_b = Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = raycast(bombe_b.position, (0,-1), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = raycast(bombe_b.position, (0,-1), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_b) ; new_sprite.y -= i+1
                new_sprite.texture = self.__tex_folder + 'b12'
                new_sprite.name = 'bout'
                destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = Entity(scale=self.scale,model='quad',collider='box',parent=bombe_b) ; new_sprite.y -= i+1 ; new_sprite.texture = self.__tex_folder + 'b11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'b12'
                    new_sprite.name = 'bout'
        for sprite in bombe_b.children:
            if sprite.name != 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b21', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b31', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b41', delay=wt3)
                destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b22', delay=wt1)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b32', delay=wt2)
                invoke(setattr, sprite, 'texture', self.__tex_folder+'b42', delay=wt3)
                destroy(sprite, delay=wt4)
        
        m1.parent = bombes
        bombe_d.parent = bombes
        bombe_g.parent = bombes
        bombe_h.parent = bombes
        bombe_b.parent = bombes

        for i in scene.entities:
            if type(i) == SpriteSheetAnimation:
                if 'flash' in i.animations:
                    i.disable()


joueurs = []
carte = Entity(model='quad', texture='./textures/vide')
murs_incassables = Entity(model='quad', texture='./textures/vide', parent=carte)
murs_cassables = Entity(model='quad', texture='./textures/vide', parent=carte)
bombes = Entity(model='quad', texture='./textures/vide')

class UnWall(Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_incassables
        self.texture='./textures/UnWall'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

class BrWall(Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_cassables
        self.texture='./textures/BrWall'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

def make_level(texture, plr_list:list):
    # destroy every child of the level parent.
    [destroy(c) for c in murs_incassables.children]
    
    camera.position = (texture.width/2, texture.height/2)
    camera.fov = texture.width * 4

    for y in range(texture.height):
        for x in range(texture.width):
            col = texture.get_pixel(x,y)
            # If it's black, it's solid, so we'll place a tile there.
            if col == color.black:
                UnWall(position=(x,y))
            elif col == color.brown:
                BrWall(position=(x,y))
            # elif col == color.green:
            #     plr_list[0].start_position = (x, y)
            #     plr_list[0].position = plr_list[0].start_position


make_level(load_texture('./textures/map1'), joueurs)

# la première fois qu'une bombe explose, elle provoque un lag-spike, on en fait donc exploser une à l'avance dehors de l'écran
bombe_lag=Bomb(position=(-100,-100)) ; invoke(bombe_lag.explode, delay=0) ; destroy(bombe_lag, delay=0)


# invoke(setattr, entity, 'var_name', value, delay=1.1)
# explo_tex = glob.glob('./textures/explosion/*.png')
# for i in explo_tex:
#     load_texture(i)
    # print(f'Loaded texture {i}', end='. ')
EditorCamera()

player1 = Player(x=-1)
joueurs.append(player1)

# EditorCamera()
window.color = color.light_gray
window.borderless = False
window.exit_button.visible = False

# app.run()
if __name__ == '__main__':
    app.run()

