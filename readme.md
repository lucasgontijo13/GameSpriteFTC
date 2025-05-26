# AFD - Animação de Personagem (Pygame)

Este projeto demonstra a implementação de um Autômato Finito Determinístico (AFD) para controlar as animações e o estado de um personagem em Pygame. O personagem pode andar, correr, agachar, pular, e executar diversas ações como ataques e habilidades especiais, todas controladas por transições de estado bem definidas.

-----
## Requisitos

Para rodar este projeto, você precisará ter o **Python** instalado em sua máquina, juntamente com a biblioteca **Pygame**.

* **Python 3.x**
* **Pygame**: Você pode instalá-lo via pip:
    ```bash
    pip install pygame
    ```

---

## Estrutura de Pastas

Certifique-se de que a estrutura de pastas do seu projeto esteja organizada da seguinte forma:

```
seu_projeto/
├── main.py
├── Sprite/
│   ├── attack/
│   │   ├── attack1-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── attack1-1.png
│   │       └── ...
│   ├── attackCombo/
│   │   ├── attack(crouch)-1.png
│   │   ├── ...
│   │   ├── attack(run)-1.png
│   │   ├── ...
│   │   ├── attack(up)-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── attack(crouch)-1.png
│   │       ├── ...
│   │       ├── attack(run)-1.png
│   │       ├── ...
│   │       ├── attack(up)-1.png
│   │       └── ...
│   ├── crouch/
│   │   ├── crouch-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── crouch-1.png
│   │       └── ...
│   ├── crouchWalk/
│   │   ├── crouchWalk-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── crouchWalk-1.png
│   │       └── ...
│   ├── jump/
│   │   ├── jump-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── jump-1.png
│   │       └── ...
│   ├── ninDogs/
│   │   ├── ninDogs-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── ninDogs-1.png
│   │       └── ...
│   ├── raikiri/
│   │   ├── raikiri-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── raikiri-1.png
│   │       └── ...
│   ├── run/
│   │   ├── run-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── run-1.png
│   │       └── ...
│   ├── sharingan/
│   │   ├── sharingan-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── sharingan-1.png
│   │       └── ...
│   ├── stand/
│   │   ├── stand-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── stand-1.png
│   │       └── ...
│   ├── walk/
│   │   ├── walk-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── walk-1.png
│   │       └── ...
│   ├── win/
│   │   ├── win-1.png
│   │   └── ...
│   │   └── espelhadas/
│   │       ├── win-1.png
│   │       └── ...
├── Sons/
│   ├── raikiri.mp3
│   └── sharingan.mp3
└── Mapa/
    ├── mapa3.jpg
    └── mapa4.jpg
```

**Importante:** A pasta `espelhadas` dentro de cada diretório de sprite deve conter as imagens espelhadas horizontalmente das animações, para representar o personagem virado para a esquerda.

---

## Como Rodar

1.  **Navegue até a pasta do projeto:** Abra o terminal ou prompt de comando e use o comando `cd` para ir até o diretório onde você salvou o arquivo `main.py`.
    ```bash
    cd caminho/para/seu/projeto
    ```
2.  **Execute o script:**
    ```bash
    python main.py
    ```
    O jogo será iniciado em tela cheia. Para sair, você pode esperar a animação de "vitória" terminar ou pressionar `Alt + F4` (Windows) / `Cmd + Q` (macOS).

---

## Descrição do Código

O código é estruturado para simular um Autômato Finito Determinístico (AFD) para as animações do personagem.

### 1. Importações

```python
import pygame # Biblioteca principal para o desenvolvimento de jogos.
import os     # Para manipulação de caminhos de arquivos (útil para carregar recursos).
import math   # Usado para cálculos matemáticos, como o arco do pulo.
from enum import Enum, auto # Para criar enumerações de estados de forma organizada.
import sys    # Para encerrar o programa.
```

### 2. Definições de Estado e Símbolo

```python
class State(Enum):
    IDLE = auto() # Estado parado, virado para a direita.
    IDLE_LEFT = auto() # Estado parado, virado para a esquerda.
    # ... (outros estados para andar, correr, agachar, pular, ataques, etc.)
    WIN = auto() # Estado de vitória.
    WIN_LEFT = auto() # Estado de vitória, virado para a esquerda.
    # ... (habilidades especiais)
```

