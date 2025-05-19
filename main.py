import pygame
import os

def init_pygame(width=800, height=600):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AFD - Animação Personagem")
    clock = pygame.time.Clock()
    return screen, clock

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def load_frames(folder, prefix, count):
    frames = []
    max_w = max_h = 0
    raw = []

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

# Diretórios
base = os.path.dirname(__file__)
stand_folder      = os.path.join(base, 'Sprite', 'stand')
stand_left_folder = os.path.join(stand_folder, 'espelhadas')
walk_r_folder     = os.path.join(base, 'Sprite', 'walk')
walk_l_folder     = os.path.join(walk_r_folder, 'espelhadas')
run_r_folder      = os.path.join(base, 'Sprite', 'run')
run_l_folder      = os.path.join(run_r_folder, 'espelhadas')

# Autômato com corrida
AFD = {
    'idle':        {'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', 'SHIFT+D': 'run_right', '': 'idle'},
    'idle_left':   {'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', 'SHIFT+D': 'run_right', '': 'idle_left'},
    'walk_left':   {'A': 'walk_left', 'D': 'walk_right', 'SHIFT+A': 'run_left', '': 'idle_left'},
    'walk_right':  {'D': 'walk_right', 'A': 'walk_left', 'SHIFT+D': 'run_right', '': 'idle'},
    'run_left':    {'SHIFT+A': 'run_left', 'A': 'walk_left', 'D': 'walk_right', '': 'idle_left'},
    'run_right':   {'SHIFT+D': 'run_right', 'D': 'walk_right', 'A': 'walk_left', '': 'idle'}
}

def main():
    screen, clock = init_pygame()

    # Carregamento de sprites
    frames = {
        'idle':        load_frames(stand_folder,      'stand', 6),
        'idle_left':   load_frames(stand_left_folder, 'stand', 6),
        'walk_right':  load_frames(walk_r_folder,     'walk',  6),
        'walk_left':   load_frames(walk_l_folder,     'walk',  6),
        'run_right':   load_frames(run_r_folder,      'run',   6),
        'run_left':    load_frames(run_l_folder,      'run',   6),
    }

    frame_rate = 10
    estado_atual = 'idle'
    frame_index = 0
    tick = 0
    x_pos = screen.get_width() // 2
    y_pos = screen.get_height() // 2 + 100

    # Velocidades
    walk_speed = 1.5
    run_speed = 3.5

    running = True
    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if shift and keys[pygame.K_a]:
            entrada = 'SHIFT+A'
        elif shift and keys[pygame.K_d]:
            entrada = 'SHIFT+D'
        elif keys[pygame.K_a]:
            entrada = 'A'
        elif keys[pygame.K_d]:
            entrada = 'D'
        else:
            entrada = ''

        estado_atual = AFD[estado_atual].get(entrada, 'idle')

        # Frame da animação
        if tick % frame_rate == 0:
            frame_index = (frame_index + 1) % len(frames[estado_atual])

        # Movimento
        if estado_atual == 'walk_right':
            x_pos += walk_speed
        elif estado_atual == 'walk_left':
            x_pos -= walk_speed
        elif estado_atual == 'run_right':
            x_pos += run_speed
        elif estado_atual == 'run_left':
            x_pos -= run_speed

        # Limite de tela
        x_pos = max(0, min(x_pos, screen.get_width()))

        # Desenho
        frame = frames[estado_atual][frame_index]
        rect = frame.get_rect(midbottom=(x_pos, y_pos))

        screen.fill((30, 30, 30))
        screen.blit(frame, rect)
        pygame.display.flip()

        tick += 1
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()
