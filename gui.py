
import pygame
from process_image import get_output_image

# pre defined colors, pen radius and font color
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 7
font_size = 500

# window screen  size
width = 640
height = 640

# initializing pygame window screen
screen = pygame.display.set_mode((width*2, height))
screen.fill(white)
pygame.font.init()

# Icon
pygame.display.set_caption("pehchanKon")
icon = pygame.image.load('k32.png')
pygame.display.set_icon(icon)

def show_output_image(img):
    # copying the pixel array of the imh on new surface
    surf = pygame.pixelcopy.make_surface(img)

    surf = pygame.transform.rotate(surf, -270)
    # flipping the image vertically
    surf = pygame.transform.flip(surf, 0, 1)
    screen.blit(surf, (width+2, 0))

# creating a surface and putting the original screen on it of same size
def crope(orginal):
    cropped = pygame.Surface((width-5, height-5))
    cropped.blit(orginal, (0, 0), (0, 0, width-5, height-5))
    return cropped

# Drawing line from last postion to current mouse motion
def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)

# Splitting the screen into two parts
def draw_partition_line():
    pygame.draw.line(screen, black, [width, 0], [width,height ], 8)


try:
    while True:
        # get all events in an event queue
        e = pygame.event.wait()
        draw_partition_line()

        # clear screen after right click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
            screen.fill(white)

        # quiting the pygame window on clicking the close button
        if e.type == pygame.QUIT:
            raise StopIteration

        # start drawing after left click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
            screen.fill(white)
            color = black
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True

        # stop drawing after releasing left click
        if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
            draw_on = False
            fname = "out.png"

            img = crope(screen)
            pygame.image.save(img, fname)

            output_img = get_output_image(fname)
            show_output_image(output_img)

        # start drawing line on screen if draw is true
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos
       #  will update the contents of the entire display after each loop
        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()
