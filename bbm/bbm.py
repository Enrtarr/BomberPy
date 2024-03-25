
import glob
# from ursina import *
import ursina as urs

import splashscreen
import loadingmenu
import bombe
import mapnlevel as mapnlevel
import pwup
import ball

print("""
      ⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣷⣤⡀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀ 
⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀ 
⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿
⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⠃⠀⠀ 
⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀ 
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀ 
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀ 
⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀ 
⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀ 
⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⢠⣿⣿⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⡿⠏⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")

titre="Ultra-Bomberman: The Movie: The Game MMXXIV: Remastered, Deluxe Definitive Gold Edition by AA Games"
# app = Ursina(title=titre)
if __name__ == '__main__':
    app = urs.Ursina(title=titre)
# app = Ursina(title=titre,development_mode=False)

gm = 'foot'
gm_d = {
    'br': {
        'map': {
            'texture': 'map3',
            'bonus': True,
            'sky': 'grass',
        },
        'player': {
            'speed': 2,
            'bomb_size': 3,
            'max_bomb': 1,
            'max_lives': 3,
            'stun_time': 2,
        },
    },
    'foot': {
        'map': {
            'texture': 'map7',
            'bonus': False,
            'sky': 'grass',
        },
        'player': {
            'speed': 3,
            'bomb_size': 2,
            'max_bomb': 3,
            'max_lives': 2,
            'stun_time': 1,
        },
    },
}
input_mode = 'Clavier'


class Player(urs.Entity): 
    def __init__(self, **kwargs):
        """Initialisation du joueur et des attributs
            - scale_y : la déformation verticale du joueur
            - rotation_x : permet de faire en sorte que le joueur fasse face à la caméra
            - always_on_top : permet de faire en sorte que le joueur soit toujours au premier plan
            - collider : la hitbox du joueur
            - speed : la vitesse de déplacement du joueur (multiplicatif)
            - stunned : contient si le joueur est étourdi ou non
            - bombed : contient si le joueur a déjà une bombe placée
            - __anims : les animations du joueur"""
        super().__init__() 
        # self.model = 'quad'
        self.scale_y = 2
        self.rotation_x = -90
        # self.texture = '/textures/vide'
        self.always_on_top = True
        self.collider = 'box'
        
        self.controls = {
            'up': 'w',
            'down': 's',
            'left': 'a',
            'right': 'd',
            'atk': 'space',
        }
        
        self.speed = gm_d[gm]['player']['speed']
        self.bomb_size = gm_d[gm]['player']['bomb_size']
        self.max_bomb = gm_d[gm]['player']['max_bomb']
        self.bombed = 1
        
        self.max_lives = gm_d[gm]['player']['max_lives']
        self.lives = self.max_lives
        self.respawn_time = 1.7
        
        self.start_position = self.position
        self.stunned = False
        self.can_move = True
        
        self.__anims = urs.SpriteSheetAnimation(
            texture='/textures/new_bbm_sheet4.png',
            tileset_size=(18,5),
            fps=4,
            model='plane',
            animations={
                'idle': ((7,2), (8,2)),
                'walk_right': ((9,4),(10,4)),
                'walk_left': ((3,4),(4,4)),
                'walk_down': ((6,4),(7,4)),
                'walk_up': ((0,4),(1,4)),
                'interact': ((0,5),(0,5)),
                'damage': ((14,2),(17,2)),
                'death': ((6,1),(12,1)),
            }
        )
        self.__anims.parent = self
        self.__anims.play_animation('idle')

        for key, value in kwargs.items(): 
            setattr(self, key, value) 
        
    def __animer(self, direction: urs.Vec2 = urs.Vec2(0,0)):
        """Animations du joueur
        Le principe est le suivant :
            - selon que l'on avance ou pas :
                └> si l'animation est en pause, alors ça veut dire qu'elle ne se joue pas.
                    └> donc ça veut dire qu'on peut lancer une nouvelle animation."""
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
            if self.__anims.animations['idle'].paused and self.__anims.animations['damage'].paused:
                self.__anims.play_animation('idle')
    
    def __unbomb(self):
        self.bombed -= 1

    def input(self, key):
        """Entrées du clavier pour le joueur"""
        # if key == Keys.gamepad_x:
        if key == self.controls['atk']:
            if self.bombed < self.max_bomb + 1:
                self.bombed += 1
                if gm == 'br':
                    bombe_p = bombe.Bomb(murs_incassables,murs_cassables,bombes,balles,x=round(self.x),y=round(self.y),longueur=self.bomb_size)
                elif gm == 'foot':
                    bombe_p = bombe.Bomb(murs_incassables,murs_cassables,bombes,balles,x=self.x,y=self.y,longueur=self.bomb_size)
                urs.invoke(bombe_p.explode, delay=3)
                urs.invoke(self.__unbomb, delay=3)
                # @after(3)
                # def unbomb():
                #     self.bombed = False
    
    def update(self):
        """Actualisation des divers attributs du joueur
            1. On met à jour la direction (vecteur)
            2. On met à jour la position en fonction de la direction
            3. On met à jour l'étourdissement"""
        self.direction = urs.Vec2(urs.held_keys[self.controls['right']] - urs.held_keys[self.controls['left']], urs.held_keys[self.controls['up']] - urs.held_keys[self.controls['down']]).normalized()
        # self.direction = urs.Vec2(urs.held_keys[urs.Keys.gamepad_left_stick_x], urs.held_keys[urs.Keys.gamepad_left_stick_y]).normalized()
        if self.can_move:
            hit_map = urs.raycast(self.position , self.direction, traverse_target=carte, distance=.5, debug=False)
            if not hit_map:
                self.position += self.direction * urs.time.dt * self.speed
            self.__animer(self.direction)
            hit_pwup = urs.raycast(self.position , self.direction, traverse_target=power_ups, distance=.5, debug=False)
            if hit_pwup:
                if not hit_pwup.entity.collected :
                    hit_pwup.entity.collected = True
                    stat = hit_pwup.entity.stat_change()
                    if stat == 'speed':
                        self.speed += 1
                    elif stat == 'bomb_size':
                        self.bomb_size += 1
                    elif stat == 'max_bomb':
                        self.max_bomb += 1
                    hit_pwup.entity.recuperer()
        if self.intersects(bombes).hit:
            self.stunned = True
            self.can_move = False
        elif self.stunned:
            self.stunned = False
            self.lives -= 1
            if self.lives == 0:
                self.__anims.play_animation('death')
                urs.invoke(self.__anims.play_animation, 'idle', delay=self.respawn_time)
                urs.invoke(setattr, self, 'position', self.start_position, delay=self.respawn_time)
                urs.invoke(setattr, self, 'lives', self.max_lives, delay=self.respawn_time)
                urs.invoke(setattr, self, 'can_move', True, delay=self.respawn_time)
            else:
                self.__anims.play_animation('damage')
                urs.invoke(setattr, self, 'can_move', True, delay=gm_d[gm]['player']['stun_time'])
                urs.invoke(self.__anims.play_animation, 'idle', delay=gm_d[gm]['player']['stun_time'])


joueurs = []
carte = urs.Entity(model='quad', texture='./textures/vide')
murs_incassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
murs_cassables = urs.Entity(model='quad', texture='./textures/vide', parent=carte)
murs_deco = urs.Entity(model='quad', texture='./textures/vide')
murs_buts = urs.Entity(model='quad', texture='./textures/vide')
balles = urs.Entity(model='quad', texture='./textures/vide')
bombes = urs.Entity(model='quad', texture='./textures/vide')
# power_ups = pwup.PwupSpawner()
power_ups = urs.Entity(model='quad', texture='./textures/vide')


map1 = mapnlevel.scan_texture(urs.load_texture(f"./textures/{gm_d[gm]['map']['texture']}"))
print(map1)

# la première fois qu'une bombe explose, elle provoque un lag-spike, on en fait donc exploser une à l'avance dehors de l'écran
bombe_lag=bombe.Bomb(murs_incassables,murs_cassables,bombes,balles,position=(-100,-100)) ; urs.invoke(bombe_lag.explode, delay=0) # ; urs.destroy(bombe_lag, delay=0)


urs.EditorCamera()

player1 = Player(name='P1')
joueurs.append(player1)

player2 = Player(name='P2', controls={'up': 'up arrow','down': 'down arrow','left': 'left arrow','right': 'right arrow','atk':'right shift'})
joueurs.append(player2)

# test_pwup_feu1 = pwup.PowerUp(type='fire',power_ups=power_ups,x=-1,y=1)
# test_pwup_feu2 = pwup.PowerUp(type='fire',power_ups=power_ups,x=-1,y=2)
# test_pwup_feu3 = pwup.PowerUp(type='fire',power_ups=power_ups,x=-1,y=3)
# test_pwup_feu4 = pwup.PowerUp(type='fire',power_ups=power_ups,x=-1,y=4)
# test_pwup_feu5 = pwup.PowerUp(type='fire',power_ups=power_ups,x=-1,y=5)
# test_pwup_rolleur1 = pwup.PowerUp(type='roller',power_ups=power_ups,x=-3,y=1)
# test_pwup_rolleur2 = pwup.PowerUp(type='roller',power_ups=power_ups,x=-3,y=2)
# test_pwup_rolleur3 = pwup.PowerUp(type='roller',power_ups=power_ups,x=-3,y=3)
# test_pwup_rolleur4 = pwup.PowerUp(type='roller',power_ups=power_ups,x=-3,y=4)
# test_pwup_rolleur5 = pwup.PowerUp(type='roller',power_ups=power_ups,x=-3,y=5)
# test_pwup_bombup1 = pwup.PowerUp(type='bombup',power_ups=power_ups,x=-3,y=7)
# test_pwup_bombup2 = pwup.PowerUp(type='bombup',power_ups=power_ups,x=-3,y=8)
# test_pwup_bombup3 = pwup.PowerUp(type='bombup',power_ups=power_ups,x=-3,y=9)
# test_pwup_bombup4 = pwup.PowerUp(type='bombup',power_ups=power_ups,x=-3,y=10)
# test_pwup_bombup5 = pwup.PowerUp(type='bombup',power_ups=power_ups,x=-3,y=11)

mapnlevel.place_level(map1, murs_incassables, murs_cassables, murs_deco, murs_buts)
if gm_d[gm]['map']['bonus']:
    mapnlevel.place_bonus(texture_list=map1,nbr_pwup=50,power_ups=power_ups)
mapnlevel.place_player(map1,joueurs)
balle1 = ball.Ball(balles,murs_buts,carte,x=8,y=6)

urs.Sky(texture='deco_grass')

# EditorCamera()
urs.window.color = urs.color.light_gray
urs.window.borderless = False
urs.window.exit_button.visible = False

# app.run()
if __name__ == '__main__':
    app.run()

# 5.3.0