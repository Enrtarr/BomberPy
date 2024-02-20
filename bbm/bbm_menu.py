
import json

import ursina as urs

# import datamanager
# import splashscreen
import inputs


app = urs.Ursina(development_mode=True)

# urs.application.paused = True
# SC_duration = 4
# splashscreen.SplashScreen(
#     overlay_color=urs.color.white,
#     logo_texture='./textures/logo_aa.png',
#     delay_time=SC_duration,
#     audio='./audio/crazy_frog.mp3',
#     audio_volume=1
#     )
# urs.invoke(setattr, urs.application, 'paused', False, delay=1.2*SC_duration)


with open('./datas/settings.json', 'r') as liseur:
    settings_file = json.load(liseur)

class MenuButton(urs.Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.25, .075), highlight_color=urs.color.red, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)


# button_size = (.25, .075)
button_spacing = .075 * 1.25
menu_parent = urs.Entity(parent=urs.camera.ui, y=.15)
main_menu = urs.Entity(parent=menu_parent)
load_menu = urs.Entity(parent=menu_parent)
option_menu = urs.Entity(parent=menu_parent)
input_menu = urs.Entity(parent=menu_parent)

state_handler = urs.Animator({
    'main_menu' : main_menu,
    'load_menu' : load_menu,
    'option_menu' : option_menu,
    'input_menu' : input_menu,
    }
)