* A classe `State` define todos os estados possíveis do personagem usando `Enum` e `auto()`. Isso torna o código mais legível e menos propenso a erros de digitação de strings.
* `Symbol = str`: Define que um símbolo de entrada é uma string, representando a tecla ou combinação de teclas pressionadas.

### 3. Tabela de Transições (δ)

```python
transitions: dict[tuple[State, Symbol], State] = {
    (State.IDLE,      'A'): State.WALK_LEFT, # Se estiver IDLE e apertar 'A', vai para WALK_LEFT.
    (State.IDLE,      'D'): State.WALK_RIGHT, # Se estiver IDLE e apertar 'D', vai para WALK_RIGHT.
    # ... (outras transições)
    (State.JUMP, None): State.JUMP, # Enquanto estiver pulando, mantém o estado de pulo.
    # ... (estados que "preservam" até que a animação termine ou outra condição seja atendida)
}
```

* Esta é a essência do AFD. O dicionário `transitions` mapeia uma tupla `(estado_atual, símbolo_de_entrada)` para o `próximo_estado`.
* `None` como símbolo de entrada representa a ausência de uma tecla específica pressionada, sendo usado para transições padrão (ex: de volta ao IDLE após parar de andar).
* Estados como `JUMP`, `RAIKIRI`, `ATTACK` e `SHARINGAN` são considerados estados "preservados" ou "atômicos" no AFD. Uma vez que o personagem entra neles, ele permanece neles até que a animação seja concluída ou uma condição específica seja atendida no loop principal, independentemente de outras entradas (exceto para mudanças de direção durante o pulo, que são tratadas separadamente).

### 4. Funções de Inicialização e Carregamento

```python
def init_pygame(width=1500, height=800):
    pygame.init() # Inicializa todos os módulos Pygame.
    pygame.mixer.init() # Inicializa o mixer de som.
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Cria uma tela em modo fullscreen.
    pygame.display.set_caption("AFD - Animação Personagem") # Define o título da janela.
    clock = pygame.time.Clock() # Cria um objeto Clock para controlar a taxa de quadros.
    return screen, clock

def load_image(path):
    return pygame.image.load(path).convert_alpha() # Carrega uma imagem e otimiza para transparência.

def load_frames(folder, prefix, count, scale=1.0):
    # Carrega uma sequência de imagens de uma pasta, ajusta seu tamanho
    # e as retorna como uma lista de superfícies Pygame.
    # Garante que todos os frames tenham o mesmo tamanho para fácil manipulação.
    # 'scale' permite redimensionar as animações.
```

* `init_pygame`: Configura a janela do Pygame, o mixer de áudio e o relógio.
* `load_image`: Uma função auxiliar para carregar imagens com transparência.
* `load_frames`: Esta função é crucial. Ela carrega todos os frames de uma animação, garante que todos tenham o mesmo tamanho (para centralização e alinhamento corretos) e aplica uma escala.

### 5. Configurações de Sprites e Parâmetros

```python
# Diretórios de sprites (caminhos para as pastas de imagens)
base = os.path.dirname(__file__) # Pega o diretório atual do script.
stand_folder = os.path.join(base, 'Sprite', 'stand') # Exemplo de caminho.
# ... (outros diretórios)

# Parâmetros de jogo
crouch_walk_speed = 1.6 # Velocidade ao andar agachado.
walk_speed = 3 # Velocidade ao andar.
run_speed = 10 # Velocidade ao correr.
jump_height = 400 # Altura máxima do pulo.
jump_duration = 50 # Duração do pulo em frames.
frame_rates = { # Dicionário para controlar a velocidade de cada animação.
    'default': 8,
    'attack': 4,
    # ...
}
```

* Define os caminhos para todas as pastas de sprites.
* Define velocidades de movimento, altura de pulo e taxas de quadros para diferentes animações, permitindo controlar a fluidez e a velocidade.

### 6. Função Principal (`main`)

