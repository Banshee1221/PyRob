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
        self.cam1 = ob_list['Camera']
        self.cam2 = ob_list['Cam_Zoomed']

        self.reset_button = bgui.FrameButton(self.frame, text='Reset', size=[.07, .04], pos=[.08, .0],
                                             options=bgui.BGUI_DEFAULT)
        self.reset_button.on_click = self.on_reset_click
        # self.button.on_click = self.hide_show

        # A themed frame
        self.win = bgui.Frame(self, size=[0.5, 0.95], pos=[0, 0.05],
                              options=bgui.BGUI_DEFAULT)

        self.rightWin = bgui.Frame(self, size=[0.5, 0.25], pos=[0.5, 0.05],
                                   options=bgui.BGUI_DEFAULT)
        

        # A button
        self.run_button = bgui.FrameButton(self.frame, text='Run', size=[.07, .04], pos=[0, .0],
                                           options=bgui.BGUI_DEFAULT)

        # Setup an on_click callback for the image
        self.run_button.on_click = self.on_run_click

        # Add a label
        #self.lbl = bgui.Label(self, text="I'm a label!", pos=[.75, .5],
        #	sub_theme='small', options = bgui.BGUI_DEFAULT)

        # A couple of progress bars to demonstrate sub themes
        self.progress = bgui.ProgressBar(self.frame, percent=0.0, size=[0.5, 0.03], pos=[.15, 0.01],
                                         sub_theme="Progress", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

        #self.health = bgui.ProgressBar(self.win, percent=0.5, size=[0.92, 0.02], pos=[0, 0.14],
        #									sub_theme="Health",	options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

        # A few TextInput widgets
        self.input = bgui.TextInput(self.win, text="", size=[.93, .98], pos=[.05, .01],
                                    input_options=bgui.BGUI_INPUT_NONE, options=bgui.BGUI_DEFAULT)

        self.console = bgui.TextBlock(self.rightWin, text="console", size=[.96, .98], pos=[.01, .01],
                                      options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

        self.lines = []
        incriment = .0258
        start = 0.9675
        count = 1
        for i in range(20):
            self.lines.append(bgui.Label(self.win, text=str(count) + ".", pos=[.01, start], options=bgui.BGUI_DEFAULT))
            start = start - incriment
            count = count + 1
        #self.lines.append(bgui.Label(self.win, text="2.", pos=[.01, .94], options = bgui.BGUI_DEFAULT))
        self.input.activate()
        #self.input.on_enter_key = self.on_run_click


        # A counter property used for the on_img_click() method
        #self.counter = 0

        self.helpWin = bgui.Frame(self, size=[0.75, .9], pos=[.5, 1],
                              options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

        self.helpText = bgui.TextBlock(self.helpWin, text="Help:\n\n"+
        	"Movement:\nmoveUp()\nmoveDown()\nmoveLeft()\nmoveRight()"+
        	"\n\nLoops:\nfor\nwhile"+
        	"\n\nConditionals:\nif with keyword 'not on'"+
        	"\n\nFunctions:\nobject()\nground()\npickup()", size=[.9, .9], pos=[.0, .0],
    	                      options = bgui.BGUI_DEFAULT |bgui.BGUI_CENTERX | bgui.BGUI_CENTERY)

        self.help_button = bgui.FrameButton(self, text='Help', size=[.07, .04], pos=[0.93, .96],
                                             options=bgui.BGUI_DEFAULT)
        self.help_button.on_click = self.hide_show

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

    def on_run_click(self, widget):
        #print(os.getcwd())
        self.scene.active_camera = self.cam2
        #self.win.visible = False
        externalFile = ''
        data = ''
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
            self.input.activate()
            self.Cube.setText(self.input.text)

    def on_reset_click(self, widget):
        self.Cube.resetPos()
        self.win.visible = True
        self.scene.active_camera = self.cam1
        self.console.text = "Console"
        self.progress.percent = 0
    	#win_y=self.win.position[1]/self.size[1]
    	#print("reset", y)

    def update(self):
        self.input.activate()
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
                scene.replace("loops")
        elif isinstance(error, str):
            self.console.text = str(error)
            self.progress.percent = 1
        elif 0 < error <= 1:
            print(error)
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
