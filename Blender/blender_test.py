#Arrow Image from http://www.wpclipart.com/

import sys
import os

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge
import codeInterp


class SimpleLayout(bgui.bge_utils.Layout):
    """A layout showcasing various Bgui features"""

    def __init__(self, sys, data):
        super().__init__(sys, data)
        self.Cube = codeInterp.tester()
        self.hidden = True
        # Use a frame to store all of our widgets
        self.frame = bgui.Frame(self, border=0)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]
        self.frame.visible = True

        self.scene = bge.logic.getCurrentScene()
        ob_list = self.scene.objects
        self.Camera = ob_list['Camera']
        self.Cam_Zoomed = ob_list['Cam_Zoomed']
        self.Cam_Follow = ob_list['Cam_Follow']

        self.popupCounter = 0

        self.whichCam = 2

        self.frame = bgui.Frame(self, size=[1, .045], pos=[0,0.0],
                            sub_theme="Bar",  options=bgui.BGUI_DEFAULT)


        self.bgFrame = bgui.Frame(self, size=[1, 1], pos=[0,0],
                            sub_theme="BG",  options=bgui.BGUI_DEFAULT)

        self.reset_button = bgui.FrameButton(self.frame, text='Reset', size=[.07, .7], pos=[.08, .15],
                                            sub_theme="Reset", options=bgui.BGUI_DEFAULT)
        self.reset_button.on_click = self.on_reset_click

        #self.reset_button.on_click = self.on_reset_click

        # self.button.on_click = self.hide_show

        # A themed frame
        self.win = bgui.Frame(self.bgFrame, size=[0.5, 0.95], pos=[0, 0.05],
                              options=bgui.BGUI_DEFAULT)

        self.rightWin = bgui.Frame(self, size=[0.5, 0.25], pos=[0.5, 0.05],
                                  sub_theme="Console", options=bgui.BGUI_DEFAULT)
        

        # A button
        self.run_button = bgui.FrameButton(self.frame, text='Run', size=[.07, .7], pos=[.005, .15],
                                        sub_theme="Run",   options=bgui.BGUI_DEFAULT)

        # Setup an on_click callback for the image
        self.run_button.on_click = self.on_run_click

        # Add a label
        self.lbl = bgui.Label(self, text="Score : 0", pos=[.5, .96],
        	sub_theme='small', options = bgui.BGUI_DEFAULT)

        # A couple of progress bars to demonstrate sub themes
        self.progress = bgui.ProgressBar(self.frame, percent=0.0, size=[0.5, 0.7], pos=[.15, 0.15],
                                         sub_theme="Progress", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

        self.cam_button = bgui.FrameButton(self.frame, text='Zoomed', size=[.1, .7], pos=[.8, .15],
                                           sub_theme="Help", options=bgui.BGUI_DEFAULT)

        # Setup an on_click callback for the image
        self.cam_button.on_click = self.on_cam_click

        #self.health = bgui.ProgressBar(self.win, percent=0.5, size=[0.92, 0.02], pos=[0, 0.14],
        #									sub_theme="Health",	options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

        # A few TextInput widgets
        self.input = bgui.TextInput(self.win, text="", font="consola.ttf", pt_size=26, size=[.92, .98], pos=[.059, .01],
                                    input_options=bgui.BGUI_INPUT_NONE, options=bgui.BGUI_DEFAULT)
        self.input.activate()

        self.console = bgui.TextBlock(self.rightWin, text="console", size=[.96, .98], pos=[.01, .01],
                                     sub_theme="Cons", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

        self.lines = []
        incriment = .0285
        start = 0.9665
        count = 1
        for i in range(34):
            self.lines.append(bgui.Label(self.win, text=str(count) + ".", font="arial.ttf", pos=[.01, start], options=bgui.BGUI_DEFAULT))
            start = start - incriment
            count = count + 1
        #self.lines.append(bgui.Label(self.win, text="2.", pos=[.01, .94], options = bgui.BGUI_DEFAULT))
        
        #self.input.on_enter_key = self.on_run_click


        # A counter property used for the on_img_click() method
        #self.counter = 0

        self.helpWin = bgui.Frame(self, size=[0.75, .9], pos=[.5, 1],
                               options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

        self.helpText = bgui.TextBlock(self.helpWin, text="Help:\n\n"+
        	"There are four ways to move the quad-copter. Each command moves it one block."+
            "\n\nmoveUp() - Moves the copter upwards."+
            "\nmoveDown() - Moves the copter downwards."+
            "\nmoveLeft() - Moves the copter to the left."+
            "\nmoveRight() - Moves the copter to the right."+
        	"\n\nYou can take advantages of both types of Python loops:"+
            "\n\nfor <commands> - For loop limited to specification."+
            "\nwhile <commands> - Possible infinite loop."+
        	"\n\nThere is a special type of check that can be done in order to pick up objects:"+
            "\nif - using the keyword 'is on' instead of '==' will allow you to check for below:"+
        	"\n\nFunctions:\n\nobject() - Type object for comparison.\nground() - Check is something is on the ground.\npickup() - Pick up the object.", size=[.9, .9], pos=[.0, .0],
    	                      options = bgui.BGUI_DEFAULT |bgui.BGUI_CENTERX | bgui.BGUI_CENTERY)

        self.closeHelp =    bgui.FrameButton(self.helpWin, text='Close', size=[.1, .04], pos=[0.93, .1],
                                            sub_theme="Help", options=bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)

        self.closeHelp.on_click = self.hide_show

        self.help_button = bgui.FrameButton(self, text='Help', size=[.07, .04], pos=[0.93, .96],
                                            sub_theme="Help", options=bgui.BGUI_DEFAULT)
        self.help_button.on_click = self.hide_show

        self.popUpWindow = bgui.Frame(self, size=[0.4, .2], pos=[.5, 0.52],
                               sub_theme="PopUp", options=bgui.BGUI_DEFAULT)

        self.popUpText = bgui.TextBlock(self.popUpWindow, text="Your goal is to move the drone from the start \nlocation on the left, to the red block on the right", size=[.9, .8], pos=[.0, .0],
                              sub_theme="PopUp", options = bgui.BGUI_DEFAULT |bgui.BGUI_CENTERX | bgui.BGUI_CENTERY)

        self.win.img = bgui.Image(self.popUpWindow, 'arrow_down.png', size=[.1, .3], pos=[.112, .05],
            options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

        self.popup_button = bgui.FrameButton(self.popUpWindow, text='Next', size=[.2, .2], pos=[0.7, 0.1],
                                            sub_theme="Help", options=bgui.BGUI_DEFAULT)

        self.popup_button.on_click = self.popup_button_next

    def popup_button_next(self, widget):
        self.popupCounter+=1
        print(self.popupCounter)
        if self.popupCounter == 1:
            self.popUpWindow.position = [.05,.75]
            self.popUpText.text = "Do this by typing python code in this window"
            self.win.img.position = [.35,.05]

        elif self.popupCounter == 2:
            self.popUpWindow.position = [.6,.75]
            self.popUpText.text = "A list of commands can be found by\nclicking the 'Help' button"
            self.win.img.position = [.85,.65]
            self.win.img.update_image("arrow_up.png")
        elif self.popupCounter == 3:
            self.popUpWindow.position = [.01,.05]
            self.popUpText.text = "Click the 'Run' button to execute the code that you input"
            self.win.img.position = [.05,.05]
            self.win.img.update_image("arrow_down.png")
        elif self.popupCounter == 4:
            self.popUpWindow.position = [.09,.05]
            self.popUpText.text = "Click the 'Reset' button to return the drone to its original position"
            self.win.img.position = [.05,.05]
        elif self.popupCounter == 5:
            self.popUpWindow.position = [.5,.05]
            self.popUpWindow.size = [.45,.25]
            self.popUpText.text = "This button changes which view is used during code execution\n'Default' is the current camera\n'Zoomed' is a zoomed in version of the default camera\n'Follow' is a third person view of the drone"
            self.popup_button.text = "Close"
            self.popup_button.position = [0.05,0.1]
            self.popup_button.size = [.2, .15]
            self.win.img.position = [.75,.05]
        else:
            self.popUpWindow.visible = False

    def hide_show(self, widget):
    	if self.hidden:
    		self.helpWin.move([.5, .05], 400)
    		self.hidden = False
    	else:
    		self.helpWin.move([.5, 1.5], 400)
    		self.hidden = True


    #def on_input_enter(self, widget):
    #	self.lbl.text = "You've entered: " + widget.text
    #	widget.text = "You've locked this widget."
    #	self.input.activate()
    #widget.frozen = 1

    def on_cam_click(self, widget):
    	self.whichCam += 1
    	if self.whichCam == 4:
    		self.whichCam = 1
    		self.cam_button.text = 'Default'
    	elif self.whichCam == 2:
    		self.cam_button.text = 'Zoomed in'
    	elif self.whichCam == 3:
    		self.cam_button.text = 'Follow'

    def on_run_click(self, widget):
        #print(os.getcwd())
        if self.whichCam == 1:
        	self.scene.active_camera = self.Camera
        elif self.whichCam == 2:
        	self.scene.active_camera = self.Cam_Zoomed
        elif self.whichCam == 3:
        	self.scene.active_camera = self.Cam_Follow
        	self.win.visible = False
        externalFile = ''
        data = ''
        self.Cube.resetScore()
        self.lbl.text = "Score: 0"
        try:
            externalFile = open("external.py", "r")
            if os.stat("external.py").st_size > 0:
                data = externalFile.read()
            print("data loaded")
        except:
            print("File not found/can't be read")
        self.Cube.resetPos()
        if data is not '':
            self.Cube.setText(data)
        else:
            #self.input.activate()
            self.Cube.setText(self.input.text)

    def on_reset_click(self, widget):
        self.Cube.resetPos()
        self.win.visible = True
        self.scene.active_camera = self.Camera
        self.progress.percent = 0
    	#win_y=self.win.position[1]/self.size[1]
    	#print("reset", y)

    def update(self):
        self.input.activate()
        #self.input.system.focused_widget
        if (str(self.scene) != 'tut1'):
            self.popUpWindow.visible = False
        error = self.Cube.run()
        #print(str(bge.logic.getCurrentScene()))
        if error is -2:
            scene = bge.logic.getCurrentScene()
            if str(scene) == 'tut1':
                self.Cube.clearArrayOnSceneChange()
                scene.replace("tut2")
            if str(scene) == 'tut2':
                self.Cube.clearArrayOnSceneChange()
                scene.replace("tut3")
            if str(scene) == 'tut3':
                self.Cube.clearArrayOnSceneChange()
                scene.replace("pre_loops")
            if str(scene) == 'pre_loops':
                self.Cube.clearArrayOnSceneChange()
                scene.replace("loops")
        elif isinstance(error, str):
            self.console.text = str(error)
            self.progress.percent = 1
        elif isinstance(error, tuple):
            self.lbl.text = "Score: "+str(error[1])
        elif 0 < error <= 1:
            #print(error)
            self.console.text = "Console"
            self.progress.percent = error


def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        scene = bge.logic.getCurrentScene()
        ob_list = scene.objects
        # Setup the viewports
        # x = bge.render.getWindowWidth()
        #y = bge.render.getWindowHeight()
        cam = ob_list['Camera']
        print(cam)
        scene.active_camera = cam
        #cam.useViewport = True
        #cam.setViewport(0, 0, x, y)

        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System('themes/default')
        own['sys'].load_layout(SimpleLayout, None)
        mouse.visible = True

    else:
        own['sys'].run()