```python
def main():
    screen, clock = init_pygame()
    # Carregamento de backgrounds
    background = pygame.image.load(os.path.join(base, 'Mapa', 'mapa4.jpg')).convert()
    background = pygame.transform.scale(background, screen.get_size())
    orig_background = background
    mapa3 = pygame.image.load(os.path.join(base, 'Mapa', 'mapa3.jpg')).convert()
    mapa3 = pygame.transform.scale(mapa3, screen.get_size())

    # Carregamento de sons
    sound_sharingan = pygame.mixer.Sound(os.path.join(base, 'Sons', 'sharingan.mp3'))
    sound_raikiri = pygame.mixer.Sound(os.path.join(base, 'Sons', 'raikiri.mp3'))
    sound_sharingan.set_volume(0.5)
    sound_raikiri.set_volume(0.5)

    scale = 4.0 # Fator de escala para todos os sprites.
    frames = { # Dicionário que armazena todas as animações (listas de superfícies Pygame)
        State.IDLE: load_frames(stand_folder, 'stand', 6, scale),
        # ...
    }

    state = State.IDLE # Estado inicial do personagem.
    frame_index = 0 # Índice do frame atual da animação.
    tick = 0 # Contador de ticks para controle de animação.
    x_pos = screen.get_width() // 2 # Posição X inicial do personagem.
    y_pos = screen.get_height() - 50 # Posição Y inicial do personagem (no chão).
    jump_timer = 0 # Contador para a duração do pulo.
    running = True # Flag para o loop principal do jogo.
    fade_duration = 300 # Duração do efeito de fade do Sharingan.
    fade_start = 0 # Tempo de início do fade.

    sharingan_triggered = False # Flag para saber se o Sharingan foi ativado e o mapa trocado.
    sharingan_start = 0 # Tempo em que o Sharingan foi ativado.
    raikiri_start = 0 # Tempo de início do Raikiri.
    drucao_mapa3_ms = 20000 # Duração em milissegundos para o mapa 3 ficar ativo.
    raikiri_anim_rate_fast = max(1, frame_rates['sharingan'] // 2) # Taxa de animação mais rápida para o Raikiri.
    raikiri_move_speed_slow = 25 # Velocidade de movimento durante o Raikiri.

    while running:
        pygame.event.pump() # Processa eventos internos do Pygame.
        keys = pygame.key.get_pressed() # Obtém o estado de todas as teclas pressionadas.

        # --- Lógica de Entrada de Usuário ---
        # Determina qual 'Symbol' (símbolo de entrada) corresponde às teclas pressionadas.
        # Considera combinações como SHIFT+A, S+A, etc.
        # Prioriza estados "atômicos" (jump, attack) para não serem interrompidos por outras entradas.

        # --- Atualiza Estado (δ) ---
        # Utiliza a tabela de transições para determinar o próximo estado.
        # Se o estado mudou, reinicia o frame_index e o tick.

        # --- Atualiza Frame da Animação ---
        # Controla qual frame da animação deve ser exibido com base no 'frame_rates'
        # e no 'tick' atual. Gerencia loops de animação e transições de volta ao IDLE.
        # Possui lógicas específicas para ataques e habilidades para garantir que as animações
        # sejam concluídas antes de retornar a um estado normal.

        # --- Física do Pulo e Movimento ---
        # Calcula o offset vertical para o pulo.
        # Aplica movimento horizontal com base no estado (andar, correr, agachar-andar).
        # Garante que o personagem permaneça dentro dos limites da tela.

        # --- Lógica de Troca de Mapa no Sharingan ---
        # Quando o Sharingan é ativado (e atinge o frame 19), o mapa de fundo muda para 'mapa3'.
        # O mapa 'mapa3' permanece ativo por 'drucao_mapa3_ms' milissegundos e depois retorna ao 'mapa4'.
        # Também gerencia o som do Sharingan e um efeito de fade na animação.

        # --- Desenho Final ---
        screen.blit(current_background, (0, 0)) # Desenha o background atual.
        # Lógica especial de desenho para o Sharingan (fade e full-screen nos últimos frames).
        # Desenha o frame atual do personagem na tela, ajustando sua posição.
        pygame.display.flip() # Atualiza a tela inteira para mostrar o que foi desenhado.

        tick += 1 # Incrementa o contador de ticks.
        clock.tick(60) # Limita a taxa de quadros a 60 FPS.

        # --- Gerenciamento de Eventos (Sair do Jogo) ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False # Define a flag para sair do loop principal.

    pygame.quit() # Desinicializa todos os módulos Pygame.
```

