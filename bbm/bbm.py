
import glob
# from ursina import *
import ursina as urs

import splashscreen
import loadingmenu
import bombe
import bbm.mapnlevel as mapnlevel


titre="Ultra-Bomberman"
# app = Ursina(title=titre)
if __name__ == '__main__':
    app = urs.Ursina(title=titre)
# app = Ursina(title=titre,development_mode=False)

input_mode = 'Clavier'
keys = {
    "atk_key" : 'x',
    "pause_key" : 'p',
}

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
        if key == keys['pause_key']:
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
        if key == keys['atk_key'] and not self.bombed:
            self.bombed = True
            # bombe = Bomb(x=round(self.x),y=round(self.y),longueur=3)
            bombe_p = bombe.Bomb(murs_incassables,murs_cassables,bombes,x=round(self.x),y=round(self.y),longueur=3)
            urs.invoke(bombe_p.explode, delay=3)
            urs.invoke(urs.destroy, bombe_p, delay=3)
            urs.invoke(setattr, self, 'bombed', False, delay=3)
            # @after(3)
            # def unbomb():
            #     self.bombed = False
    
    def update(self):
        # self.direction = urs.Vec2(urs.held_keys['d'] - urs.held_keys['a'], urs.held_keys['w'] - urs.held_keys['s']).normalized()
        self.direction = urs.Vec2(urs.held_keys[urs.Keys.gamepad_left_stick_x], urs.held_keys[urs.Keys.gamepad_left_stick_y]).normalized()
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


joueurs = []
carte = urs.Entity(model='quad', texture='./textures/vide')
murs_incassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
murs_cassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
bombes = urs.Entity(model='quad', texture='./textures/vide')

map1 = mapnlevel.scan_texture(urs.load_texture('./textures/map2'))

# la première fois qu'une bombe explose, elle provoque un lag-spike, on en fait donc exploser une à l'avance dehors de l'écran
bombe_lag=bombe.Bomb(murs_incassables,murs_cassables,bombes,position=(-100,-100)) ; urs.invoke(bombe_lag.explode, delay=0) ; urs.destroy(bombe_lag, delay=0)


urs.EditorCamera()

player1 = Player(name='P1')
joueurs.append(player1)

# player2 = Player(name='P2')
# joueurs.append(player2)

mapnlevel.place_level(map1, joueurs, murs_incassables, murs_cassables)

# EditorCamera()
urs.window.color = urs.color.light_gray
urs.window.borderless = False
urs.window.exit_button.visible = False

# app.run()
if __name__ == '__main__':
    app.run()

