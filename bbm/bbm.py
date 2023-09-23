
import glob
# from ursina import *
import ursina as urs

import splashscreen
import loadingmenu
# import levelbuilder


titre="AA Games Bomberman"
# app = Ursina(title=titre)
if __name__ == '__main__':
    app = urs.Ursina(title=titre)
# app = Ursina(title=titre,development_mode=False)

input_mode = 'Clavier'
atk_key = 'x'
pause_key = 'p'
# application.paused = True
# SC_duration = 4
# SplashScreen(overlay_color=color.white,logo_texture='./textures/logo_aa.png',delay_time=SC_duration,audio='./audio/Tetris.mp3',audio_volume=1)
# invoke(setattr, application, 'paused', False, delay=1.2*SC_duration)


# explo_tex = glob.glob('./textures/explosion/*.png')
# barre = LoadingBar(texture_to_load=explo_tex)
# invoke(barre.start, delay=1.2*SC_duration)


pause_handler = urs.Entity(ignore_paused=True)
pause_text = urs.Text('PAUSED', origin=(0,0), scale=2, enabled=False)
def pause_handler_input(key):
    if input_mode == 'Manette':
        if key == urs.Keys.gamepad_start:
            urs.application.paused = not urs.application.paused
            pause_text.enabled = urs.application.paused
    else:
        if key == pause_key:
            urs.application.paused = not urs.application.paused
            pause_text.enabled = urs.application.paused
pause_handler.input = pause_handler_input


# print(camel_to_snake('CamelToSnake'))
# print(snake_to_camel('snake_to_camel'))
# test_var = 'test_str'
# printvar(test_var)
# info_var = 'info_str'
# print_info(info_var)
# warning_var = 'warning_str'
# print_warning(warning_var)


class Player(urs.Entity): 
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
        self.__anims = urs.SpriteSheetAnimation(
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
        
    def __animer(self, direction: urs.Vec2 = urs.Vec2(0,0)):
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
            urs.invoke(bombe.explode, delay=3)
            urs.invoke(urs.destroy, bombe, delay=3)
            urs.invoke(setattr, self, 'bombed', False, delay=3)
            # @after(3)
            # def unbomb():
            #     self.bombed = False
    
    def update(self):
        self.direction = urs.Vec2(urs.held_keys['d'] - urs.held_keys['a'], urs.held_keys['w'] - urs.held_keys['s']).normalized()
        # self.direction = Vec2(held_keys[Keys.gamepad_left_stick_x], held_keys[Keys.gamepad_left_stick_y]).normalized()
        if not self.stunned:
            hit_map = urs.raycast(self.position , self.direction, traverse_target=carte, distance=.5, debug=False)
            if not hit_map:
                self.position += self.direction * urs.time.dt * self.speed
            self.__animer(self.direction)
        if self.intersects(bombes).hit:
            self.stunned = True
        elif self.stunned:
            # invoke(setattr, self, 'stunned', False, delay=2)
            self.stunned = False
            print('aïe')
            


class Bomb(urs.Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        # self.model="quad"
        # self.texture="./textures/vide"
        self.rotation_x = -90
        self.scale=1
        self.__tex_folder = './textures/explosion/'
        self.longueur = 3

        self.__anims = urs.SpriteSheetAnimation(
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

        m1 = urs.Entity(scale=self.scale,model='quad',position=self.position,collider='box') ; m1.texture = self.__tex_folder + 'm11'
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m21', delay=wt1)
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m31', delay=wt2)
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m41', delay=wt3)
        urs.destroy(m1, delay=wt4)
        
        bombe_d = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = urs.raycast(bombe_d.position, (1,0), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = urs.raycast(bombe_d.position, (1,0), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_d) ; new_sprite.x += i+1
                new_sprite.texture = self.__tex_folder + 'd12'
                new_sprite.name = 'bout'
                urs.destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_d) ; new_sprite.x += i+1 ; new_sprite.texture = self.__tex_folder + 'd11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'd12'
                    new_sprite.name = 'bout'
        for sprite in bombe_d.children:
            if sprite.name != 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d21', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d31', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d41', delay=wt3)
                urs.destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d22', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d32', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'d42', delay=wt3)
                urs.destroy(sprite, delay=wt4)
        
        bombe_g = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = urs.raycast(bombe_g.position, (-1,0), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = urs.raycast(bombe_g.position, (-1,0), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_g) ; new_sprite.x -= i+1
                new_sprite.texture = self.__tex_folder + 'g12'
                new_sprite.name = 'bout'
                urs.destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_g) ; new_sprite.x -= i+1 ; new_sprite.texture = self.__tex_folder + 'g11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'g12'
                    new_sprite.name = 'bout'
        for sprite in bombe_g.children:
            if sprite.name != 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g21', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g31', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g41', delay=wt3)
                urs.destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g22', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g32', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'g42', delay=wt3)
                urs.destroy(sprite, delay=wt4)
        
        bombe_h = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = urs.raycast(bombe_h.position, (0,1), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = urs.raycast(bombe_h.position, (0,1), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_h) ; new_sprite.y += i+1
                new_sprite.texture = self.__tex_folder + 'h12'
                new_sprite.name = 'bout'
                urs.destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_h) ; new_sprite.y += i+1 ; new_sprite.texture = self.__tex_folder + 'h11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'h12'
                    new_sprite.name = 'bout'
        for sprite in bombe_h.children:
            if sprite.name != 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h21', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h31', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h41', delay=wt3)
                urs.destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h22', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h32', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'h42', delay=wt3)
                urs.destroy(sprite, delay=wt4)
        
        bombe_b = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        for i in range(self.longueur):
            hit_UnWall = urs.raycast(bombe_b.position, (0,-1), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = urs.raycast(bombe_b.position, (0,-1), traverse_target=murs_cassables, distance=i+1, debug=False)
            if hit_UnWall:
                break
            elif hit_BrWall:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_b) ; new_sprite.y -= i+1
                new_sprite.texture = self.__tex_folder + 'b12'
                new_sprite.name = 'bout'
                urs.destroy(hit_BrWall.entity)
                break
            else:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=bombe_b) ; new_sprite.y -= i+1 ; new_sprite.texture = self.__tex_folder + 'b11'
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder + 'b12'
                    new_sprite.name = 'bout'
        for sprite in bombe_b.children:
            if sprite.name != 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b21', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b31', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b41', delay=wt3)
                urs.destroy(sprite, delay=wt4)
            elif sprite.name == 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b22', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b32', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+'b42', delay=wt3)
                urs.destroy(sprite, delay=wt4)
        
        m1.parent = bombes
        bombe_d.parent = bombes
        bombe_g.parent = bombes
        bombe_h.parent = bombes
        bombe_b.parent = bombes

        for i in urs.scene.entities:
            if type(i) == urs.SpriteSheetAnimation:
                if 'flash' in i.animations:
                    i.disable()


