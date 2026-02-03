"""
Uses GenerativeAIController and ImageHandler to build the game. GameBuilder will
take in the command line input and the created project directory.
"""

import os
import shutil
import time
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
        self._imageCountRateLimit = 2

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
            self._scriptHandler.script = self._scriptHandler.openAndReturnScript(self._gameName)
            return
        else:
            # Use GenerativeAIController to write the new script
            script = self._generativeAIController.generateScript()
            # With the script we can make the script handler
            self._scriptHandler.script = script
            self._scriptHandler.replaceScript(self._gameName,script)

    # Get all background images
    def getBackgroundImages(self):
        # Get list of all background images
        self.backgroundImageNames = self._scriptHandler.scanForBackgroundImages()
        

    def getCharacterImages(self):
        # Get list of all character images
        self.characterImageNames = self._scriptHandler.scanForCharacterImages()
        print("Character images to generate: " + ", ".join(self.characterImageNames))

    # Create background images
    def createBackgroundImages(self):
        if(self._options & OptionFlags.SKIP_BACKGROUND_IMAGE_GENERATION):
            print("SKIP_BACKGROUND_IMAGE_GENERATION set. Skipping background image generation...")
        else:
            rateLimitCounter = 0
            # Iterate over all background images
            for i in range(len(self.backgroundImageNames)):
                image_data = self._generativeAIController.generateBackgroundScene(self.backgroundImageNames[i])
                newFilepath = self._scriptHandler.scanForImageDeclaration(self.backgroundImageNames[i])
                self._imageHandler.saveImageData(self._gameName+'/game/'+newFilepath,image_data)
                # # Generate each background image
                # imageURL = self._generativeAIController.generateBackgroundScene(self.backgroundImageNames[i])
                # # Get the exact location of where the webp file will be downloaded
                # webpFilename = self._gameName+'/game/images/'+self.backgroundImageNames[i]+'.webp'
                # # Check for image declaration
                # newFilepath = self._scriptHandler.scanForImageDeclaration(self.backgroundImageNames[i])
                # # Download each image
                # self._imageHandler.downloadImage(imageURL,webpFilename)
                # # Convert downloaded image to format we can use, png
                # self._imageHandler.convertWEBPBackgroundToPNG(webpFilename,self._gameName+'/game/'+newFilepath)
                # # With a new image created and downloaded we must increment the rateLimitCounter
                # rateLimitCounter = rateLimitCounter + 1
                # # If the rate limit has been hit, pause for a full minute before continuinge
                # if(rateLimitCounter == self._imageCountRateLimit):
                #     print("Sleeping for rate limit")
                #     time.sleep(60)
                #     rateLimitCounter = 0

    # Create character images
    def createCharacterImages(self):
        if(self._options & OptionFlags.SKIP_CHARACTER_IMAGE_GENERATION):
            print("SKIP_CHARACTER_IMAGE_GENERATION set. Skipping character image generation...")
        else:
            rateLimitCounter = 0
             # Iterate over all character images
            for i in range(len(self.characterImageNames)):
                # Generate each character image
                imageURL = self._generativeAIController.generateCharacterImage(self.characterImageNames[i])
                # Get the exact location of where the webp file will be downloaded
                webpFilename = self._gameName+'/game/images/'+self.characterImageNames[i]+'.webp'
                # Check for image declaration
                newFilepath = self._scriptHandler.scanForImageDeclaration(self.characterImageNames[i])
                # Download each image
                self._imageHandler.downloadImage(imageURL,webpFilename)
                # Convert downloaded image to format we can use, png
                self._imageHandler.convertWEBPBackgroundToPNG(webpFilename,self._gameName+'/game/'+newFilepath)
                # With a new image created and downloaded we must increment the rateLimitCounter
                rateLimitCounter = rateLimitCounter + 1
                # If the rate limit has been hit, pause for a full minute before continuinge
                if(rateLimitCounter == self._imageCountRateLimit):
                    print("Sleeping for rate limit")
                    time.sleep(60)
                    rateLimitCounter = 0

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