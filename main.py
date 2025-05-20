import pygame
import os
import math

# Inicialização do Pygame
def init_pygame(width=800, height=600):
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
stand_folder         = os.path.join(base, 'Sprite', 'stand')
stand_left_folder    = os.path.join(stand_folder, 'espelhadas')
walk_r_folder        = os.path.join(base, 'Sprite', 'walk')
walk_l_folder        = os.path.join(walk_r_folder, 'espelhadas')
run_r_folder         = os.path.join(base, 'Sprite', 'run')
run_l_folder         = os.path.join(run_r_folder, 'espelhadas')
crouch_folder        = os.path.join(base, 'Sprite', 'crouch')
crouch_left_folder   = os.path.join(crouch_folder, 'espelhadas')
crouch_walk_folder   = os.path.join(base, 'Sprite', 'crouchWalk')
crouch_walk_left     = os.path.join(crouch_walk_folder, 'espelhadas')
jump_r_folder = os.path.join(base, 'Sprite', 'jump')
jump_l_folder = os.path.join(jump_r_folder, 'espelhadas')

# Definição do autômato (AFD) com transições de crouch e crouch_walk
AFD = {
    'idle': {
    'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', 'SHIFT+D': 'run_right',
    'S': 'crouch', 'S+A': 'crouch_walk_left', 'S+D': 'crouch_walk', 'SPACE': 'jump', '': 'idle'
    },
    'idle_left': {
        'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', 'SHIFT+D': 'run_right',
        'S': 'crouch_left', 'S+A': 'crouch_walk_left', 'S+D': 'crouch_walk', 'SPACE': 'jump_left', '': 'idle_left'
    },
    'jump': {
        '': 'jump'
    },
    'jump_left': {
        '': 'jump_left'
    },
    'walk_left': {
        'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', 'S': 'crouch_left', '': 'idle_left','SPACE': 'jump_left',
    },
    'walk_right': {
        'D': 'walk_right', 'A': 'walk_left', 'SHIFT+D': 'run_right', 'S': 'crouch', '': 'idle','SPACE': 'jump',
    },
    'run_left': {
        'SHIFT+A': 'run_left', 'A': 'walk_left', 'D': 'walk_right', 'S': 'crouch_left', '': 'idle_left','SPACE': 'jump_left',
    },
    'run_right': {
        'SHIFT+D': 'run_right', 'D': 'walk_right', 'A': 'walk_left', 'S': 'crouch', '': 'idle','SPACE': 'jump',
    },
    'crouch': {
        'S': 'crouch', 'S+A': 'crouch_walk_left', 'S+D': 'crouch_walk', '': 'idle', 'SPACE': 'jump',
    },
    'crouch_left': {
        'S': 'crouch_left', 'S+A': 'crouch_walk_left', 'S+D': 'crouch_walk', '': 'idle_left' ,'SPACE': 'jump_left',
    },
    'crouch_walk': {
        'S+D': 'crouch_walk', 'S+A': 'crouch_walk_left', 'S': 'crouch', '': 'crouch', 'SPACE': 'jump',
    },
    'crouch_walk_left': {
        'S+A': 'crouch_walk_left', 'S+D': 'crouch_walk', 'S': 'crouch_left', '': 'crouch_left','SPACE': 'jump_left',
    }
}

# Velocidade de deslocamento ao andar agachado
crouch_walk_speed = 0.8

