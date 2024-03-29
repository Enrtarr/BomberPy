from ursina import *
from ursina.networking import *
from collections import deque   # Il s'agit d'une sur-chouche de liste
import bombe

# -- Begin custom classes with serialization for networking --

class InputState:
    def __init__(self, input_state=None):
        if input_state is not None:
            self.up = input_state.up
            self.down = input_state.down
            self.left = input_state.left
            self.right = input_state.right
            self.sequence_number = input_state.sequence_number
            return

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.sequence_number = 0

    def copy(self):
        return InputState(self)

def serialize_input_state(writer, input_state):
    writer.write(input_state.up)
    writer.write(input_state.down)
    writer.write(input_state.left)
    writer.write(input_state.right)
    writer.write(input_state.sequence_number)

def deserialize_input_state(reader):
    input_state = InputState()
    input_state.up = reader.read(bool)
    input_state.down = reader.read(bool)
    input_state.left = reader.read(bool)
    input_state.right = reader.read(bool)
    input_state.sequence_number = reader.read(int)
    return input_state


class BearState:
    def __init__(self, bear_state=None):
        if bear_state is not None:
            self.uuid = bear_state.uuid
            self.x = bear_state.x
            self.y = bear_state.y
            self.input_state = bear_state.input_state.copy()
            return

        self.uuid = 0
        self.x = 0.0
        self.y = 0.0
        self.input_state = InputState()

    def copy(self):
        return BearState(self)

def serialize_bear_state(writer, bear_state):
    writer.write(bear_state.uuid)
    writer.write(bear_state.x)
    writer.write(bear_state.y)
    serialize_input_state(writer, bear_state.input_state)

def deserialize_bear_state(reader):
    bear_state = BearState()
    bear_state.uuid = reader.read(int)
    bear_state.x = reader.read(float)
    bear_state.y = reader.read(float)
    bear_state.input_state = deserialize_input_state(reader)
    return bear_state

# -- End custom classes with serialization for networking --

# -- Begin the main Bear (Player) class of the game --

