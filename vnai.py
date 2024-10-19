# Copying a template project and inserting a generated script

import os
import shutil
import argparse
import re
from generativeAIController import GenerativeAIController
from imageHandler import ImageHandler

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--name')

    args = parser.parse_args()
    print (args.name)

    """
    openTemplate(args.name)
    
    generator = GenerativeAIController()
    
    script = generator.generateScript()
    replaceScript(args.name,script)
    """

    # Testing ability to read scene image uses in script
    originalScript = open(args.name+'/game/script.rpy', 'r')
    backgroundImages = list(searchImages(originalScript.readlines()))

    generator = GenerativeAIController()

    imageHandler = ImageHandler()
    imageUrl = generator.generateBackgroundScene(backgroundImages[0])
    webpFilename = args.name+'/game/images/'+backgroundImages[0][:-1]+'.webp'
    imageHandler.downloadImage(imageUrl, webpFilename)
    imageHandler.convertWEBPBackgroundToPNG(webpFilename)
    
    


def openTemplate(newName):
    if(os.path.exists('templateGame')):
        print("template game exists. Copying...")
        shutil.copytree('templateGame',newName)
        fixProjectName(newName)
    else:
        print("template game is not here")


def fixProjectName(newName):
    options = open(newName+'/game/options.rpy', 'r')
    lines = options.readlines()
    for i, line in enumerate(lines):
        if "define config.name" in line:
            lines[i] = "define config.name = _(\""+newName+"\")"
            break
    with open(newName+'/game/options.rpy', 'w') as file:
        file.writelines(lines)

def replaceScript(newName, newScript):
    with open(newName+'/game/script.rpy', 'w') as f:
        f.write(newScript)

def searchImages(script):
    sceneSet = set()
    scenePattern = r"scene\b\s.*"
    for line in script:
        match = re.search(scenePattern,line)
        if match:
            sceneSet.add(line[match.start():])
    print("Unique scene set: " + str(sceneSet))
    return sceneSet


if __name__ == "__main__":
    main()