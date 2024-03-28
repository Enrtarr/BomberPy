import ursina as urs


class Ball(urs.Entity):
    def __init__(self, balles:urs.Entity, buts:urs.Entity, carte:urs.Entity, **kwargs): 
        super().__init__()     

        self.model = 'quad'
        self.collider = 'box'
        self.scale = .6
        self.parent = balles
        self.buts = buts
        self.carte = carte
        self.texture='./textures/Ball2'
        
        self.x_velocity = 0 ; self.y_velocity = 0
        self.old_x = self.x ; self.old_y = self.y
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)
    
    def reset(self):
        self.x = 8
        self.y = 6
     
    def update(self):
        self.old_x = self.x
        self.old_y = self.y
        
        hit_posiX = urs.raycast(self.position, (1,0), traverse_target=self.carte, distance=abs(self.x_velocity/10), debug=False)
        hit_negaX = urs.raycast(self.position, (-1,0), traverse_target=self.carte, distance=abs(self.x_velocity/10), debug=False)
        if not hit_posiX and not hit_negaX:
            self.x += self.x_velocity / 10
        hit_posiY = urs.raycast(self.position, (0,1), traverse_target=self.carte, distance=abs(self.y_velocity/10), debug=False)
        hit_negaY = urs.raycast(self.position, (0,-1), traverse_target=self.carte, distance=abs(self.y_velocity/10), debug=False)
        if not hit_posiY and not hit_negaY:
            self.y += self.y_velocity / 10
        
        if hit_posiX:
            self.x_velocity = - self.x_velocity
            self.x = self.old_x
            self.x -= .1
        elif hit_negaX:
            self.x_velocity = - self.x_velocity
            self.x = self.old_x
            self.x += .1
        if hit_posiY:
            self.y_velocity = - self.y_velocity
            self.y = self.old_y
            self.y -= .1
        elif hit_negaY:
            self.y_velocity = - self.y_velocity
            self.y = self.old_y
            self.y += .1
        
        if self.x_velocity > 0:
            self.x_velocity = round(self.x_velocity - .1, 1)
        elif self.x_velocity < 0:
            self.x_velocity = round(self.x_velocity + .1, 1)
        if self.y_velocity > 0:
            self.y_velocity = round(self.y_velocity - .1, 1)
        elif self.y_velocity < 0:
            self.y_velocity = round(self.y_velocity + .1, 1)
        
        if self.intersects(self.buts).hit:
            urs.invoke(self.reset, delay=1)
            self.x_velocity = 0
            self.y_velocity = 0