# In general in a networked game you have two states for networked entities.
# There is the actual position / state, and then there is the visual state (how / where it's drawn).
# These two can differ. In general the visual state is an interpolation between two actual states.
# This gives the illusion of smooth movement between updates from the server.
# This is known as client side interpolation (CSI).
# The locally controlled player (your player) is not interpolated, instead it respondes immediately to controller input.
# This is known as client side prediction (CSP).
class Bear(Entity):
    def __init__(self,**kwargs):
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

        self.state = BearState()
        self.state.y = 0.1

        self.new_state = BearState()
        self.prev_state = self.new_state.copy()

        self.speed = 0.4

        self.lerping = False
        self.lerp_time = 0.0
        self.lerp_timer = 0.0

        self.talking = True
        self.talk_time = 0.0
        self.talk_timer = 0.0
        self.speech_audio = Audio("sine", autoplay=False, loop=True, loops=20)


        # self.model = 'quad'
        self.scale_y = 2
        self.rotation_x = -90
        # self.texture = '/textures/vide'
        self.always_on_top = True
        self.collider = 'box'

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

        self.__anims = SpriteSheetAnimation(
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
            print(key,value)
            setattr(self, key, value)

    def __animer(self, direction: Vec2 = Vec2(0,0)):
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
        if key == keys['atk_key']:
            if self.bombed < self.max_bomb + 1:
                self.bombed += 1
                if gm == 'br':
                    bombe_p = bombe.Bomb(murs_incassables,murs_cassables,bombes,balles,x=round(self.x),y=round(self.y),longueur=self.bomb_size)
                elif gm == 'foot':
                    bombe_p = bombe.Bomb(murs_incassables,murs_cassables,bombes,balles,x=self.x,y=self.y,longueur=self.bomb_size)
                invoke(bombe_p.explode, delay=3)
                invoke(self.__unbomb, delay=3)
                # @after(3)
                # def unbomb():
                #     self.bombed = False

    def update(self):
        """Actualisation des divers attributs du joueur
            1. On met à jour la direction (vecteur)
            2. On met à jour la position en fonction de la direction
            3. On met à jour l'étourdissement"""

        self.x = self.state.x
        self.y = self.state.y

        self.direction = Vec2(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']).normalized()

        # self.direction = Vec2(held_keys[Keys.gamepad_left_stick_x], held_keys[Keys.gamepad_left_stick_y]).normalized()
        if self.can_move:
            hit_map = raycast(self.position , self.direction, traverse_target=carte, distance=.5, debug=False)
            if not hit_map:
                self.position += self.direction * time.dt * self.speed
            self.__animer(self.direction)
            hit_pwup = raycast(self.position , self.direction, traverse_target=power_ups, distance=.5, debug=False)
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
                invoke(self.__anims.play_animation, 'idle', delay=self.respawn_time)
                invoke(setattr, self, 'position', self.start_position, delay=self.respawn_time)
                invoke(setattr, self, 'lives', self.max_lives, delay=self.respawn_time)
                invoke(setattr, self, 'can_move', True, delay=self.respawn_time)
            else:
                self.__anims.play_animation('damage')
                invoke(setattr, self, 'can_move', True, delay=gm_d[gm]['player']['stun_time'])
                invoke(self.__anims.play_animation, 'idle', delay=gm_d[gm]['player']['stun_time'])

    # The actual update function with normal game logic.
    # This is a fixed timestep, sometimes also called fixed_update, tick, step, or fixed.
    # The delta time argument (dt) is fixed, it's constant.
    def tick(self, dt):
        self.state.x += float(int(self.state.input_state.right) - int(self.state.input_state.left)) * self.speed * dt
        self.state.y += float(int(self.state.input_state.up) - int(self.state.input_state.down)) * self.speed * dt

    def interpolate(self, start_state, end_state, duration):
        if self.lerping:
            self.state = self.new_state.copy()
        self.lerping = True
        self.lerp_time = duration
        self.lerp_timer = 0.0
        self.prev_state = start_state.copy()
        self.new_state = end_state.copy()

    def set_speech(self, msg, duration):
        self.talking = True
        self.talk_time = duration
        self.talk_timer = 0.0
        self.speech_text.text = msg
        self.speech_audio.play()

# -- End the main Bear (Player) class of the game --

# -- Begin game initialization and global state (putting this into a class would be a good idea) --

app = Ursina(borderless=False)

uuid_counter = 0

start_text = "Host or join a room."
status_text = Text(text=start_text, origin=(0, 0), z=1, y=0.1)
host_input_field = InputField(default_value="localhost", scale_x=0.6, scale_y=0.1)
host_button = Button(text="Host", scale_x=0.28, scale_y=0.1, x=-0.16, y=-0.11)
join_button = Button(text="Join", scale_x=0.28, scale_y=0.1, x=0.16, y=-0.11)

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
keys = {
    "atk_key" : 'space',
    "pause_key" : 'escape',
}

bears = []

my_bear_uuid = None
uuid_to_bear = dict()

connection_to_bear = dict()

input_state = InputState()

inputs_received = dict()
input_buffer = []
send_input_buffer = []

tick_rate = 1.0 / 60.0
tick_timer = 0.0
time_factor = 1.0

update_rate = 1.0 / 20.0
update_timer = 0.0

speech_duration = 3.0

# Setting a connection timeout is important to detect disconnects.
peer = RPCPeer(connection_timeout=5.0)

# These registered types can be used as types in remote procedure calls.
peer.register_type(InputState, serialize_input_state, deserialize_input_state)
peer.register_type(BearState, serialize_bear_state, deserialize_bear_state)

# -- End game initialization and global state (putting this into a class would be a good idea) --

# -- Begin remote procedure calls (for both host and client) --

@rpc(peer)
def on_connect(connection, time_connected):
    global uuid_counter

    # If this is the server, we need to make a new bear, and track which connection is associated with it.
    # Each bear is assigned a unique id, so that it can be synchronized across the network.
    # This id will be the same on both server and client.
    if peer.is_hosting():
        b = Bear()
        b.state.uuid = uuid_counter
        uuid_counter += 1
        bears.append(b)
        uuid_to_bear[b.state.uuid] = b
        connection_to_bear[connection] = b
        inputs_received[b.state.uuid] = deque()
        connection.rpc_peer.set_bear_uuid(connection, b.state.uuid)
        s = [b.state for b in bears]
        for conn in connection.peer.get_connections():
            connection.rpc_peer.spawn_bears(conn, s)
        print("Bear count:", len(bears))

@rpc(peer)
def on_disconnect(connection, time_disconnected):
    if peer.is_hosting():
        b = connection_to_bear.get(connection)
        if b is not None:
            destroy(b)
            bears.remove(b)
            del uuid_to_bear[b.state.uuid]
            del connection_to_bear[connection]
            del inputs_received[b.state.uuid]
            for conn in connection.rpc_peer.get_connections():
                connection.rpc_peer.remove_bears(conn, [b.state.uuid])
        if connection.is_timed_out():
            print("\tConnection timed out.")
        print("Bear count:", len(bears))
    else:
        for bear in bears:
            destroy(bear)
            del uuid_to_bear[bear.state.uuid]
        bears.clear()
        my_bear_uuid = None
        if connection.is_timed_out():
            print("\tConnection timed out.")


# The client needs to know which bear is their bear that they control.
@rpc(peer)
def set_bear_uuid(connection, time_received, uuid: int):
    global my_bear_uuid

    if connection.peer.is_hosting():
        return

    my_bear_uuid = uuid

@rpc(peer)
def spawn_bears(connection, time_received, new_bears: list[BearState]):
    if connection.peer.is_hosting():
        return

    for state in new_bears:
        if state.uuid not in uuid_to_bear:
            b = Bear()
            b.state = state.copy()
            bears.append(b)
            uuid_to_bear[state.uuid] = b

@rpc(peer)
def remove_bears(connection, time_received, to_be_removed: list[int]):
    global my_bear_uuid

    if connection.peer.is_hosting():
        return

    for uuid in to_be_removed:
        bear = uuid_to_bear.get(uuid)
        if bear is not None:
            destroy(bear)
            bears.remove(bear)
            del uuid_to_bear[uuid]
            if uuid == my_bear_uuid:
                my_bear_uuid = None

@rpc(peer)
def set_states(connection, time_received, bear_states: list[BearState]):
    global time_factor

    if connection.peer.is_hosting():
        return

    for new_bear_state in bear_states:
        bear = uuid_to_bear.get(new_bear_state.uuid)
        if bear is None:
            continue

        # Interpolate other bears, and predict my bear.
        if my_bear_uuid is None or my_bear_uuid != new_bear_state.uuid:
            # A better way would be to keep a buffer of the past N states and interpolate between them.
            bear.interpolate(bear.state, new_bear_state, update_rate * 2.0)
        else:
            # Compute processed input difference between client and host.
            sequence_delta = input_state.sequence_number - new_bear_state.input_state.sequence_number
            # Maybe slow down if ahead of host.
            max_delta = ((update_rate / tick_rate) + 1) * 2.5
            if sequence_delta > max_delta:
                time_factor = 0.95
            elif sequence_delta < max_delta * 0.75:
                time_factor = 1.0
            my_bear = uuid_to_bear.get(my_bear_uuid)
            if my_bear is None:
                continue
            # Reconcile with host.
            my_bear.state = new_bear_state.copy()
            if sequence_delta > 0 and sequence_delta < len(input_buffer):
                # Re-apply all inputs after the last processed input.
                for state in input_buffer[len(input_buffer) - sequence_delta:]:
                    bear.state.input_state = state.copy()
                    bear.tick(tick_rate)

@rpc(peer)
def set_inputs(connection, time_received, input_states: list[InputState]):
    if not connection.peer.is_hosting():
        return

    for state in input_states:
        b = connection_to_bear.get(connection)
        if b is None:
            return
        input_queue = inputs_received.get(b.state.uuid)
        if input_queue is None:
            return
        if len(input_queue) > 100:
            # Host is being spammed, disconnect.
            print("Peer is spamming inputs, disconnecting...")
            connection.disconnect()
            return
        input_queue.append(state)

@rpc(peer)
def chat(connection, time_received, uuid: int, msg: str):
    if connection.rpc_peer.is_hosting():
        bear = connection_to_bear.get(connection)
        if bear is None:
            return
        if bear.state.uuid == uuid:
            for conn in connection.rpc_peer.get_connections():
                connection.rpc_peer.chat(conn, uuid, msg)
            bear.set_speech(msg, speech_duration)
    else:
        bear = uuid_to_bear.get(uuid)
        if bear is None:
            return
        bear.set_speech(msg, speech_duration)

# -- End remote procedure calls (for both host and client) --

def host():
    global uuid_counter, my_bear_uuid

    b = Bear()
    b.state.uuid = uuid_counter
    uuid_counter += 1
    bears.append(b)
    uuid_to_bear[b.state.uuid] = b
    my_bear_uuid = b.state.uuid

    h = host_input_field.text
    port = 8080

    peer.start(h, port, is_host=True)
    host_input_field.enabled = False
    host_button.enabled = False
    join_button.enabled = False

host_button.on_click = host

def join():
    h = host_input_field.text
    port = 8080

    peer.start(h, port, is_host=False)
    host_input_field.enabled = False
    host_button.disabled = True
    host_button.enabled = False
    join_button.disabled = True
    join_button.enabled = False

join_button.on_click = join

#  Networked games require a fixed timestep to function semi-deterministically.
def tick(dt):
    global last_input_sequence_number_processed

    if time_factor < 1.0:
        print("Host is lagging, slowing down local simulation.")

    input_state.up = bool(held_keys["w"])
    input_state.down = bool(held_keys["s"])
    input_state.right = bool(held_keys["d"])
    input_state.left = bool(held_keys["a"])
    if my_bear_uuid is not None:
        my_bear = uuid_to_bear.get(my_bear_uuid)
        if my_bear is not None:
            my_bear.state.input_state = input_state
            my_bear.tick(dt)

    if not peer.is_hosting():
        if my_bear_uuid is not None:
            input_state.sequence_number += 1
            input_buffer.append(input_state.copy())
            if len(input_buffer) >= 100:
                input_buffer.pop(0)
            send_input_buffer.append(input_buffer[-1])
            if len(send_input_buffer) > 10:
                send_input_buffer.pop(0)
    else:
        for bear in bears:
            if my_bear_uuid is None or my_bear_uuid != bear.state.uuid:
                input_queue = inputs_received.get(bear.state.uuid)
                if input_queue is None:
                    continue
                if len(input_queue) > 0:
                    bear.state.input_state = input_queue.popleft()
                else:
                    bear.state.input_state.up = False
                    bear.state.input_state.down = False
                    bear.state.input_state.left = False
                    bear.state.input_state.right = False
                bear.tick(dt)

def update():
    global update_timer, tick_timer

    # Remember to update the peer (process network events waiting in queue).
    peer.update()
    if not peer.is_running():
        status_text.text = start_text
        status_text.y = 0.1
        host_input_field.enabled = True
        host_button.disabled = False
        host_button.enabled = True
        join_button.disabled = False
        join_button.enabled = True
        return

    host_input_field.enabled = False
    host_button.disabled = True
    host_button.enabled = False
    join_button.disabled = True
    join_button.enabled = False
    if peer.is_hosting():
        status_text.text = "Hosting.\nWASD to move."
        status_text.y = -0.45
    else:
        status_text.text = "Connected to host.\nWASD to move."
        status_text.y = -0.45

    # Try to call the fixed timestep function at a fixed rate.
    tick_timer += time.dt * time_factor
    while tick_timer >= tick_rate:
        tick(tick_rate)
        tick_timer -= tick_rate

    # Try to send network messages (RPCs) at a fixed rate.
    # "update_rate" is not a very descriptive name.
    update_timer += time.dt
    if update_timer >= update_rate:
        if peer.is_running() and peer.connection_count() > 0:
            if peer.is_hosting():
                s = [b.state for b in bears]
                for connection in peer.get_connections():
                    peer.set_states(connection, s)
            else:
                peer.set_inputs(peer.get_connections()[0], send_input_buffer)
                send_input_buffer.clear()
        update_timer = 0.0

def input(key):
    if key == "f5":
        peer.stop()
    if key == "f9":
        peer.stop()
    if not peer.is_running():
        return

carte = Entity(model='quad', texture='./textures/vide')
murs_incassables = Entity(model='quad', texture='./textures/vide', parent=carte)
murs_cassables = Entity(model='quad', texture='./textures/vide', parent=carte)
murs_deco = Entity(model='quad', texture='./textures/vide')
murs_buts = Entity(model='quad', texture='./textures/vide')
balles = Entity(model='quad', texture='./textures/vide')
bombes = Entity(model='quad', texture='./textures/vide')
power_ups = Entity(model='quad', texture='./textures/vide')

app.run()
