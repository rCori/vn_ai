"""
Uses GenerativeAIController and ImageHandler to build the game. GameBuilder will
take in the command line input and the created project directory.
"""

import os
import shutil
from optionFlags import OptionFlags
from generativeAIController import GenerativeAIController
from scriptHandler import ScriptHandler
from imageHandler import ImageHandler

class GameBuilder:

    def __init__(self):
        self._gameName = ""
        self._options = 0
        self._prompt = ""
        self._generativeAIController = GenerativeAIController()
        self._scriptHandler = ScriptHandler()
        self._imageHandler = ImageHandler()

    # Getter and setter for name
    # Name is the name of the game being generated
    @property
    def gameName(self):
        return self._gameName
    
    @gameName.setter
    def gameName(self, gameName):
        self._gameName = gameName


    # Getter and setter for prompt
    # Prompt is the story script prompt we will be sending to the AI generation to make for us
    @property
    def prompt(self):
        return self._prompt
    
    @prompt.setter
    def prompt(self, prompt):
        self._prompt = prompt

    # Several settings can be enabled or disabled from user input
    # These options are stored as flags in _options
    def setOption(self, optionFlag, value):
        # If we are not setting a valid flag we should return early
        if(not optionFlag in OptionFlags):
            return False
        
        if value:
             self._options |= optionFlag
        else:
            self._options &= ~optionFlag
        
        # Return that the flag was set correctly
        return True

    # Copy the template project and replace game name
    def createProjectFromTemplate(self):
        if(self._options & OptionFlags.SKIP_PROJECT_GENERATION):
            print("SKIP_PROJECT_GENERATION set. Skipping project generation...")
            return
        if(os.path.exists('templateGame')):
            print("template game exists. Copying...")
            shutil.copytree('templateGame',self._gameName)
            self.fixProjectName()
        else:
            print("template game is not here")


    # Change the name of the 
    def fixProjectName(self):
        options = open(self._gameName+'/game/options.rpy', 'r')
        lines = options.readlines()
        for i, line in enumerate(lines):
            if "define config.name" in line:
                lines[i] = "define config.name = _(\""+self._gameName+"\")"
                break
        with open(self._gameName+'/game/options.rpy', 'w') as file:
            file.writelines(lines)


    # Create new script
    def createScript(self):
        if(self._options & OptionFlags.SKIP_SCRIPT_GENERATION):
            print("SKIP_SCRIPT_GENERATION set. Skipping new script generation...")
            return
        else:
            # Use GenerativeAIController to write the new script
            script = self._generativeAIController.generateScript()
            # With the script we can make the script handler
            self._scriptHandler.script = script
            self._scriptHandler.replaceScript(self._gameName,script)

    # Create all images
    def createImages(self):
        if(self._options & OptionFlags.SKIP_BACKGROUND_IMAGE_GENERATION):
            print("SKIP_BACKGROUND_IMAGE_GENERATION set. Skipping background image generation...")
        else:
            # Get list of all background images
            backgroundImages = self._scriptHandler.scanForBackgroundImages()
            # Iterate over all background images
            for backgroundImage in backgroundImages:
                # Generate each background image
                imageURL = self._generativeAIController.generateBackgroundScene(backgroundImage)
                # Get the exact location of where the webp file will be downloaded
                webpFilename = self._gameName+'/game/images/'+backgroundImage+'.webp'
                print("webpFilename to download: " + webpFilename)
                # Download each background image and convert to webp
                self._imageHandler.downloadImage(imageURL,webpFilename)
                self._imageHandler.convertWEBPBackgroundToPNG(webpFilename)