import sys
import glob
import random

import pygame
import pygame.locals
from PIL import Image, ImageFilter

class View() :

    def __init__(self):

        # Initialize PyGame
        pygame.init()

        self.screen = pygame.display.set_mode( (700,700), 0, 32)
        pygame.display.set_caption("ElectricDreamz")

        # Set up FPS clock
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        self.cycle = 0
        self.cycleSpeed = random.randint(10,200)/10.0
        self.currentImage = 0

    def loadImages(self):

        self.images_path = []
        self.images = []
        for path in glob.glob("../christ/*.jpeg"):
            self.images_path.append(path)
            self.images.append(pygame.image.load(path))

        self.coordinates = [ random.randint(0, 100) for i in self.images ]
        self.coordinates[random.randint(0,len(self.images)-1)] = 100
        self.renorm_coordinates()
        self.direction = random.randint(0,len(self.images)-1)

        self.font = pygame.font.Font("./Lack-Regular.otf",50)
        self.text1 = self.makeText("What is")
        self.text2 = self.makeText("'christ'")


    def change_direction(self):

        self.direction = random.randint(0,len(self.images)-1)

    def renorm_coordinates(self):

        s = sum(self.coordinates)
        self.coordinates = [ c/s for c in self.coordinates ]

    def makeText(self, text, insideColor = (250,250,250), outsideColor=(150,150,150)) :

        return self.font.render(text, 1, insideColor )
        textIn   = self.font.render(text, 1, insideColor )
        #textOut  = self.font.render(text, 1, outsideColor)
        #size = textIn.get_width() + 2, textIn.get_height() + 2
        #s = pygame.Surface(size, pygame.SRCALPHA, 32)
        #s.blit(textOut,(0,0))
        #s.blit(textOut,(2,2))
        #s.blit(textOut,(2,0))
        #s.blit(textOut,(0,2))
        #s.blit(textIn, (1,1))

        #return s

    def mainLoop(self) :

        # Handle events
        self.eventHandler()

        # Handle keys
        self.keysHandler()

        # Render elements
        self.update()
        self.render()

        # Update screen
        pygame.display.update()
        self.fpsClock.tick(self.fps)


    def eventHandler(self) :

        for event in pygame.event.get():

            if (event.type == pygame.QUIT) :
                pygame.quit()
                sys.exit()


    def keysHandler(self) :

        pass
        #keyPressed = pygame.key.get_pressed()
        #print(keyPressed)

    def blur(self,image, radius):

        # Convert the surface to PIL image
        surfSize = image.get_size()
        surfInString = pygame.image.tostring(image, "RGBA", False)
        surfPIL = Image.frombytes("RGBA", surfSize, surfInString)

        # Blur image using PIL
        surfPILblurred = surfPIL.filter(ImageFilter.GaussianBlur(radius=radius))
        return pygame.image.fromstring(surfPILblurred.tobytes("raw", "RGBA"), surfSize, "RGBA")


    def update(self):

        current_max = max(self.coordinates)
        current_max_coordinate = [i for i,j in enumerate(self.coordinates) if j == current_max][0]
        if current_max >= 0.95 and current_max_coordinate == self.direction:
            self.change_direction()
        elif current_max <= 0.80 and random.randint(0,100)<7:
            self.change_direction()

        self.speed = max((1-current_max)/10,0.0001)

        self.coordinates[self.direction] += self.speed
        self.renorm_coordinates()

    def render(self):

        self.screen.fill( (0,0,0) )

        coordinates_and_images = sorted(zip(self.coordinates, self.images), key=lambda ci:ci[0], reverse=True)

        i = 0
        for coordinate, image in coordinates_and_images:
            render_image = self.blur(image, (25*(1-coordinate))**1.3)
            render_image.set_alpha(int((1-coordinate)*255))
            if i == 0:
                self.screen.blit(render_image, (0,0))
            else:
                self.screen.blit(render_image, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
            i+=1
            if i >= 3:
                break

        #size = textIn.get_width() + 2, textIn.get_height() + 2
        self.screen.blit(pygame.transform.scale(self.screen, (750*2,750*2)), (0,0))
        w1 = self.text1.get_width()
        h1 = self.text1.get_height()
        w2 = self.text2.get_width()
        h2 = self.text2.get_height()
        self.screen.blit(self.text1, (750/2-w1/2, 750/2-h1-10))
        self.screen.blit(self.text2, (750/2-w2/2, 750/2+10))


def main():

    v = View()
    v.loadImages()

    while True:
        v.mainLoop()

main()
