import pygame as pg
import pandas as pd
import random

# Init ----------------------------------------
WIDTH = 360
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")

# birdImg = pg.image.load("bird.png")

running = True
gameSpeed = 1


# Classes -------------------------------------
class Bird:
    def __init__(self, x, y):
        self.location = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)

        self.border = 50

        self.jumpForce = pg.math.Vector2(0, -7)

    def updateLocation(self):
        self.velocity.x += self.acceleration.x
        self.velocity.y += self.acceleration.y

        self.location.x += self.velocity.x
        self.location.y += self.velocity.y

        self.acceleration.x = 0
        self.acceleration.y = 0

    def applyForce(self, force):
        self.acceleration.x += force.x
        self.acceleration.y += force.y

    def jump(self):
        self.applyForce(self.jumpForce)
        self.velocity.x = 0
        self.velocity.y = 0

    def draw(self):
        # window.blit(birdImg, (self.location.x - 12.5, self.location.y - 12.5))
        pg.draw.rect(window, BLACK, (self.location.x, self.location.y, self.border, self.border))

    def crash(self, tube):
        if self.location.y <= tube.height or self.location.y + self.border >= tube.height + tube.gapHeight:
            if tube.x - self.border <= self.location.x <= tube.x + tube.width:
                return True

        if self.location.y < 0 or self.location.y > HEIGHT - self.border:
            return True

class Tube:
    def __init__(self, speed, x=WIDTH):
        self.gapHeight = 180
        self.width = 100
        self.height = random.randrange(100, HEIGHT - self.gapHeight - 100)

        self.x = x
        self.speed = speed

        self.bypassed = False

    def draw(self):
        pg.draw.rect(window, BLACK, (self.x, 0, self.width, self.height))
        pg.draw.rect(window, BLACK, (self.x, self.height + self.gapHeight, self.width, HEIGHT - self.height - self.gapHeight))

    def move(self):
        self.x -= self.speed


class TubeSystem:
    def __init__(self, speed):
        self.speed = speed

        self.tubeList = [Tube(self.speed), Tube(self.speed, WIDTH + (WIDTH + 100)/2)]

    def add(self):
        self.tubeList.append(Tube(self.speed))

    def remove(self):
        self.tubeList.pop(0)

    def drawAll(self):
        for tube in self.tubeList:
            tube.draw()

    def moveAll(self):
        for tube in self.tubeList:
            tube.move()


# Setup ---------------------------------------
bird = Bird(WIDTH / 2, HEIGHT / 2)
tubes = TubeSystem(gameSpeed)

score = 0

gravity = pg.math.Vector2(0, 0.3)
pause = True

# Main loop -----------------------------------

while running:

    window.fill(WHITE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()
                pause = False

    # action
    if not pause:
        bird.applyForce(gravity)

    bird.updateLocation()



    if tubes.tubeList[0].x < - tubes.tubeList[0].width:
        tubes.add()
        tubes.remove()

    if not pause:
        tubes.moveAll()

    # check if bypassed tube, i'm proud of this part of my code
    for tube in tubes.tubeList:
        if not tube.bypassed:
            if bird.crash(tube):
                print("Your final score is: ", score)
                running = False
                break
            elif tube.x + tube.width < bird.location.x:
                tube.bypassed = True
                score += 1
                print("Your score is : ", score)
                break

    # draw
    bird.draw()
    tubes.drawAll()

    pg.display.update()