# main menu content
main_menu.buttons = [
    MenuButton('Jouer', on_click=urs.Func(setattr, state_handler, 'state', 'load_menu')),
    MenuButton('Options', on_click=urs.Func(setattr, state_handler, 'state', 'option_menu')),
    MenuButton('Quitter', on_click=urs.Sequence(urs.Wait(.01), urs.Func(urs.application.quit))),
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
    bbm.keys = temp_keys
    # bbm.atk_key = 

# charge le contenu du menu jouer
for i in range(3):
    MenuButton(parent=load_menu, text=f'Emplacement vide {i}', y=-i * button_spacing, on_click=start_game)

load_menu.back_button = MenuButton(
    parent=load_menu, 
    text='Retour', 
    y=((-i-2) * button_spacing), 
    on_click=urs.Func(setattr, state_handler, 'state', 'main_menu')
    )


# options menu content
preview_text = urs.Text(parent=option_menu, x=.275, y=.25, text='Texte d\'exemple', origin=(-.5,0))
# for t in [e for e in scene.entities if isinstance(e, Text)]:
#     t.original_scale = t.scale
    
options_e = []
inputs_e = []


text_scale_value = settings_file["TextSize"]
text_scale_slider = urs.Slider(
    0, 
    2, 
    default=text_scale_value, 
    step=.1, 
    dynamic=True, 
    text='Taille du texte :', 
    parent=option_menu, 
    x=-.25
    )

def set_text_scale():
    for t in [e for e in urs.scene.entities if isinstance(e, urs.Text) and hasattr(e, 'original_scale')]:
        t.scale = t.original_scale * text_scale_slider.value
text_scale_slider.on_value_changed = set_text_scale
# appelle la fonction afin de mettre le texte à la bonne taille
set_text_scale()

options_e.append(text_scale_slider)


audio_volume_value = settings_file["Volume"]
volume_slider = urs.Slider(0, 2, default=audio_volume_value, step=.1, text='Volume principal :', parent=option_menu, x=-.25)

def set_volume_multiplier():
    urs.Audio.volume_multiplier = volume_slider.value
volume_slider.on_value_changed = set_volume_multiplier

options_e.append(volume_slider)


def set_input_mode():
    if settings_file["InputMode"] == 'Clavier':
        settings_file["InputMode"] = 'Manette'
    else:
        settings_file["InputMode"] = 'Clavier'
    input_mode_button.text = settings_file["InputMode"]

input_mode = settings_file["InputMode"]
input_mode_button = urs.Button(
    parent=option_menu, 
    text=input_mode, 
    scale=(.25, .075), 
    highlight_color=urs.color.red, 
    on_click=urs.Func(set_input_mode),
    x=.125
    )
input_mode_text = urs.Text(parent=option_menu, text="Mode d'entrée", origin=(0,0), x=-.125, color=urs.color.white)

options_e.append(input_mode_button)

input_menu_button = MenuButton(parent=option_menu, text='Commandes', on_click=urs.Func(setattr, state_handler, 'state', 'input_menu'))
options_e.append(input_menu_button)


temp_keys = {
    "atk_key" : settings_file["Inputs"]["atk"],
    "pause_key" : settings_file["Inputs"]["pause"],
}

def apply():
    global input_mode, temp_keys
    
    settings_file["TextSize"] = round(text_scale_slider.value, 1)
    settings_file["Volume"] = round(volume_slider.value, 1)
    settings_file["InputMode"] = input_mode_button.text
    
    temp_keys['atk_key'] = i_atk_dial.key
    settings_file["Inputs"]["atk"] = i_atk_dial.key
    temp_keys['pause_key'] = i_pause_dial.key
    settings_file["Inputs"]["pause"] = i_pause_dial.key
    
    # settings_file["Inputs"]["pause"] = inputs_panel.content[1].text[0]
    # settings_file["Inputs"]["atk"] = inputs_panel.content[3].text[0]
    
    input_mode = input_mode_button.text
    # atk_key = inputs_panel.content[1].text[0]
    # pause_key = inputs_panel.content[3].text[0]
    
    with open('./datas/settings.json', 'w') as ecriveur:
        json.dump(settings_file, ecriveur, indent=4)
    

apply_button = MenuButton(
    parent=option_menu, 
    text='Appliquer', 
    x=0, 
    origin_x=-.5, 
    on_click=urs.Func(apply)
    )
options_back = MenuButton(
    parent=option_menu, 
    text='Retour', 
    x=-.25, 
    origin_x=-.5, 
    on_click=urs.Func(setattr, state_handler, 'state', 'main_menu')
    )
options_e.append(options_back)


input_back = MenuButton(
    parent=input_menu, 
    text='Retour', 
    x=-.25, 
    origin_x=-.5, 
    on_click=urs.Func(setattr, state_handler, 'state', 'option_menu')
    )
inputs_e.append(input_back)


i_atk_dial = inputs.InputChoiceDialogue(input_menu, "Attaque", temp_keys['atk_key'])
i_atk_show = inputs.InputChoiceButton(i_atk_dial, "Attaque")
# inputs_e.append(i_atk_dial)
inputs_e.append(i_atk_show)

i_pause_dial = inputs.InputChoiceDialogue(input_menu, "Pause", temp_keys['pause_key'])
i_pause_show = inputs.InputChoiceButton(i_pause_dial, "Pause")
# inputs_e.append(i_atk_dial)
inputs_e.append(i_pause_show)

for i, e in enumerate(options_e):
    e.y = -i * button_spacing
apply_button.y = options_back.y
input_mode_text.y = input_mode_button.y

for i, e in enumerate(inputs_e):
    e.y = -i * button_spacing
    print(i, e)


for t in [e for e in urs.scene.entities if isinstance(e, urs.Text)]:
    t.original_scale = t.scale


# animate the buttons in nicely when changing menu
for menu in (main_menu, load_menu, option_menu, input_menu):
    def animate_in_menu(menu=menu):
        for i, e in enumerate(menu.children):
            e.original_x = e.x
            e.x += .1
            e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=urs.curve.out_quad)

            e.alpha = 0
            e.animate('alpha', .7, delay=i*.05, duration=.1, curve=urs.curve.out_quad)

            if hasattr(e, 'text_entity'):
                e.text_entity.alpha = 0
                e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

    menu.on_enable = animate_in_menu


background = urs.Entity(
    parent=menu_parent, 
    model='quad', 
    texture='./textures/bbm_bg1', 
    scale=(urs.camera.aspect_ratio,1), 
    color=urs.color.white, 
    z=1, 
    world_y=0)

app.run()
