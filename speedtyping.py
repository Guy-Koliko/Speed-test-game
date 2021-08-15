import pygame
from pygame.locals import *
import sys
import time
import random
from pathlib import Path

path = Path(__file__).parent.absolute()


#this is the game class
class Game:


    #the main constructor with useful variables
    def __init__(self):
        self.w = 750
        self.h= 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0'

        self.wpm = 0
        self.end = False
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)


        #calling and initilatizing pygame
        pygame.init()

        #this helpful variables load all our images for the screen with the help of pygame
        self.open_img = pygame.image.load(f"{path}/type-speed-open.png")

        self.open_img =pygame.transform.scale(self.open_img,(self.w,self.h))

        self.bg = pygame.image.load(f'{path}/background.jpg')
        self.bg = pygame.transform.scale(self.bg,(500,750))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')

        '''
        The draw_text() method is a helper function that help to
        draw the text on the screen. This mehthod takes the following arguments.
         *screen
         *msg
         *y
         *fsize
         *color
        '''
    def draw_text(self,screen,msg,y,fsize,color):
            font = pygame.font.Font(None,fsize)
            text = font.render(msg,1,color)
            text_rect = text.get_rect(center=(self.w/2,y))

            #updating the pygame with the screen
            screen.blit(text,text_rect)
            pygame.display.update()

    '''
        The get_sentence() method open a text file that contains all of the sentence used in the game. The sentence in the .text file are return randomly
        '''
    def get_sentence(self):
        f = open(f'{path}/sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    '''
         The show_results() method, calculate the speed of a user.
         It performs the calculations in this maner; Whenever a user clicks on the imput box and when the user hits the Enter key. The difference between the clicking in the input box and hitting the Enter key is taking.

         Accuracy is calcualted in this way; the correct words typed by a user is compared with the displayed text, using this formular (correct characters)x100/ (total characters in sentence)
        '''

    def show_results(self,screen):
        if (not self.end):
            #Calculate time
            self.total_time = time.time() - self.time_start

            #Calculate accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i]== c:
                        count +=1
                except:
                    pass
                self.accuracy = count/len(self.word)*100

                #Calculate words per minute
                self.wpm = len(self.input_text)*60/(5*self.total_time)
                self.end = True
                print(self.total_time)

                self.results = 'Time:'+str(round(self.total_time))+" secs Accuracy:"+str(round(self.accuracy))+ "%"+'Wpm: '+ str(round(self.wpm))


                #draw icon image
                self.time_img = pygame.image.load(f"{path}/icon.png")
                self.time_img = pygame.transform.scale(self.time_img, (150,150))

                screen.blit(self.time_img, (self.w/2-75,self.h-140))
                self.draw_text(screen,"Reset", self.h -70,26, (100,100,100))

                print(self.results)
                pygame.display.update()

    def run(self):
        self.reset_game()

        self.running = True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0),(50,250,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C,(50,250,650,50), 2)

            #update the text of user input
            self.draw_text(self.screen,self.input_text, 274,26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    # position of input box

                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()

                    # postion the reset box
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                        if self.active and not self.end:
                            if event.key == pygame.K_RETURN:
                                print(self.input_text)
                                self.show_results(self.screen)
                                print(self.input_text)
                                self.show_results(self.screen)
                                print(self.results)
                                self.draw_text(self.screen, self.results,350,28,self.RESULT_C)
                                self.end = True
                            elif event.key == pygame.K_BACKSLASH:
                                    self.input_text = self.input_text[:-1]
                            else:
                                try:
                                    self.input_text += event.unicode
                                except:
                                    pass
            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.total_time =0
        self.start_time = 0

        self.wpm = 0


        #get random sentence

        self.word = self.get_sentence()
        if (not self.word):
            self.reset_game()

            #drawing heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))

        msg = "Typing Speed Test"
        self.draw_text(self.screen,msg,80,0,self.HEAD_C)

         # draw the sentence string
        self.draw_text(self.screen, self.word,200,28,self.TEXT_C)

        pygame.display.update()

Game().run()
