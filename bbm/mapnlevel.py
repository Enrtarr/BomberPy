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

class BlocSol(urs.Entity):
    def __init__(self, murs_deco:urs.Entity, nom:str, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.z = .001
        self.parent = murs_deco
        self.texture= f'./textures/deco_{nom}'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)

class Goal(urs.Entity):
    def __init__(self, murs_buts:urs.Entity, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.parent = murs_buts
        self.texture='./textures/goal'
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)


def scan_texture(texture):
    """converstion nombre couleur:
        0-Blanc, 1-Noir, 2-Brun, 3-VertClair, 4-VertFonce, 5-Rose
    """
    scanned_tex = []
    
    for y in range(texture.height):
        scanned_tex.append([])
        for x in range(texture.width):
            scanned_tex[y].append(0)
            col = texture.get_pixel(x,y)
            if col == urs.color.rgb(255,255,255):
                scanned_tex[y][x] = 0
            # si c'est noir, on y place un mur incassable
            elif col == urs.color.rgb(0,0,0):
                scanned_tex[y][x] = 1
            elif col == urs.color.rgb(165,42,42):
                scanned_tex[y][x] = 2
            # si c'est vert, on y place les joueurs chacun leur tour
            elif col == urs.color.rgb(0,255,0):
                scanned_tex[y][x] = 3
            elif col == urs.color.rgb(0,128,0):
                scanned_tex[y][x] = 4
            elif col == urs.color.rgb(255,0,255):
                scanned_tex[y][x] = 5
            # elif col == urs.color.rgb():
            #     scanned_tex[y][x] = 6
    return scanned_tex

def place_level(texture_list:list, murs_incassables:urs.Entity, murs_cassables:urs.Entity, murs_deco:urs.Entity, murs_buts:urs.Entity):
    # destroy every child of the level parent.
    [urs.destroy(c) for c in murs_incassables.children]
    [urs.destroy(c) for c in murs_cassables.children]
    [urs.destroy(c) for c in murs_deco.children]
    
    width = len(texture_list[0])
    height = len(texture_list)
    urs.camera.position = (width/2, height/2)
    urs.camera.fov = width * 4
    
    for y in range(height):
        for x in range(width):
            block = texture_list[y][x]
            if block == 1:
                UnWall(murs_incassables, position=(x,y))
            elif block == 2:
                BrWall(murs_cassables, position=(x,y))
            elif block == 4:
                BlocSol(murs_deco,'grass', position=(x,y))
            elif block == 5:
                Goal(murs_buts, position=(x,y))
            

def place_player(texture_list:list, plr_list:list):
    
    width = len(texture_list[0])
    height = len(texture_list)
    
    plr_i = 0
    for y in range(height):
        for x in range(width):
            block = texture_list[y][x]
            # On  place les joueurs chacun leurs tours
            if block == 3:
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
            lst_pwup = ['fire','roller','bombup']
            pwup.PowerUp(type=lst_pwup[random.randint(0,len(lst_pwup)-1)],power_ups=power_ups,y=y,x=x)
            pwup_i += 1

if __name__ == '__main__':
    app.run()