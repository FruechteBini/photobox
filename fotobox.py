import serial
#import auit_thermal_printer
import os, time, Image, sys, random
from os.path import isfile, join
import pygame
from time import sleep
from picamera import PiCamera
from Adafruit_Thermal import *
from os import listdir

#initialize camera
camera=PiCamera(resolution = (1920, 1440))
#camera.rotation = 180
# Some variables
photoPath = '/home/pi/Python-Thermal-Printer/fotobox/'
photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
photoResize = 512, 384
photoTitle = "Gtown " + time.strftime("%Y-%m-%d-%H-%M") + "\n Karlas grosser Tag"
gewinnerTitle = " "

#define printer
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#start camera preview
camera.start_preview(fullscreen=False, window=(0,0,1902,1080))


#random Pfeffi
def random_pfeffi():
    random_number = random.randint(1,10)
    if random_number is 5:
        gewinnerTitle = "Du hast einen Pfeffi gewonnen!\nGehe an die Bar und gib das\nFoto ab, um deinen Gewinn\n     einzuloesen!"
        print "gewonnen!\n"
    else:
        gewinnerTitle = " "
        print "verloren\n"
    return gewinnerTitle


def photo_callback():
        #mixer = pygame.mixer
        #path = "/home/pi/ogg"
        #click_sound=mixer.Sound(path+"/"+"click.ogg")
        #channel = click_sound.play()
        # Define filename with timestamp
        photoName = time.strftime("%Y-%m-%d-%H-%M-%S") + "_fotobox.jpg"
        camera.capture(photoPath+photoName)
	#camera.capture(photoPath + photoName)#time.strftime("%y%m%d_%H-%M-%S") + ".jpg")
        # Take photo using "raspistill"
        #os.system("sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + photoPath + photoName)
        # Resize the high res photo to create thumbnail
	Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")

def print_callback():
        # Rotate the thumbnail for printing
        Image.open(photoPath + "thumbnail.jpg").transpose(2).rotate(180).save(photoPath + "thumbnail-rotated.jpg")
        # Print the foto
        printer.begin(90) # Warmup time
        printer.setTimes(40000, 3000) # Set print and feed times
        printer.justify('C') # Center alignment
        printer.println(photoTitle)
        printer.printImage(Image.open(photoPath + "thumbnail-rotated.jpg"), True) # Specify image to print
        printer.feed(1)
        pfeffiwin = random_pfeffi()
        printer.println(pfeffiwin)
        printer.feed(3)



def play_random_sound():
    mixer=pygame.mixer
    #path you want to get wav files from
    path = "/home/pi/ogg/"
    onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]

    onlyoggfiles = []
    for f in onlyfiles:
        if f[-3:] == "ogg":
            onlyoggfiles.append(f)

    #generate random number based on number of available files
    randomnum = random.randint(0,len(onlyoggfiles)-1)

    play_sound = mixer.Sound(path + "/" + onlyoggfiles[randomnum])
    #pygame.mixer.music.play()
    channel = play_sound.play()
    #pygame.mixer.music.load("/home/pi/ogg/sexy.ogg")
    #pygame.mixer.music.play()
    while channel.get_busy():
        print "playing.."
    print "finished"
    #click_sound = mixer.Sound(path + "/" + "click.ogg")
    #channel = click_sound.play()


#init pygame for mouseclick
pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load("/home/pi/ogg/sexy.ogg")
#pygame.mixer.music.play()
#print "\nsound played"

while True:
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print("nice")
            #takePicture()
            #play_random_sound()
            photo_callback()
            print_callback()
            pygame.event.clear()
