# Pi-Mation v0.6
# Stop motion animation for the Raspberry Pi and camera module 1
# Russell Barnes - 12 Nov 2013 for Linux User magazine issue 134 
# www.linuxuser.co.uk
# Modified by Emory T Moody III, Oct 2016
# adding parallel full resolution pics and camera control. 

import pygame, picamera, os, sys, time

# global variables
pics_taken = 0
current_alpha, next_alpha = 128, 255


# set your desired fps (~5 for beginners, 10+ for advanced users)
fps = 12

# Initialise Pygame, start screen and camera
pygame.init()
res = pygame.display.list_modes() # return the best resolution for your monitor
width, height = 1920,1080 # Having trouble getting the right resolution? Manually set with: 'width, height = 1650, 1050' (where the numbers match your monitor)
print ("Reported resolution is:", width, "x", height)
start_pic = pygame.image.load(os.path.join('data', 'start_screen.jpg'))
start_pic_fix = pygame.transform.scale(start_pic, (1920, 1080))
screen = pygame.display.set_mode([1920,1080])
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible = False
play_clock = pygame.time.Clock()
camera = picamera.PiCamera(sensor_mode=1)
camera.resolution =(1920,1080) 
# camera.drc_strength = 'high'
camera.saturation = 25
camera.still_stats = True


def take_pic():
    """Grabs an image and load it for the alpha preview and 
    appends the name to the animation preview list"""
    global pics_taken, prev_pic
    pics_taken += 1
    camera.capture(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'), use_video_port = True)
    prev_pic = pygame.image.load(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'))
    awbMode = camera.awb_mode
    awbData=camera.awb_gains
    camera.awb_mode = 'off'
    camera.stop_preview()
    camera.sensor_mode = 2
    camera.resolution = (2592,1944)
    time.sleep(.8)
    camera.awb_gains = awbData
    time.sleep(.8)
    camera.capture(os.path.join('fullres', 'image_' + str(pics_taken) + '.jpg'), use_video_port = False)
    camera.sensor_mode = 1
    camera.resolution = (1920,1080)
    camera.awb_mode = awbMode
    camera.start_preview()
def delete_pic():
    """Doesn't actually delete the last picture, but the preview will 
    update and it will be successfully overwritten the next time you take a shot"""
    global pics_taken, prev_pic
    if pics_taken > 0:
        pics_taken -= 1
    if pics_taken >= 1:
        prev_pic = pygame.image.load(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'))
        
def animate():
    """Do a quick live preview animation of 
    all current pictures taken"""
    camera.stop_preview()
    for pic in range(1, pics_taken):
        anim = pygame.image.load(os.path.join('pics', 'image_' + str(pic) + '.jpg'))
        screen.blit(anim, (0, 0))
        play_clock.tick(fps)
        pygame.display.flip()
    play_clock.tick(fps)
    camera.start_preview()

def update_display():
    """Blit the screen (behind the camera preview) with the last picture taken"""
    screen.fill((0,0,0))
    if pics_taken > 0:
        screen.blit(prev_pic, (0, 0))
    play_clock.tick(30)
    pygame.display.flip()

def make_movie():
    """Quit out of the application 
    and create a movie with your pics"""
    camera.stop_preview()
    pygame.quit()
    print ("\nQuitting Pi-Mation to transcode your video.\nWarning: this will take a long time!")
    print ("\nOnce complete, write 'omxplayer video.mp4' in the terminal to play your video.\n")
    os.system("avconv -r " + str(fps) + " -i " + str((os.path.join('pics', 'image_%d.jpg'))) + " -vcodec libx264 video.mp4")
    sys.exit(0)
    
def change_alpha():
    """Toggle's camera preview optimacy between half and full."""
    global current_alpha, next_alpha
    camera.stop_preview()
    current_alpha, next_alpha = next_alpha, current_alpha
    return next_alpha
    
def quit_app():
    """Cleanly closes the camera and the application"""
    camera.close()
    pygame.quit()
    print ("You've taken", pics_taken, " pictures. Don't forget to back them up (or they'll be overwritten next time)")
    sys.exit(0)



def intro_screen():
    """Application starts on the help screen. User can exit 
    or start Pi-Mation proper from here"""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_app()
                elif event.key == pygame.K_F1:
                    camera.start_preview()
                    intro = False
        screen.blit(start_pic_fix, (0, 0))
        pygame.display.update()



def main():
    """Begins on the help screen before the main application loop starts"""
    intro_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_app()
                elif event.key == pygame.K_SPACE:
                    take_pic()
                elif event.key == pygame.K_BACKSPACE:
                    delete_pic()
                elif event.key == pygame.K_RETURN:
                    make_movie()
                elif event.key == pygame.K_TAB:
                    camera.preview_alpha = change_alpha()
                    camera.start_preview()
                elif event.key == pygame.K_F1:
                    camera.stop_preview()
                    intro_screen()
                elif event.key == pygame.K_p:
                    if pics_taken > 1:
                        animate()
                elif event.key == pygame.K_w:
                     awbData=camera.awb_gains
                     camera.awb_mode = 'off'
                     camera.awb_gains=awbData
                elif event.key == pygame.K_a:
                     camera.awb_mode = 'auto'
                elif event.key == pygame.K_t:
                    camera.awb_mode = 'tungsten'
                elif event.key == pygame.K_f:
                    camera.awb_mode = 'fluorescent'
                elif event.key == pygame.K_s:
                    camera.awb_mode = 'sunlight'    
                elif event.key == pygame.K_0:
                    camera.iso = 0
                elif event.key == pygame.K_1:
                    camera.iso = 100
                elif event.key == pygame.K_2:
                    camera.iso = 200    
                elif event.key == pygame.K_3:
                    camera.iso = 320
                elif event.key == pygame.K_4:
                    camera.iso = 400    
                elif event.key == pygame.K_5:
                    camera.iso = 500
                elif event.key == pygame.K_6:
                    camera.iso = 640
                elif event.key == pygame.K_8:
                    camera.iso = 800
                elif event.key == pygame.K_z:
                    camera.drc_strength = 'off'
                elif event.key == pygame.K_x:
                    camera.drc_strength = 'low'
                elif event.key == pygame.K_c:
                    camera.drc_strength = 'medium'
                elif event.key == pygame.K_v:
                    camera.drc_strength = 'high'
                elif event.key == pygame.K_COMMA:
                    camera.saturation = 0
                elif event.key == pygame.K_PERIOD:
                    camera.saturation = 25
                elif event.key == pygame.K_LEFT:
                    checkLow = camera.exposure_compensation
                    if checkLow > -25:
                        camera.exposure_compensation -= 1
                elif event.key == pygame.K_RIGHT:
                    checkHigh = camera.exposure_compensation
                    if checkHigh < 25:
                        camera.exposure_compensation += 1
                    
                    
        update_display()

if __name__ == '__main__':
    main()