joueurs = []
carte = urs.Entity(model='quad', texture='./textures/vide')
murs_incassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
murs_cassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
bombes = urs.Entity(model='quad', texture='./textures/vide')

class UnWall(urs.Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_incassables
        self.texture='./textures/UnWall'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

class BrWall(urs.Entity):
    def __init__(self, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_cassables
        self.texture='./textures/BrWall'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

def scan_texture(texture):
    scanned_tex = []
    
    for y in range(texture.height):
        scanned_tex.append([])
        for x in range(texture.width):
            scanned_tex[y].append(0)
            col = texture.get_pixel(x,y)
            # If it's black, it's solid, so we'll place a tile there.
            if col == urs.color.black:
                scanned_tex[y][x] = 1
            elif col == urs.color.brown:
                scanned_tex[y][x] = 2
            # si c'est vert, on y pace les joueurs chacun leurs tours
            elif col == urs.color.green:
                scanned_tex[y][x] = 3
    return scanned_tex

print(scan_texture(urs.load_texture('./textures/map2')))
map1 = scan_texture(urs.load_texture('./textures/map2'))

def place_level(texture_list:list, plr_list:list):
    # destroy every child of the level parent.
    [urs.destroy(c) for c in murs_incassables.children]
    
    width = len(texture_list[0])
    height = len(texture_list)
    urs.camera.position = (width/2, height/2)
    urs.camera.fov = width * 4
    
    plr_i = 0
    for y in range(height):
        for x in range(width):
            block = texture_list[y][x]
            # If it's black, it's solid, so we'll place a tile there.
            if block == 1:
                UnWall(position=(x,y))
            elif block == 2:
                BrWall(position=(x,y))
            # si c'est vert, on y pace les joueurs chacun leurs tours
            elif block == 3:
                try:
                    plr_list[plr_i].start_position = (x, y)
                    if plr_list[plr_i].position != plr_list[plr_i].start_position:
                        plr_list[plr_i].position = plr_list[plr_i].start_position
                    plr_i += 1
                except IndexError:
                    print('Not enough players to spwan a new one')


# lvl_b = levelbuilder.LevelBuilder(
#     map_image=load_texture('./textures/map1'),
#     plr_list=joueurs,
#     map_e=carte,
#     un_walls=murs_incassables,
#     br_walls=murs_cassables,
#     )
# lvl_b.make_level()

# la première fois qu'une bombe explose, elle provoque un lag-spike, on en fait donc exploser une à l'avance dehors de l'écran
bombe_lag=Bomb(position=(-100,-100)) ; urs.invoke(bombe_lag.explode, delay=0) ; urs.destroy(bombe_lag, delay=0)


# invoke(setattr, entity, 'var_name', value, delay=1.1)
# explo_tex = glob.glob('./textures/explosion/*.png')
# for i in explo_tex:
#     load_texture(i)
    # print(f'Loaded texture {i}', end='. ')
urs.EditorCamera()

player1 = Player(name='P1')
joueurs.append(player1)

# player2 = Player(name='P2')
# joueurs.append(player2)

place_level(map1, joueurs)

# EditorCamera()
urs.window.color = urs.color.light_gray
urs.window.borderless = False
urs.window.exit_button.visible = False

# app.run()
if __name__ == '__main__':
    app.run()

