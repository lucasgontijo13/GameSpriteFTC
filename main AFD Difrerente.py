import pygame
import os
from enum import Enum, auto

# Definição de estados do AFD
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

# Definição de símbolos de entrada
class Symbol(Enum):
    A = auto()
    D = auto()
    SHIFT_A = auto()
    SHIFT_D = auto()
    S = auto()
    S_A = auto()
    S_D = auto()
    NONE = auto()

# Função de transição T: State x Symbol -> State
TRANSITION = {
    State.IDLE: {
        Symbol.A: State.WALK_LEFT,
        Symbol.D: State.WALK_RIGHT,
        Symbol.SHIFT_A: State.RUN_LEFT,
        Symbol.SHIFT_D: State.RUN_RIGHT,
        Symbol.S: State.CROUCH,
        Symbol.S_A: State.CROUCH_WALK_LEFT,
        Symbol.S_D: State.CROUCH_WALK,
        Symbol.NONE: State.IDLE
    },
    State.IDLE_LEFT: {
        Symbol.A: State.WALK_LEFT,
        Symbol.D: State.WALK_RIGHT,
        Symbol.SHIFT_A: State.RUN_LEFT,
        Symbol.SHIFT_D: State.RUN_RIGHT,
        Symbol.S: State.CROUCH_LEFT,
        Symbol.S_A: State.CROUCH_WALK_LEFT,
        Symbol.S_D: State.CROUCH_WALK,
        Symbol.NONE: State.IDLE_LEFT
    },
    State.WALK_RIGHT: {
        Symbol.D: State.WALK_RIGHT,
        Symbol.A: State.WALK_LEFT,
        Symbol.SHIFT_D: State.RUN_RIGHT,
        Symbol.S: State.CROUCH,
        Symbol.NONE: State.IDLE
    },
    State.WALK_LEFT: {
        Symbol.A: State.WALK_LEFT,
        Symbol.D: State.WALK_RIGHT,
        Symbol.SHIFT_A: State.RUN_LEFT,
        Symbol.S: State.CROUCH_LEFT,
        Symbol.NONE: State.IDLE_LEFT
    },
    State.RUN_RIGHT: {
        Symbol.SHIFT_D: State.RUN_RIGHT,
        Symbol.D: State.WALK_RIGHT,
        Symbol.A: State.WALK_LEFT,
        Symbol.S: State.CROUCH,
        Symbol.NONE: State.IDLE
    },
    State.RUN_LEFT: {
        Symbol.SHIFT_A: State.RUN_LEFT,
        Symbol.A: State.WALK_LEFT,
        Symbol.D: State.WALK_RIGHT,
        Symbol.S: State.CROUCH_LEFT,
        Symbol.NONE: State.IDLE_LEFT
    },
    State.CROUCH: {
        Symbol.S: State.CROUCH,
        Symbol.S_A: State.CROUCH_WALK_LEFT,
        Symbol.S_D: State.CROUCH_WALK,
        Symbol.NONE: State.CROUCH
    },
    State.CROUCH_LEFT: {
        Symbol.S: State.CROUCH_LEFT,
        Symbol.S_A: State.CROUCH_WALK_LEFT,
        Symbol.S_D: State.CROUCH_WALK,
        Symbol.NONE: State.CROUCH_LEFT
    },
    State.CROUCH_WALK: {
        Symbol.S_D: State.CROUCH_WALK,
        Symbol.S: State.CROUCH,
        Symbol.NONE: State.CROUCH
    },
    State.CROUCH_WALK_LEFT: {
        Symbol.S_A: State.CROUCH_WALK_LEFT,
        Symbol.S: State.CROUCH_LEFT,
        Symbol.NONE: State.CROUCH_LEFT
    }
}

# Carregamento de frames
def load_image(path):
    return pygame.image.load(path).convert_alpha()

def load_frames(folder, prefix, count):
    frames = []
    raw = []
    max_w = max_h = 0
    for i in range(1, count+1):
        img = load_image(os.path.join(folder, f"{prefix}-{i}.png"))
        rect = img.get_bounding_rect()
        raw.append((img, rect))
        max_w = max(max_w, rect.width)
        max_h = max(max_h, rect.height)
    for img, rect in raw:
        surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        dest = rect.copy()
        dest.midbottom = (max_w//2, max_h)
        surf.blit(img, dest.topleft, rect)
        frames.append(surf)
    return frames

# Captura símbolo corrente baseado em teclas
def get_symbol(keys):
    if keys[pygame.K_s] and keys[pygame.K_a]: return Symbol.S_A
    if keys[pygame.K_s] and keys[pygame.K_d]: return Symbol.S_D
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_a]: return Symbol.SHIFT_A
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_d]: return Symbol.SHIFT_D
    if keys[pygame.K_s]: return Symbol.S
    if keys[pygame.K_a]: return Symbol.A
    if keys[pygame.K_d]: return Symbol.D
    return Symbol.NONE

# Define velocidade por estado
SPEED = {
    State.WALK_RIGHT: 1.5,
    State.WALK_LEFT: -1.5,
    State.RUN_RIGHT: 3.5,
    State.RUN_LEFT: -3.5,
    State.CROUCH_WALK: 0.8,
    State.CROUCH_WALK_LEFT: -0.8
}

# Função principal
if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    base = os.path.dirname(__file__)

    # Agora que display está inicializado, carregue as animações
    ANIMATIONS = {
        State.IDLE: load_frames(os.path.join(base,'Sprite','stand'),'stand',6),
        State.IDLE_LEFT: load_frames(os.path.join(base,'Sprite','stand','espelhadas'),'stand',6),
        State.WALK_RIGHT: load_frames(os.path.join(base,'Sprite','walk'),'walk',6),
        State.WALK_LEFT: load_frames(os.path.join(base,'Sprite','walk','espelhadas'),'walk',6),
        State.RUN_RIGHT: load_frames(os.path.join(base,'Sprite','run'),'run',6),
        State.RUN_LEFT: load_frames(os.path.join(base,'Sprite','run','espelhadas'),'run',6),
        State.CROUCH: load_frames(os.path.join(base,'Sprite','crouch'),'crouch',2),
        State.CROUCH_LEFT: load_frames(os.path.join(base,'Sprite','crouch','espelhadas'),'crouch',2),
        State.CROUCH_WALK: load_frames(os.path.join(base,'Sprite','crouchWalk'),'crouchWalk',6),
        State.CROUCH_WALK_LEFT: load_frames(os.path.join(base,'Sprite','crouchWalk','espelhadas'),'crouchWalk',6)
    }

    pos_x, pos_y = 400, 350
    current_state = State.IDLE
    frame_idx, tick = 0, 0
    running = True

    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        symbol = get_symbol(keys)
        next_st = TRANSITION[current_state].get(symbol, State.IDLE)
        if next_st != current_state:
            current_state, frame_idx, tick = next_st, 0, 0

        if tick % 10 == 0:
            frames = ANIMATIONS[current_state]
            if current_state in (State.CROUCH, State.CROUCH_LEFT):
                frame_idx = min(frame_idx+1, len(frames)-1)
            else:
                frame_idx = (frame_idx+1) % len(frames)

        # Movimento e limite
        pos_x += SPEED.get(current_state, 0)
        pos_x = max(0, min(pos_x, 800))

        # Renderização
        screen.fill((30,30,30))
        frame = ANIMATIONS[current_state][frame_idx]
        rect = frame.get_rect(midbottom=(pos_x,pos_y))
        screen.blit(frame, rect)
        pygame.display.flip()

        tick += 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        clock.tick(60)
    pygame.quit()

if __name__=='__main__':
    main()