# Função principal
def main():
    screen, clock = init_pygame()
    # Carregar frames de cada estado
    frames = {
        'idle':             load_frames(stand_folder,         'stand',     6),
        'idle_left':        load_frames(stand_left_folder,    'stand',     6),
        'walk_right':       load_frames(walk_r_folder,        'walk',      6),
        'walk_left':        load_frames(walk_l_folder,        'walk',      6),
        'run_right':        load_frames(run_r_folder,         'run',       6),
        'run_left':         load_frames(run_l_folder,         'run',       6),
        'crouch':           load_frames(crouch_folder,        'crouch',    2),
        'crouch_left':      load_frames(crouch_left_folder,   'crouch',    2),
        'crouch_walk':      load_frames(crouch_walk_folder,   'crouchWalk',6),
        'crouch_walk_left': load_frames(crouch_walk_left,     'crouchWalk',6),
        'jump': load_frames(jump_r_folder, 'jump', 4),
        'jump_left': load_frames(jump_l_folder, 'jump', 4),
    }

    frame_rate = 10
    estado_atual = 'idle'
    frame_index = 0
    tick = 0
    x_pos = screen.get_width() // 2
    y_pos = screen.get_height() // 2 + 100
    walk_speed = 1.5
    run_speed = 3.5
    running = True
    jump_height = 200
    jump_duration = 40  # frames

    jump_timer = 0

    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        # 1) Captura de entrada (prioritário: SPACE, depois S combos, SHIFT, A/D)
        entrada = ''
        if estado_atual not in ('jump', 'jump_left'):
            shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            if keys[pygame.K_SPACE]:
                entrada = 'SPACE'
                jump_timer = jump_duration
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

        # 2) Atualiza estado e reseta animação se mudou
        prev = estado_atual
        estado_atual = AFD[estado_atual].get(entrada, 'idle')
        if estado_atual != prev:
            frame_index = 0
            tick = 0

        # 3) Atualiza índice de frame (animação)
        if tick % frame_rate == 0:
            if estado_atual in ('crouch', 'crouch_left'):
                frame_index = min(frame_index + 1, len(frames[estado_atual]) - 1)
            elif estado_atual in ('jump', 'jump_left'):
                # a animação de pulo é guiada por jump_timer, mas ainda precisa setar frame_index
                progress = 1 - (jump_timer / jump_duration)
                frame_index = min(int(progress * len(frames[estado_atual])), len(frames[estado_atual]) - 1)
            else:
                frame_index = (frame_index + 1) % len(frames[estado_atual])

        # PREPARA jump_offset
        jump_offset = 0

        # ─── Movimento no solo ───
        if estado_atual == 'walk_right':
            x_pos += walk_speed
        elif estado_atual == 'walk_left':
            x_pos -= walk_speed
        elif estado_atual == 'run_right':
            x_pos += run_speed
        elif estado_atual == 'run_left':
            x_pos -= run_speed
        elif estado_atual == 'crouch_walk':
            x_pos += crouch_walk_speed
        elif estado_atual == 'crouch_walk_left':
            x_pos -= crouch_walk_speed

        # ─── Física do salto ───
        if estado_atual in ('jump', 'jump_left'):
            if jump_timer > 0:
                progress = 1 - (jump_timer / jump_duration)
                jump_offset = -math.sin(progress * math.pi) * jump_height
                jump_timer -= 1
            else:
                # fim do salto, volta ao idle correspondente
                estado_atual = 'idle' if estado_atual == 'jump' else 'idle_left'
                frame_index = 0
                tick = 0

        # ─── Movimento horizontal no ar ───
        if estado_atual in ('jump', 'jump_left'):
            shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            # correr no ar
            if shift and keys[pygame.K_a]:
                x_pos -= run_speed
            elif shift and keys[pygame.K_d]:
                x_pos += run_speed
            # andar no ar
            elif keys[pygame.K_a]:
                x_pos -= walk_speed
            elif keys[pygame.K_d]:
                x_pos += walk_speed

        # ─── Troca sprite de salto no ar se inverter direção ───
        if estado_atual in ('jump', 'jump_left'):
            if keys[pygame.K_a] and estado_atual == 'jump':
                estado_atual = 'jump_left'
            # deixa frame_index como está, só inverte o lado
            elif keys[pygame.K_d] and estado_atual == 'jump_left':
                estado_atual = 'jump'
            # idem, continua no frame atual

        # Clamp em X
        x_pos = max(0, min(x_pos, screen.get_width()))

        # Desenho
        frame = frames[estado_atual][frame_index]
        rect = frame.get_rect(midbottom=(x_pos, y_pos + jump_offset))
        screen.fill((30, 30, 30))
        screen.blit(frame, rect)
        pygame.display.flip()

        # Incrementa tick e controla FPS
        tick += 1
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()
