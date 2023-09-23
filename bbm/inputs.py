
import json

import ursina as urs

if __name__ == '__main__':
    app = urs.Ursina()

with open('./datas/keys_keyboard.json', 'r') as liseur:
    keys_file = json.load(liseur)

class InputChoiceDialogue(urs.Entity):
    def __init__(self, input_menu:urs.Entity, key_name, key_value, **kwargs):
        super().__init__(**kwargs)
        
        self.parent = input_menu
        
        self.waiting = True
        self.key = key_value
        self.ok_keys = []
        for touche in keys_file["alphabet"]:
            self.ok_keys.append(touche)
        for touche in keys_file["other"]:
            self.ok_keys.append(touche)
        for touche in keys_file["numbers"]:
            self.ok_keys.append(touche)
        
        self.wp = urs.WindowPanel(
            title = key_name,
            content = (
                urs.Text('Appuyez sur une touche.'),
                urs.Text('Touche actuelle :'),
                urs.Space(-.5),
                urs.Text(self.key),
            ),
            lock = urs.Vec3(1,1,1)
            )
        
        self.cacher()
        
        for key, value in kwargs.items():
            setattr(self, key ,value)
    
    def __change_cont_txt(self, index, val):
        self.wp.content[index].text = val
        return val
    
    def attendre(self):
        urs.invoke(setattr, self, 'waiting', True, delay=.25)
        # self.waiting = True
    
    def montrer(self):
        self.wp.enable()
        self.wp.disabled = False
    
    def cacher(self):
        self.wp.disable()
        self.wp.disabled = False
    
    def input(self, key):
        if self.waiting:
            if key in self.ok_keys:
                self.key = key
                # print(self.wp.content[3].text)
                # self.wp.content[3].text = key
                self.waiting = False
                self.__change_cont_txt(3, key)
                self.cacher()

class InputChoiceButton(urs.Button):
    def __init__(self, ICD:InputChoiceDialogue, text:str, **kwargs):
        super().__init__(**kwargs)
        
        self.scale = (.25, .075)
        self.text = text
        self.highlight_color = urs.color.red
        
        self.highlight_scale = 1.1
        self.pressed_scale = 0.8
        
        self.on_click = urs.Sequence(
           urs.Func(ICD.montrer),
           urs.Func(ICD.attendre),
           )

        for key, value in kwargs.items():
            setattr(self, key ,value)

# atk = InputChoice()
atk2 = InputChoiceDialogue(urs.Entity(), 'nom de touche', 'space')

b = InputChoiceButton(atk2, y=.25, text='Montrer')

def update():
    print(atk2.key)


if __name__ == '__main__':
    app.run()
