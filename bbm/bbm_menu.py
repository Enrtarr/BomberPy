
import json

from ursina import *

# import datamanager
import splashscreen

# app = Ursina(development_mode=False)
app=Ursina()


# application.paused = True
# SC_duration = 4
# splashscreen.SplashScreen(overlay_color=color.white,logo_texture='./textures/logo_aa.png',delay_time=SC_duration,audio='./audio/crazy_frog.mp3',audio_volume=1)
# invoke(setattr, application, 'paused', False, delay=1.2*SC_duration)


with open('./datas/settings.json', 'r') as liseur:
    settings_file = json.load(liseur)

class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.25, .075), highlight_color=color.red, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)

# button_size = (.25, .075)
button_spacing = .075 * 1.25
menu_parent = Entity(parent=camera.ui, y=.15)
main_menu = Entity(parent=menu_parent)
load_menu = Entity(parent=menu_parent)
option_menu = Entity(parent=menu_parent)
input_menu = Entity(parent=menu_parent)

state_handler = Animator({
    'main_menu' : main_menu,
    'load_menu' : load_menu,
    'option_menu' : option_menu,
    'input_menu' : input_menu,
    }
)

# main menu content
main_menu.buttons = [
    MenuButton('Jouer', on_click=Func(setattr, state_handler, 'state', 'load_menu')),
    MenuButton('Options', on_click=Func(setattr, state_handler, 'state', 'option_menu')),
    MenuButton('Quitter', on_click=Sequence(Wait(.01), Func(application.quit))),
]
# reparent les boutons principaux au menu principal
for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i-2) * button_spacing

# créer une fonction lançant le jeu et désactivant le menu
def start_game():
    menu_parent.enabled = False
    import bbm
    bbm.input_mode = input_mode

# charge le contenu du menu jouer
for i in range(3):
    MenuButton(parent=load_menu, text=f'Emplacement vide {i}', y=-i * button_spacing, on_click=start_game)

load_menu.back_button = MenuButton(parent=load_menu, text='Retour', y=((-i-2) * button_spacing), on_click=Func(setattr, state_handler, 'state', 'main_menu'))


# options menu content
preview_text = Text(parent=option_menu, x=.275, y=.25, text='Texte d\'exemple', origin=(-.5,0))
# for t in [e for e in scene.entities if isinstance(e, Text)]:
#     t.original_scale = t.scale
    
options = []


text_scale_value = settings_file["TextSize"]
text_scale_slider = Slider(0, 2, default=text_scale_value, step=.1, dynamic=True, text='Taille du texte :', parent=option_menu, x=-.25)

def set_text_scale():
    for t in [e for e in scene.entities if isinstance(e, Text) and hasattr(e, 'original_scale')]:
        t.scale = t.original_scale * text_scale_slider.value
text_scale_slider.on_value_changed = set_text_scale
# appelle la fonction afin de mettre le texte à la bonne taille
set_text_scale()

options.append(text_scale_slider)


audio_volume_value = settings_file["Volume"]
volume_slider = Slider(0, 2, default=audio_volume_value, step=.1, text='Volume principal :', parent=option_menu, x=-.25)

def set_volume_multiplier():
    Audio.volume_multiplier = volume_slider.value
volume_slider.on_value_changed = set_volume_multiplier

options.append(volume_slider)


def set_input_mode():
    if settings_file["InputMode"] == 'Clavier':
        settings_file["InputMode"] = 'Manette'
    else:
        settings_file["InputMode"] = 'Clavier'
    input_button.text = settings_file["InputMode"]

input_mode = settings_file["InputMode"]
input_button = Button(
    parent=option_menu, 
    text=input_mode, 
    scale=(.25, .075), 
    highlight_color=color.red, 
    on_click=Func(set_input_mode),
    x=.125
    )
input_mode_text = Text(parent=option_menu, text="Mode d'entrée", origin=(0,0), x=-.125, color=color.white)

options.append(input_button)

input_menu_button = MenuButton(parent=option_menu, text='Commandes', on_click=Func(setattr, state_handler, 'state', 'input_menu'))
options.append(input_menu_button)

def apply():
    settings_file["TextSize"] = round(text_scale_slider.value, 1)
    settings_file["Volume"] = round(volume_slider.value, 1)
    settings_file["InputMode"] = input_button.text
    
    with open('./datas/settings.json', 'w') as ecriveur:
        json.dump(settings_file, ecriveur, indent=4)
    

apply_button = MenuButton(parent=option_menu, text='Appliquer', x=0, origin_x=-.5, on_click=Func(apply))
options_back = MenuButton(parent=option_menu, text='Retour', x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'main_menu'))
options.append(options_back)


for i, e in enumerate(options):
    e.y = -i * button_spacing
apply_button.y = options_back.y
input_mode_text.y = input_button.y


for t in [e for e in scene.entities if isinstance(e, Text)]:
    t.original_scale = t.scale
    

input_back = MenuButton(parent=input_menu, text='Retour', x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'option_menu'))


# animate the buttons in nicely when changing menu
for menu in (main_menu, load_menu, option_menu, input_menu):
    def animate_in_menu(menu=menu):
        for i, e in enumerate(menu.children):
            e.original_x = e.x
            e.x += .1
            e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

            e.alpha = 0
            e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

            if hasattr(e, 'text_entity'):
                e.text_entity.alpha = 0
                e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

    menu.on_enable = animate_in_menu


background = Entity(parent=menu_parent, model='quad', texture='./textures/bbm_bg1', scale=(camera.aspect_ratio,1), color=color.white, z=1, world_y=0)

app.run()