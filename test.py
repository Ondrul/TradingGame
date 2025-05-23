import pygame
import math

pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel-by-pixel Line Animation")

data = [10, 30, 20, 50, 40, 60, 80, 70]

def get_points(data, width, height, margin=50):
    max_val = max(data)
    min_val = min(data)
    data_range = max_val - min_val if max_val != min_val else 1
    x_step = (width - 2 * margin) / (len(data) - 1)
    points = []
    for i, val in enumerate(data):
        x = margin + i * x_step
        y = height - margin - ((val - min_val) / data_range) * (height - 2 * margin)
        points.append((int(x), int(y)))
    return points

points = get_points(data, width, height)

running = True
clock = pygame.time.Clock()

current_segment = 0
pos_on_line = 0.0  # progress from 0 to 1 on current segment
speed = 0.005      # how much to move per frame (adjust for speed)

def lerp(a, b, t):
    return a + (b - a) * t

while running:
    clock.tick(60)  # 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Draw axes
    pygame.draw.line(screen, (0, 0, 0), (50, 50), (50, height - 50), 2)
    pygame.draw.line(screen, (0, 0, 0), (50, height - 50), (width - 50, height - 50), 2)

    # Draw all completed segments fully
    if current_segment > 0:
        pygame.draw.lines(screen, (0, 100, 200), False, points[:current_segment+1], 3)

    # Animate current segment
    if current_segment < len(points) - 1:
        start = points[current_segment]
        end = points[current_segment + 1]

        # Calculate current point on the line
        x = lerp(start[0], end[0], pos_on_line)
        y = lerp(start[1], end[1], pos_on_line)

        # Draw partial line from start to current point
        pygame.draw.line(screen, (0, 100, 200), start, (int(x), int(y)), 3)

        pos_on_line += speed
        if pos_on_line >= 1.0:
            pos_on_line = 0.0
            current_segment += 1
    else:
        # Draw full line when done
        pygame.draw.lines(screen, (0, 100, 200), False, points, 3)

    pygame.display.flip()

pygame.quit()
