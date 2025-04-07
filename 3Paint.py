import pygame
import math

pygame.init()

# 画布尺寸和初始化
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
canvas_color = (255, 255, 255)

# 可选颜色
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'eraser': canvas_color
}

# 初始状态
radius = 10
mode = 'blue'
drawing = False
shape = 'free'
start_pos = None

# 创建画布表面
canvas = pygame.Surface((width, height))
canvas.fill(canvas_color)

running = True
while running:
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 键盘控制颜色和形状
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                mode = 'red'
            elif event.key == pygame.K_g:
                mode = 'green'
            elif event.key == pygame.K_b:
                mode = 'blue'
            elif event.key == pygame.K_y:
                mode = 'yellow'
            elif event.key == pygame.K_p:
                mode = 'purple'
            elif event.key == pygame.K_o:
                mode = 'orange'
            elif event.key == pygame.K_e:
                mode = 'eraser'

            # 新增图形选择快捷键
            elif event.key == pygame.K_f:
                shape = 'free'
            elif event.key == pygame.K_d:
                shape = 'rect'
            elif event.key == pygame.K_c:
                shape = 'circle'
            elif event.key == pygame.K_s:
                shape = 'square'
            elif event.key == pygame.K_t:
                shape = 'right_triangle'
            elif event.key == pygame.K_q:
                shape = 'equilateral_triangle'
            elif event.key == pygame.K_h:
                shape = 'rhombus'

        # 鼠标按下
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # 鼠标抬起时画图
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            x1, y1 = start_pos
            x2, y2 = end_pos
            color = colors[mode]

            if shape == 'rect':
                width_rect = abs(x2 - x1)
                height_rect = abs(y2 - y1)
                pygame.draw.rect(canvas, color, (min(x1, x2), min(y1, y2), width_rect, height_rect))

            elif shape == 'circle':
                radius = int(math.hypot(x2 - x1, y2 - y1))
                pygame.draw.circle(canvas, color, start_pos, radius)

            elif shape == 'square':
                side = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(canvas, color, (x1, y1, side, side))

            elif shape == 'right_triangle':
                points = [start_pos, (x1, y2), (x2, y2)]
                pygame.draw.polygon(canvas, color, points)

            elif shape == 'equilateral_triangle':
                side = abs(x2 - x1)
                height_eq = int(side * (3 ** 0.5) / 2)
                points = [
                    (x1, y2),
                    (x1 + side, y2),
                    (x1 + side / 2, y2 - height_eq)
                ]
                pygame.draw.polygon(canvas, color, points)

            elif shape == 'rhombus':
                dx = (x2 - x1) // 2
                dy = (y2 - y1) // 2
                points = [
                    (x1 + dx, y1),         # top
                    (x2, y1 + dy),         # right
                    (x1 + dx, y2),         # bottom
                    (x1, y1 + dy)          # left
                ]
                pygame.draw.polygon(canvas, color, points)

        # 自由画线
        elif event.type == pygame.MOUSEMOTION and drawing and shape == 'free':
            pygame.draw.circle(canvas, colors[mode], event.pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
