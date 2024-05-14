import ursina as urs

if __name__ == '__main__':
    app = urs.Ursina()

class KeyCode(urs.Entity):
    def __init__(self, code:list, func, arg, **kwargs):
        super().__init__()
        
        self.keys = code
        self.index = 0
        self.function = func
        self.arg = arg
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)
    def input(self, key):
        if len(key) == 1:
            if key == self.keys[self.index]:
                self.index += 1
                if self.index == len(self.keys):
                    self.function(self.arg)
                    self.index = 0
            else:
                self.index = 0
                

if __name__ == '__main__':
    
    def reload_textures(blank):
        urs.application.hot_reloader.reload_textures()
    
    test = KeyCode(['s','u','s'],reload_textures,None)
    
    app.run()
