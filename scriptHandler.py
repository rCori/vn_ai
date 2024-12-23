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
        return self.searchImages(scenePattern)

    # Find all lines in the script that display a background scene
    # Return a set of unique scene names
    def searchImages(self,scenePattern):
        print("searchImages scenePattern: " + scenePattern)
        sceneSet = set()
        # scenePattern = r"scene\b\s.*"
        for line in self.script.splitlines():
            print("line: " + line)
            match = re.search(scenePattern,line)
            if match:
                print("Match found: " + line)
                sceneSet.add(line[match.start():])
        print("Unique scene set: " + str(sceneSet))
        return sceneSet
    
    # Write the new script into the script.rpy file
    def replaceScript(self,newName, newScript):
        with open(newName+'/game/script.rpy', 'w') as f:
            f.write(newScript)