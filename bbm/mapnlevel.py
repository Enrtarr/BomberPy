import random
import ursina as urs
import pwup

if __name__ == '__main__':
    app = urs.Ursina()


class UnWall(urs.Entity):
    def __init__(self, murs_incassables:urs.Entity, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_incassables
        self.texture='./textures/UnWall'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

class BrWall(urs.Entity):
    def __init__(self, murs_cassables:urs.Entity, **kwargs): 
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

def place_level(texture_list:list, plr_list:list, murs_incassables:urs.Entity, murs_cassables:urs.Entity):
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
                UnWall(murs_incassables, position=(x,y))
            elif block == 2:
                BrWall(murs_cassables, position=(x,y))
            # si c'est un 3, on y place les joueurs chacun leurs tours
            elif block == 3:
                try:
                    plr_list[plr_i].start_position = (x, y)
                    if plr_list[plr_i].position != plr_list[plr_i].start_position:
                        plr_list[plr_i].position = plr_list[plr_i].start_position
                    plr_i += 1
                except IndexError:
                    print('Not enough players to spwan a new one')

def place_bonus(texture_list:list, nbr_pwup:int, power_ups:urs.Entity):
    width = len(texture_list[0])
    height = len(texture_list)
    pwup_i = 0
    while pwup_i != nbr_pwup:
        y = random.randint(0,height-1)
        x = random.randint(0,width-1)
        block = texture_list[y][x]
        # If it's black, it's solid, so we'll place a tile there.
        if block == 2:
            pwup.PowerUp(type='fire',power_ups=power_ups,y=y,x=x)
            pwup_i += 1
            print('place')

if __name__ == '__main__':
    app.run()