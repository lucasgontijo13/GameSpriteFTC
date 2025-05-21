import pygame
import os
import math
from enum import Enum, auto

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
    (State.IDLE,      None): State.IDLE,

    (State.IDLE_LEFT, 'A'): State.WALK_LEFT,
    (State.IDLE_LEFT, 'D'): State.WALK_RIGHT,
    (State.IDLE_LEFT, 'SHIFT+A'): State.RUN_LEFT,
    (State.IDLE_LEFT, 'SHIFT+D'): State.RUN_RIGHT,
    (State.IDLE_LEFT, 'S'): State.CROUCH_LEFT,
    (State.IDLE_LEFT, 'S+A'): State.CROUCH_WALK_LEFT,
    (State.IDLE_LEFT, 'S+D'): State.CROUCH_WALK,
    (State.IDLE_LEFT, 'SPACE'): State.JUMP_LEFT,
    (State.IDLE_LEFT, None): State.IDLE_LEFT,

    (State.WALK_RIGHT, 'D'): State.WALK_RIGHT,
    (State.WALK_RIGHT, 'A'): State.WALK_LEFT,
    (State.WALK_RIGHT, 'SHIFT+D'): State.RUN_RIGHT,
    (State.WALK_RIGHT, 'S'): State.CROUCH,
    (State.WALK_RIGHT, 'SPACE'): State.JUMP,
    (State.WALK_RIGHT, None): State.IDLE,

    (State.WALK_LEFT,  'A'): State.WALK_LEFT,
    (State.WALK_LEFT,  'D'): State.WALK_RIGHT,
    (State.WALK_LEFT,  'SHIFT+A'): State.RUN_LEFT,
    (State.WALK_LEFT,  'S'): State.CROUCH_LEFT,
    (State.WALK_LEFT,  'SPACE'): State.JUMP_LEFT,
    (State.WALK_LEFT,  None): State.IDLE_LEFT,

    (State.RUN_RIGHT,  'SHIFT+D'): State.RUN_RIGHT,
    (State.RUN_RIGHT,  'D'): State.WALK_RIGHT,
    (State.RUN_RIGHT,  'A'): State.WALK_LEFT,
    (State.RUN_RIGHT,  'S'): State.CROUCH,
    (State.RUN_RIGHT,  'SPACE'): State.JUMP,
    (State.RUN_RIGHT,  None): State.IDLE,

    (State.RUN_LEFT,   'SHIFT+A'): State.RUN_LEFT,
    (State.RUN_LEFT,   'A'): State.WALK_LEFT,
    (State.RUN_LEFT,   'D'): State.WALK_RIGHT,
    (State.RUN_LEFT,   'S'): State.CROUCH_LEFT,
    (State.RUN_LEFT,   'SPACE'): State.JUMP_LEFT,
    (State.RUN_LEFT,   None): State.IDLE_LEFT,

    (State.CROUCH,     'S'): State.CROUCH,
    (State.CROUCH,     'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH,     'S+D'): State.CROUCH_WALK,
    (State.CROUCH,     'SPACE'): State.JUMP,
    (State.CROUCH,     None): State.IDLE,

    (State.CROUCH_LEFT,'S'): State.CROUCH_LEFT,
    (State.CROUCH_LEFT,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_LEFT,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_LEFT,'SPACE'): State.JUMP_LEFT,
    (State.CROUCH_LEFT, None): State.IDLE_LEFT,

    (State.CROUCH_WALK,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_WALK,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_WALK,'S'): State.CROUCH,
    (State.CROUCH_WALK,'SPACE'): State.JUMP,
    (State.CROUCH_WALK, None): State.CROUCH,

    (State.CROUCH_WALK_LEFT,'S+A'): State.CROUCH_WALK_LEFT,
    (State.CROUCH_WALK_LEFT,'S+D'): State.CROUCH_WALK,
    (State.CROUCH_WALK_LEFT,'S'): State.CROUCH_LEFT,
    (State.CROUCH_WALK_LEFT,'SPACE'): State.JUMP_LEFT,
    (State.CROUCH_WALK_LEFT, None): State.CROUCH_LEFT,

    # Durante o pulo, mantemos o estado (permitiremos movimentos manuais)
    (State.JUMP,       None): State.JUMP,
    (State.JUMP_LEFT,  None): State.JUMP_LEFT,
}

