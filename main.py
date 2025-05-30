import pygame
import os
import math
from enum import Enum, auto
import sys

# ----- Definições de Estado e Símbolo -----
class State(Enum):
    IDLE = auto()
    IDLE_LEFT = auto()
    WALK_RIGHT = auto()
    WALK_LEFT = auto()
    RUN_RIGHT = auto()
    RUN_LEFT = auto()
    CROUCH = auto()
    CROUCH_LEFT = auto()
    CROUCH_WALK = auto()
    CROUCH_WALK_LEFT = auto()
    JUMP = auto()
    JUMP_LEFT = auto()
    RAIKIRI = auto()
    RAIKIRI_LEFT = auto()
    ATTACK = auto()
    ATTACK_LEFT = auto()
    ATTACK_CROUCH = auto()
    ATTACK_CROUCH_LEFT = auto()
    ATTACK_RUN = auto()
    ATTACK_RUN_LEFT = auto()
    ATTACK_UP = auto()
    ATTACK_UP_LEFT = auto()
    SHARINGAN = auto()
    SHARINGAN_LEFT = auto()
    WIN = auto()
    WIN_LEFT = auto()
    NINDOG_RIGHT = auto()
    NINDOG_LEFT = auto()


# Símbolos de entrada (None equivale a nenhuma tecla)
Symbol = str

