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
        characterSet = self.searchImages(scenePattern)
        characterSet = [scene.removeprefix("show ") for scene in characterSet]
        return characterSet

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
    def replaceScript(self,newName, newScript):
        with open(newName+'/game/script.rpy', 'w', encoding="utf-8") as f:
            f.write(newScript)