def init_pygame(width=600, height=350):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AFD - Animação Personagem")
    clock = pygame.time.Clock()
    return screen, clock

# Carrega imagem com canal alpha
def load_image(path):
    return pygame.image.load(path).convert_alpha()

# Carrega sequência de frames a partir de pasta, prefixo e quantidade
def load_frames(folder, prefix, count):
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

# Parâmetros
crouch_walk_speed = 0.8
walk_speed = 1.5
run_speed = 3.5
jump_height = 200
jump_duration = 40  # frames
frame_rate = 10      # atualização de frame de animação

# Função principal
def main():
    screen, clock = init_pygame()
    background = pygame.image.load(os.path.join(base, 'Mapa', 'mapa2.jpg')).convert()
    background = pygame.transform.scale(background, screen.get_size())

    frames = {
        State.IDLE:             load_frames(stand_folder, 'stand', 6),
        State.IDLE_LEFT:        load_frames(stand_left_folder, 'stand', 6),
        State.WALK_RIGHT:       load_frames(walk_r_folder, 'walk', 6),
        State.WALK_LEFT:        load_frames(walk_l_folder, 'walk', 6),
        State.RUN_RIGHT:        load_frames(run_r_folder, 'run', 6),
        State.RUN_LEFT:         load_frames(run_l_folder, 'run', 6),
        State.CROUCH:           load_frames(crouch_folder, 'crouch', 2),
        State.CROUCH_LEFT:      load_frames(crouch_left_folder, 'crouch', 2),
        State.CROUCH_WALK:      load_frames(crouch_walk_folder, 'crouchWalk', 6),
        State.CROUCH_WALK_LEFT: load_frames(crouch_walk_left, 'crouchWalk', 6),
        State.JUMP:             load_frames(jump_r_folder, 'jump', 4),
        State.JUMP_LEFT:        load_frames(jump_l_folder, 'jump', 4),
    }

    state = State.IDLE
    frame_index = 0
    tick = 0
    x_pos = screen.get_width() // 2
    y_pos = screen.get_height() - 50
    jump_timer = 0
    running = True

    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        # Determina símbolo de entrada
        entrada = None
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if state not in (State.JUMP, State.JUMP_LEFT):
            if keys[pygame.K_SPACE]:
                entrada = 'SPACE'
                jump_timer = jump_duration
            elif keys[pygame.K_s] and keys[pygame.K_a]: entrada = 'S+A'
            elif keys[pygame.K_s] and keys[pygame.K_d]: entrada = 'S+D'
            elif keys[pygame.K_s]: entrada = 'S'
            elif shift and keys[pygame.K_a]: entrada = 'SHIFT+A'
            elif shift and keys[pygame.K_d]: entrada = 'SHIFT+D'
            elif keys[pygame.K_a]: entrada = 'A'
            elif keys[pygame.K_d]: entrada = 'D'

        # Atualiza estado (δ)
        prev = state
        state = transitions.get((state, entrada),
                                 transitions.get((state, None), State.IDLE))
        if state != prev:
            frame_index = 0
            tick = 0

        # Atualiza frame
        if tick % frame_rate == 0:
            if state in (State.CROUCH, State.CROUCH_LEFT):
                frame_index = min(frame_index + 1, len(frames[state]) - 1)
            elif state in (State.JUMP, State.JUMP_LEFT):
                progress = 1 - (jump_timer / jump_duration)
                frame_index = min(int(progress * len(frames[state])), len(frames[state]) - 1)
            else:
                frame_index = (frame_index + 1) % len(frames[state])

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

        # Desenho final
        screen.blit(background, (0, 0))
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