# ----- Tabela de Transições (δ) -----
# Chave: (estado_atual, símbolo) -> próximo estado
transitions: dict[tuple[State, Symbol], State] = {
    (State.IDLE,      'A'): State.WALK_LEFT,
    (State.IDLE,      'D'): State.WALK_RIGHT,
    (State.IDLE,      'SHIFT+A'): State.RUN_LEFT,
    (State.IDLE,      'SHIFT+D'): State.RUN_RIGHT,
    (State.IDLE,      'S'): State.CROUCH,
    (State.IDLE,      'S+A'): State.CROUCH_WALK_LEFT,
    (State.IDLE,      'S+D'): State.CROUCH_WALK,
    (State.IDLE,      'SPACE'): State.JUMP,
    (State.IDLE,      'R+T'): State.RAIKIRI,
    (State.IDLE,        'H'): State.ATTACK,
    (State.IDLE,      None): State.IDLE,
    (State.IDLE,    'U'): State.ATTACK_UP,
    (State.IDLE,      'J'): State.SHARINGAN,
    (State.IDLE,      'P'): State.WIN,
    (State.IDLE,      'M'): State.NINDOG_RIGHT,





    (State.IDLE_LEFT, 'A'): State.WALK_LEFT,
    (State.IDLE_LEFT, 'D'): State.WALK_RIGHT,
    (State.IDLE_LEFT, 'SHIFT+A'): State.RUN_LEFT,
    (State.IDLE_LEFT, 'SHIFT+D'): State.RUN_RIGHT,
    (State.IDLE_LEFT, 'S'): State.CROUCH_LEFT,
    (State.IDLE_LEFT, 'S+A'): State.CROUCH_WALK_LEFT,
    (State.IDLE_LEFT, 'S+D'): State.CROUCH_WALK,
    (State.IDLE_LEFT, 'SPACE'): State.JUMP_LEFT,
    (State.IDLE_LEFT, 'R+T'): State.RAIKIRI_LEFT,
    (State.IDLE_LEFT, None): State.IDLE_LEFT,
    (State.IDLE_LEFT,   'H'): State.ATTACK_LEFT,
    (State.IDLE_LEFT, 'U'): State.ATTACK_UP_LEFT,
    (State.IDLE_LEFT, 'J'): State.SHARINGAN_LEFT,
    (State.IDLE_LEFT, 'P'): State.WIN_LEFT,
    (State.IDLE_LEFT, 'M'): State.NINDOG_LEFT,


    (State.WALK_RIGHT, 'D'): State.WALK_RIGHT,
    (State.WALK_RIGHT, 'A'): State.WALK_LEFT,
    (State.WALK_RIGHT, 'SHIFT+D'): State.RUN_RIGHT,
    (State.WALK_RIGHT, 'S'): State.CROUCH,
    (State.WALK_RIGHT, 'SPACE'): State.JUMP,
    (State.WALK_RIGHT, None): State.IDLE,
    (State.WALK_RIGHT, 'H'): State.ATTACK,
    (State.WALK_RIGHT, 'R+T'): State.WALK_RIGHT,
    (State.WALK_RIGHT, 'U'): State.ATTACK_UP,
    (State.WALK_RIGHT, 'P'): State.WALK_RIGHT,

    (State.WALK_LEFT,  'A'): State.WALK_LEFT,
    (State.WALK_LEFT,  'D'): State.WALK_RIGHT,
    (State.WALK_LEFT,  'SHIFT+A'): State.RUN_LEFT,
    (State.WALK_LEFT,  'S'): State.CROUCH_LEFT,
    (State.WALK_LEFT,  'SPACE'): State.JUMP_LEFT,
    (State.WALK_LEFT,  None): State.IDLE_LEFT,
    (State.WALK_LEFT, 'H'): State.ATTACK_LEFT,
    (State.WALK_LEFT, 'R+T'): State.WALK_LEFT,
    (State.WALK_LEFT, 'U'): State.ATTACK_UP_LEFT,
    (State.WALK_LEFT, 'P'): State.WALK_LEFT,

    (State.RUN_RIGHT,  'SHIFT+D'): State.RUN_RIGHT,
    (State.RUN_RIGHT,  'SHIFT+A'): State.RUN_LEFT,
    (State.RUN_RIGHT,  'D'): State.WALK_RIGHT,
    (State.RUN_RIGHT,  'A'): State.WALK_LEFT,
    (State.RUN_RIGHT,  'S'): State.CROUCH,
    (State.RUN_RIGHT,  'SPACE'): State.JUMP,
    (State.RUN_RIGHT,  None): State.IDLE,
    (State.RUN_RIGHT, 'H'): State.ATTACK_RUN,
    (State.RUN_RIGHT, 'R+T'): State.RUN_RIGHT,
    (State.RUN_RIGHT, 'U'): State.ATTACK_UP,
    (State.RUN_RIGHT, 'P'): State.RUN_RIGHT,

    (State.RUN_LEFT,   'SHIFT+A'): State.RUN_LEFT,
    (State.RUN_LEFT,  'SHIFT+D'): State.RUN_RIGHT,
    (State.RUN_LEFT,   'A'): State.WALK_LEFT,
    (State.RUN_LEFT,   'D'): State.WALK_RIGHT,
    (State.RUN_LEFT,   'S'): State.CROUCH_LEFT,
    (State.RUN_LEFT,   'SPACE'): State.JUMP_LEFT,
    (State.RUN_LEFT,   None): State.IDLE_LEFT,
    (State.RUN_LEFT, 'H'): State.ATTACK_RUN_LEFT,
    (State.RUN_LEFT, 'R+T'): State.RUN_LEFT,
    (State.RUN_LEFT, 'U'): State.ATTACK_UP_LEFT,
    (State.RUN_LEFT, 'P'): State.RUN_LEFT,



    (State.CROUCH,     'S'): State.CROUCH,
    (State.CROUCH,     'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH,     'S+D'): State.CROUCH_WALK,
    (State.CROUCH,     'SPACE'): State.JUMP,
    (State.CROUCH,     None): State.IDLE,
    (State.CROUCH,     'R+T'): State.CROUCH,
    (State.CROUCH,     'H'): State.ATTACK_CROUCH,
    (State.CROUCH,     'U'): State.ATTACK_UP,
    (State.CROUCH,     'P'): State.CROUCH,

    (State.CROUCH_LEFT,'S'): State.CROUCH_LEFT,
    (State.CROUCH_LEFT,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_LEFT,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_LEFT,'SPACE'): State.JUMP_LEFT,
    (State.CROUCH_LEFT, None): State.IDLE_LEFT,
    (State.CROUCH_LEFT, 'R+T'): State.CROUCH_LEFT,
    (State.CROUCH_LEFT,'H'): State.ATTACK_CROUCH_LEFT,
    (State.CROUCH_LEFT, 'U'): State.ATTACK_UP_LEFT,
    (State.CROUCH_LEFT, 'P'): State.CROUCH_LEFT,

    (State.CROUCH_WALK,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_WALK,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_WALK,'S'): State.CROUCH,
    (State.CROUCH_WALK,'SPACE'): State.JUMP,
    (State.CROUCH_WALK, None): State.CROUCH,
    (State.CROUCH_WALK, 'R+T'): State.CROUCH_WALK,
    (State.CROUCH_WALK, 'H'): State.ATTACK_CROUCH,
    (State.CROUCH_WALK, 'U'): State.ATTACK_UP,
    (State.CROUCH_WALK, 'P'): State.CROUCH_WALK,

    (State.CROUCH_WALK_LEFT,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_WALK_LEFT,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_WALK_LEFT,'S'): State.CROUCH_LEFT,
    (State.CROUCH_WALK_LEFT,'SPACE'): State.JUMP_LEFT,
    (State.CROUCH_WALK_LEFT, None): State.CROUCH_LEFT,
    (State.CROUCH_WALK_LEFT, 'R+T'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_WALK_LEFT, 'H'): State.ATTACK_CROUCH_LEFT,
    (State.CROUCH_WALK_LEFT, 'U'): State.ATTACK_UP_LEFT,
    (State.CROUCH_WALK_LEFT, 'P'): State.CROUCH_WALK_LEFT,

    # Jump and Raikiri preserve
    (State.JUMP, None): State.JUMP,
    (State.JUMP_LEFT, None): State.JUMP_LEFT,
    (State.RAIKIRI, None): State.RAIKIRI,
    (State.RAIKIRI_LEFT, None): State.RAIKIRI_LEFT,

    # Attack preserve
    (State.ATTACK, None): State.ATTACK,
    (State.ATTACK_LEFT, None): State.ATTACK_LEFT,
    (State.ATTACK_CROUCH, None): State.ATTACK_CROUCH,
    (State.ATTACK_CROUCH_LEFT, None): State.ATTACK_CROUCH_LEFT,
    (State.ATTACK_RUN, None): State.ATTACK_RUN,
    (State.ATTACK_RUN_LEFT, None): State.ATTACK_RUN_LEFT,
    (State.ATTACK_UP, None): State.ATTACK_UP,
    (State.ATTACK_UP_LEFT, None): State.ATTACK_UP_LEFT,
    (State.SHARINGAN, None): State.SHARINGAN,
    (State.SHARINGAN_LEFT, None): State.SHARINGAN_LEFT,
    (State.WIN, None): State.WIN,
    (State.WIN_LEFT, None): State.WIN_LEFT,
    (State.NINDOG_RIGHT, None): State.NINDOG_RIGHT,
    (State.NINDOG_LEFT, None): State.NINDOG_LEFT,
}

def init_pygame(width=1500, height=800):
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("AFD - Animação Personagem")
    clock = pygame.time.Clock()
    return screen, clock

# Carrega imagem com canal alpha
def load_image(path):
    return pygame.image.load(path).convert_alpha()

# Carrega sequência de frames a partir de pasta, prefixo e quantidade
def load_frames(folder, prefix, count, scale=1.0):
    frames = []
    raw = []
    max_w = max_h = 0
    for i in range(1, count + 1):
        img = load_image(os.path.join(folder, f"{prefix}-{i}.png"))
        rect = img.get_bounding_rect()
        raw.append((img, rect))
        max_w = max(max_w, rect.width)
        max_h = max(max_h, rect.height)
    for img, rect in raw:
        surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        dest = rect.copy()
        dest.midbottom = (max_w // 2, max_h)
        surf.blit(img, dest.topleft, rect)
        # Escala aplicada aqui
        if scale != 1.0:
            new_size = (int(surf.get_width() * scale), int(surf.get_height() * scale))
            surf = pygame.transform.scale(surf, new_size)
        frames.append(surf)
    return frames


# Diretórios de sprites
base = os.path.dirname(__file__)
stand_folder       = os.path.join(base, 'Sprite', 'stand')
stand_left_folder  = os.path.join(stand_folder, 'espelhadas')
walk_r_folder      = os.path.join(base, 'Sprite', 'walk')
walk_l_folder      = os.path.join(walk_r_folder, 'espelhadas')
run_r_folder       = os.path.join(base, 'Sprite', 'run')
run_l_folder       = os.path.join(run_r_folder, 'espelhadas')
crouch_folder      = os.path.join(base, 'Sprite', 'crouch')
crouch_left_folder = os.path.join(crouch_folder, 'espelhadas')
crouch_walk_folder = os.path.join(base, 'Sprite', 'crouchWalk')
crouch_walk_left   = os.path.join(crouch_walk_folder, 'espelhadas')
jump_r_folder      = os.path.join(base, 'Sprite', 'jump')
jump_l_folder      = os.path.join(jump_r_folder, 'espelhadas')
raikiri_r_folder = os.path.join(base, 'Sprite', 'raikiri')
raikiri_l_folder = os.path.join(raikiri_r_folder, 'espelhadas')
attack_r_folder    = os.path.join(base, 'Sprite', 'attack')
attack_l_folder    = os.path.join(attack_r_folder, 'espelhadas')
attack_c_folder    = os.path.join(base, 'Sprite', 'attackCombo')
attack_c_l_folder  = os.path.join(attack_c_folder, 'espelhadas')
attack_run_folder    = os.path.join(base, 'Sprite', 'attackCombo')
attack_run_l_folder  = os.path.join(attack_run_folder, 'espelhadas')
attack_up_folder   = os.path.join(base, 'Sprite', 'attackCombo')
attack_up_l_folder = os.path.join(attack_up_folder, 'espelhadas')
sharingan_r_folder = os.path.join(base, 'Sprite', 'sharingan')
sharingan_l_folder = os.path.join(sharingan_r_folder, 'espelhadas')
win_r_folder = os.path.join(base, 'Sprite', 'win')
win_l_folder = os.path.join(win_r_folder, 'espelhadas')
nindog_r_folder = os.path.join(base,'Sprite', 'ninDogs')
nindog_l_folder = os.path.join(nindog_r_folder,'espelhadas')



# Parâmetros
crouch_walk_speed = 1.6
walk_speed = 3
run_speed = 10
jump_height = 400
jump_duration = 50  # frames
frame_rates = {
    'default':8,
    'attack':4,
    'crouch_attack':4,
    'run_attack':4,
    'up_attack':4,
    'sharingan': 4,
}

# Função principal
def main():
    screen, clock = init_pygame()
    background = pygame.image.load(os.path.join(base, 'Mapa', 'mapa4.jpg')).convert()
    background = pygame.transform.scale(background, screen.get_size())
    orig_background = background
    mapa3 = pygame.image.load(os.path.join(base, 'Mapa', 'mapa3.jpg')).convert()
    mapa3 = pygame.transform.scale(mapa3, screen.get_size())

    sound_sharingan = pygame.mixer.Sound(os.path.join(base, 'Sons', 'sharingan.mp3'))
    sound_raikiri = pygame.mixer.Sound(os.path.join(base, 'Sons', 'raikiri.mp3'))

    sound_sharingan.set_volume(0.5)
    sound_raikiri.set_volume(0.5)

    scale = 4.0
    frames = {
        State.IDLE: load_frames(stand_folder, 'stand', 6, scale),
        State.IDLE_LEFT: load_frames(stand_left_folder, 'stand', 6, scale),
        State.WALK_RIGHT: load_frames(walk_r_folder, 'walk', 6, scale),
        State.WALK_LEFT: load_frames(walk_l_folder, 'walk', 6, scale),
        State.RUN_RIGHT: load_frames(run_r_folder, 'run', 6, scale),
        State.RUN_LEFT: load_frames(run_l_folder, 'run', 6, scale),
        State.CROUCH: load_frames(crouch_folder, 'crouch', 2, scale),
        State.CROUCH_LEFT: load_frames(crouch_left_folder, 'crouch', 2, scale),
        State.CROUCH_WALK: load_frames(crouch_walk_folder, 'crouchWalk', 6, scale),
        State.CROUCH_WALK_LEFT: load_frames(crouch_walk_left, 'crouchWalk', 6, scale),
        State.JUMP: load_frames(jump_r_folder, 'jump', 4, scale),
        State.JUMP_LEFT: load_frames(jump_l_folder, 'jump', 4, scale),
        State.RAIKIRI: load_frames(raikiri_r_folder, 'raikiri', 26, scale),
        State.RAIKIRI_LEFT: load_frames(raikiri_l_folder, 'raikiri', 26, scale),
        State.ATTACK: load_frames(attack_r_folder, 'attack1', 13, scale),
        State.ATTACK_LEFT: load_frames(attack_l_folder, 'attack1', 13, scale),
        State.ATTACK_CROUCH: load_frames(attack_c_folder,'attack(crouch)', 5, scale),
        State.ATTACK_CROUCH_LEFT: load_frames(attack_c_l_folder, 'attack(crouch)', 5, scale),
        State.ATTACK_RUN: load_frames(attack_run_folder, 'attack(run)', 6, scale),
        State.ATTACK_RUN_LEFT: load_frames(attack_run_l_folder, 'attack(run)', 6, scale),
        State.ATTACK_UP: load_frames(attack_up_folder, 'attack(up)', 5, scale),
        State.ATTACK_UP_LEFT: load_frames(attack_up_l_folder, 'attack(up)', 5, scale),
        State.SHARINGAN: load_frames(sharingan_r_folder,'sharingan', 21, scale),
        State.SHARINGAN_LEFT: load_frames(sharingan_l_folder, 'sharingan', 21,scale),
        State.WIN: load_frames(win_r_folder, 'win', 11, scale),
        State.WIN_LEFT: load_frames(win_l_folder, 'win', 11, scale),
        State.NINDOG_RIGHT: load_frames(nindog_r_folder, 'ninDogs', 25, scale),
        State.NINDOG_LEFT: load_frames(nindog_l_folder, 'ninDogs', 25, scale),
    }

    state = State.IDLE
    frame_index = 0
    tick = 0
    x_pos = screen.get_width() // 2
    y_pos = screen.get_height() - 50
    jump_timer = 0
    running = True
    fade_duration = 300  # duração do fade em ms
    fade_start = 0

    sharingan_triggered = False  # já disparamos a troca?
    sharingan_start = 0  # hora em que trocamos o mapa
    raikiri_start = 0
    drucao_mapa3_ms = 20000  # 20 000 ms = 20 segundos (ajuste para 15000 se quiser 15 s)
    raikiri_anim_rate_fast = max(1, frame_rates['sharingan'] // 2)  # animação 2× mais rápida
    raikiri_move_speed_slow = 25  # pixels por tick (menor que 8)


    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()


        # Determina símbolo de entrada
        entrada = None
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if state not in (
                State.JUMP, State.JUMP_LEFT,
                State.ATTACK, State.ATTACK_LEFT,
                State.ATTACK_CROUCH, State.ATTACK_CROUCH_LEFT,
                State.ATTACK_RUN, State.ATTACK_RUN_LEFT
        ):
            if keys[pygame.K_SPACE]:
                entrada, jump_timer = 'SPACE', jump_duration
            elif keys[pygame.K_p]:
                entrada = 'P'
            elif keys[pygame.K_u]:
                entrada = 'U'
            elif keys[pygame.K_m]:
                entrada = 'M'
            elif keys[pygame.K_j] and not sharingan_triggered:
                entrada = 'J'
            elif keys[pygame.K_h]:
                entrada = 'H'
            elif keys[pygame.K_r] and keys[pygame.K_t]:
                entrada = 'R+T'
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                entrada = 'S+A'
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                entrada = 'S+D'
            elif keys[pygame.K_s]:
                entrada = 'S'
            elif shift and keys[pygame.K_a]:
                entrada = 'SHIFT+A'
            elif shift and keys[pygame.K_d]:
                entrada = 'SHIFT+D'
            elif keys[pygame.K_a]:
                entrada = 'A'
            elif keys[pygame.K_d]:
                entrada = 'D'

        # Atualiza estado (δ)
        prev = state
        state = transitions.get((state, entrada),
                                 transitions.get((state, None), State.IDLE))
        if state != prev:
            frame_index = 0
            tick = 0

        # Atualiza frame
        rate = (
            frame_rates['attack'] if state in (State.ATTACK, State.ATTACK_LEFT) else
            frame_rates['crouch_attack'] if state in (State.ATTACK_CROUCH, State.ATTACK_CROUCH_LEFT) else
            frame_rates['run_attack'] if state in (State.ATTACK_RUN, State.ATTACK_RUN_LEFT) else
            frame_rates['up_attack'] if state in (State.ATTACK_UP, State.ATTACK_UP_LEFT) else
            frame_rates['sharingan'] if state in (State.SHARINGAN, State.SHARINGAN_LEFT) else
            frame_rates['default']
        )
        if tick % rate == 0 and state not in (State.RAIKIRI, State.RAIKIRI_LEFT):
            if state in (State.ATTACK_RUN, State.ATTACK_RUN_LEFT):
                if frame_index + 1 < len(frames[state]):
                    frame_index += 1
                else:
                    # ao fim do ataque correndo, volta a correr
                    state = State.RUN_RIGHT if state == State.ATTACK_RUN else State.RUN_LEFT
                    frame_index = 0
                    tick = 0

            elif state in (State.ATTACK_UP, State.ATTACK_UP_LEFT):
                if frame_index + 1 < len(frames[state]):
                    frame_index += 1
                else:
                    state = State.IDLE if state == State.ATTACK_UP else State.IDLE_LEFT
                    frame_index, tick = 0, 0
            elif state in (State.NINDOG_RIGHT, State.NINDOG_LEFT):
                total = len(frames[state])  # 25
                # avança um frame a cada tick compatível com a sua taxa default:
                if tick % frame_rates['sharingan'] == 0:
                    frame_index += 1
                # quando passar do último, volta ao idle correspondente
                if frame_index >= total:
                    state = State.IDLE if state == State.NINDOG_RIGHT else State.IDLE_LEFT
                    frame_index = 0
                    tick = 0
            elif state in (State.CROUCH, State.CROUCH_LEFT):
                frame_index = min(frame_index + 1, len(frames[state]) - 1)
            elif state in (State.ATTACK, State.ATTACK_LEFT):
                # avança somente se houver próximo frame, senão retorna a idle
                if frame_index + 1 < len(frames[state]):
                    frame_index += 1
                else:
                    state = State.IDLE if state == State.ATTACK else State.IDLE_LEFT
                    frame_index = 0
                    tick = 0
            elif state in (State.SHARINGAN, State.SHARINGAN_LEFT):
                # se estiver nos quadros 19,20 ou 21, aplica o SLOW_FACTOR
                if frame_index == 18:
                    current_rate = frame_rates['sharingan'] * 35
                elif frame_index == 19:
                    current_rate = frame_rates['sharingan']
                elif frame_index in (20,21):
                    current_rate = frame_rates['sharingan'] * 70
                else:
                    current_rate = frame_rates['sharingan']

                if tick % current_rate == 0:
                    frame_index += 1
                    # quando acabar a animação, volta a idle
                    if frame_index >= len(frames[state]):
                        state = State.IDLE if state == State.SHARINGAN else State.IDLE_LEFT
                        frame_index = tick = 0
            elif state in (State.WIN, State.WIN_LEFT):
                if frame_index + 1 < len(frames[state]):
                    if tick % frame_rates['default'] == 0:
                        frame_index += 1
                else:
                    pygame.time.delay(1000)
                    pygame.quit()
                    sys.exit()
            elif state in (State.ATTACK_CROUCH, State.ATTACK_CROUCH_LEFT):
                # avança somente se houver próximo frame, senão retorna ao crouch
                if frame_index + 1 < len(frames[state]):
                    frame_index += 1
                else:
                    if state == State.ATTACK_CROUCH:
                        state = State.CROUCH
                        frame_index = len(frames[State.CROUCH]) - 1
                    else:
                        state = State.CROUCH_LEFT
                        frame_index = len(frames[State.CROUCH_LEFT]) - 1
                    tick = 0
            else:
                # outras animações ciclam normalmente
                frame_index = (frame_index + 1) % len(frames[state])

        # garantia extra: nunca saia dos limites
        frame_index = max(0, min(frame_index, len(frames[state]) - 1))




        # Física do pulo e movimento
        jump_offset = 0
        if state in (State.JUMP, State.JUMP_LEFT):
            if jump_timer > 0:
                prog = 1 - (jump_timer / jump_duration)
                jump_offset = -math.sin(prog * math.pi) * jump_height
                jump_timer -= 1
                # Flipping de direção no ar
                if keys[pygame.K_a] and state == State.JUMP:
                    state = State.JUMP_LEFT
                elif keys[pygame.K_d] and state == State.JUMP_LEFT:
                    state = State.JUMP
                # Movimento horizontal no ar
                if shift and keys[pygame.K_a]:
                    x_pos -= run_speed
                elif shift and keys[pygame.K_d]:
                    x_pos += run_speed
                elif keys[pygame.K_a]:
                    x_pos -= walk_speed
                elif keys[pygame.K_d]:
                    x_pos += walk_speed
            else:
                state = State.IDLE if state == State.JUMP else State.IDLE_LEFT
                frame_index = tick = 0
        elif state in (State.RAIKIRI, State.RAIKIRI_LEFT):
            # 1) marca início e toca som apenas uma vez
            if frame_index == 0 and raikiri_start == 0:
                raikiri_start = pygame.time.get_ticks()
                sound_raikiri.play()

            now = pygame.time.get_ticks()
            elapsed = now - raikiri_start

            # 2) primeiros 11 frames em 3 segundos
            if frame_index < 11:
                frame_index = min(int((elapsed / 3000) * 11), 11)

                # animação rápida depois do 11
            elif tick % raikiri_anim_rate_fast == 0:
                frame_index += 1

                # movimento reduzido (mas animação mais rápida) a partir do 11
            if frame_index >= 11:
                if state == State.RAIKIRI:
                    x_pos += raikiri_move_speed_slow
                else:
                    x_pos -= raikiri_move_speed_slow

                # final da animação…
            if frame_index >= len(frames[state]):
                state = State.IDLE if state == State.RAIKIRI else State.IDLE_LEFT
                frame_index = tick = 0
                raikiri_start = 0
        else:
            # Movimento no chão
            if state == State.WALK_RIGHT:
                x_pos += walk_speed
            elif state == State.WALK_LEFT:
                x_pos -= walk_speed
            elif state == State.RUN_RIGHT:
                x_pos += run_speed
            elif state == State.RUN_LEFT:
                x_pos -= run_speed
            elif state == State.CROUCH_WALK:
                x_pos += crouch_walk_speed
            elif state == State.CROUCH_WALK_LEFT:
                x_pos -= crouch_walk_speed

        # Manter dentro da tela
        x_pos = max(0, min(x_pos, screen.get_width()))

        # —————— lógica de troca de mapa no Sharingan ——————
        # se estou em SHARINGAN e atingi o frame 19 e ainda não troquei
        if state in (State.SHARINGAN, State.SHARINGAN_LEFT) and frame_index == 19 and not sharingan_triggered:
            sharingan_triggered = True
            sound_sharingan.play()
            sharingan_start = pygame.time.get_ticks()


        # enquanto durar o periodo, mantenho mapa3
        if sharingan_triggered:
            if pygame.time.get_ticks() - sharingan_start <= drucao_mapa3_ms:
                current_background = mapa3
            else:
                # volta ao original após expirar
                current_background = orig_background
                sharingan_triggered = False
        else:
            # se não estiver numa sessão de Sharingan ativa, garanto o fundo normal
            current_background = orig_background

        # Desenho final
        screen.blit(current_background, (0, 0))

        if state in (State.SHARINGAN, State.SHARINGAN_LEFT):
            total = len(frames[state])

            # Se estiver no frame 19 (índice 18, já que começa em 0)
            if frame_index == 18:
                now = pygame.time.get_ticks()
                if fade_start == 0:
                    fade_start = now
                elapsed = now - fade_start
                # calcula alpha entre 0 e 255
                alpha = min(255, int((elapsed / fade_duration) * 255))
                surf = frames[state][frame_index].copy()
                surf.set_alpha(alpha)
            else:
                # fora do fade, desenha normalmente e reseta fade_start
                surf = frames[state][frame_index]
                fade_start = 0

            # se for um dos 3 últimos frames, desenha full-screen
            if frame_index >= total - 3:
                full = pygame.transform.scale(surf, screen.get_size())
                screen.blit(full, (0, 0))
            else:
                rect = surf.get_rect(midbottom=(x_pos, y_pos + jump_offset))
                screen.blit(surf, rect)
        else:
            surf = frames[state][frame_index]
            rect = surf.get_rect(midbottom=(x_pos, y_pos + jump_offset))
            screen.blit(surf, rect)

        pygame.display.flip()

        tick += 1
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    main()