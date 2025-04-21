"""
ScriptHandler will handle everything to do with the script text after it is generated.
Script text will need to be edited, reread for information, and written back to the
game project script.rpy source file
"""

import re

class ScriptHandler:

    def __init__(self):
        self._script = None

    @property
    def script(self):
        return self._script
    
    @script.setter
    def script(self, script):
        self._script = script

    def scanForBackgroundImages(self):
        scenePattern = r"scene\b\s.*"
        sceneSet = self.searchImages(scenePattern)
        sceneSet = [scene.removeprefix("scene ") for scene in sceneSet]
        return sceneSet
    
    def scanForCharacterImages(self):
        scenePattern = r"show\b\s.*"
        removeSuffix = r" at.*"
        characterSet = self.searchImages(scenePattern)
        characterSet = set([scene.removeprefix("show ") for scene in characterSet])
        characterSet = set([re.sub(removeSuffix, "", scene) for scene in characterSet])
        return list(characterSet)
    
    # Search for the declaration of an image
    def scanForImageDeclaration(self, imageName):
        realFp = ""
        scenePattern = r"image " + imageName
        for line in self.script.splitlines():
            match = re.search(scenePattern,line)
            if match:
                imageDeclarationSplit = line.split("=")
                realFp = imageDeclarationSplit[1].strip().strip("\"")
                print("Found real filepath: " + realFp)
        return realFp

    # Find all lines in the script that display a background scene
    # Return a set of unique scene names
    def searchImages(self,scenePattern):
        sceneSet = set()
        # scenePattern = r"scene\b\s.*"
        for line in self.script.splitlines():
            match = re.search(scenePattern,line)
            if match:
                print("Match found: " + line)
                sceneSet.add(line[match.start():])
        print("Unique image set: " + str(sceneSet))
        return sceneSet
    
    # Write the new script into the script.rpy file
    def replaceScript(self, newName, newScript):
        with open(newName+'/game/script.rpy', 'w', encoding="utf-8") as f:
            f.write(newScript)
    
    # Read and return the current script.rpy file
    def openAndReturnScript(self,gameName):
        with open(gameName+'/game/script.rpy', 'r', encoding="utf-8") as f:
            return f.read()