* **Loop Principal do Jogo:** O coração do programa, onde todos os cálculos, atualizações e desenhos acontecem.
* **Processamento de Entrada:** Captura as teclas pressionadas e as traduz em "símbolos" de entrada para o AFD.
* **Atualização de Estado:** A lógica principal do AFD ocorre aqui, usando a tabela de transições para mudar o estado do personagem.
* **Animação:** Controla qual frame de animação deve ser exibido com base no estado e na taxa de quadros definida.
* **Física:** Implementa o movimento horizontal e a parábola do pulo.
* **Lógica do Sharingan:** Gerencia a ativação do Sharingan, a troca de mapa de fundo, o som e o efeito visual de fade.
* **Desenho:** Redesenha o background e o personagem a cada frame.
* **Controle de FPS:** `clock.tick(60)` garante que o jogo não rode muito rápido.
* **Saída do Jogo:** Permite sair do jogo via evento `QUIT`.

---

## Controles do Jogo

Aqui está uma tabela detalhada das ações que cada tecla ou combinação de teclas realiza no jogo:

| Tecla(s)             | Ação                                       | Direção do Personagem | Estados Associados                         | Observações                                                                        |
| :------------------- | :----------------------------------------- | :-------------------- | :----------------------------------------- | :--------------------------------------------------------------------------------- |
| `A`                  | Andar para a Esquerda                      | Esquerda              | `IDLE_LEFT`, `WALK_LEFT`                   | Se estiver em `IDLE_LEFT`, permanece. Se em `IDLE`, vai para `WALK_LEFT`.           |
| `D`                  | Andar para a Direita                       | Direita               | `IDLE`, `WALK_RIGHT`                       | Se estiver em `IDLE`, permanece. Se em `IDLE_LEFT`, vai para `WALK_RIGHT`.         |
| `SHIFT` + `A`        | Correr para a Esquerda                     | Esquerda              | `RUN_LEFT`                                 | Mais rápido que andar.                                                            |
| `SHIFT` + `D`        | Correr para a Direita                      | Direita               | `RUN_RIGHT`                                | Mais rápido que andar.                                                            |
| `S`                  | Agachar                                    | Atual                 | `CROUCH`, `CROUCH_LEFT`                    | Mantém o agachamento enquanto `S` estiver pressionado.                            |
| `S` + `A`            | Andar Agachado para a Esquerda             | Esquerda              | `CROUCH_WALK_LEFT`                         | Movimento lento e agachado.                                                       |
| `S` + `D`            | Andar Agachado para a Direita              | Direita               | `CROUCH_WALK`                              | Movimento lento e agachado.                                                       |
| `SPACE`              | Pular                                      | Atual                 | `JUMP`, `JUMP_LEFT`                        | O personagem permanece no ar por uma duração fixa. Pode mudar de direção no ar. |
| `H`                  | Ataque Básico                              | Atual                 | `ATTACK`, `ATTACK_LEFT`                    | Animação de ataque padrão. Retorna ao `IDLE` ao final.                              |
| `U`                  | Ataque para Cima                           | Atual                 | `ATTACK_UP`, `ATTACK_UP_LEFT`              | Animação de ataque direcionado para cima. Retorna ao `IDLE` ao final.            |
| `R` + `T`            | Raikiri (Habilidade Especial)              | Atual                 | `RAIKIRI`, `RAIKIRI_LEFT`                  | Animação longa com som. O personagem se move lentamente durante a animação.       |
| `J`                  | Sharingan (Habilidade Especial)            | Atual                 | `SHARINGAN`, `SHARINGAN_LEFT`              | Animação longa com som e mudança de mapa. Uma vez ativada, o efeito tem duração. |
| `P`                  | Animação de Vitória                        | Atual                 | `WIN`, `WIN_LEFT`                          | Após a animação, o jogo é encerrado.                                                |
| `M`                  | Invocação Nindogs                          | Atual                 | `NINDOG_RIGHT`, `NINDOG_LEFT`              | Animação de invocação. Retorna ao `IDLE` ao final.                                  |
| Nenhuma tecla        | Voltar para estado de Repouso/Agachado     | Atual                 | `IDLE`, `IDLE_LEFT`, `CROUCH`, `CROUCH_LEFT` | Quando nenhuma tecla de movimento ou ação é pressionada.                          |

---

