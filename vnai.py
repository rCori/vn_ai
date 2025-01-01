# Copying a template project and inserting a generated script

import os
import shutil
import argparse
import re
from optionFlags import OptionFlags
from generativeAIController import GenerativeAIController
from imageHandler import ImageHandler
from scriptHandler import ScriptHandler
from gameBuilder import GameBuilder

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('--skip-project-generation', help='Do not generate a new project if one with the same name already exists',
                        action="store_true")
    parser.add_argument('--skip-script-generation', help="Do not generate new script",
                        action="store_true")
    parser.add_argument("--skip-background-image-generation", help='Do not generate new background images',
                        action="store_true")
    parser.add_argument("--skip-character-image-generation", help='Do not generate new character images',
                        action="store_true")
    args = parser.parse_args()

    gameBuilder = GameBuilder()
    gameBuilder.gameName = args.name
    gameBuilder.setOption(OptionFlags.SKIP_PROJECT_GENERATION, args.skip_project_generation)
    gameBuilder.setOption(OptionFlags.SKIP_SCRIPT_GENERATION, args.skip_script_generation)
    gameBuilder.setOption(OptionFlags.SKIP_BACKGROUND_IMAGE_GENERATION, args.skip_background_image_generation)
    gameBuilder.setOption(OptionFlags.SKIP_CHARACTER_IMAGE_GENERATION, args.skip_character_image_generation)

    gameBuilder.createProjectFromTemplate()
    gameBuilder.createScript()
    # gameBuilder.createImages()

    gameBuilder.getBackgroundImages()
    gameBuilder.createBackgroundImages()
    gameBuilder.getCharacterImages()
    gameBuilder.createCharacterImages()


    """  
    generator = GenerativeAIController()

    # Create the new project directory
    if not (args.skip_project_generation and os.path.exists(args.name)):
        createProjectFromTemplate(args.name)
    else:
        print("Skipping new project creation. Project created previously")
    
    # Use GenerativeAIController to write the new script
    if not args.skip_script_generation:
        script = generator.generateScript()
        replaceScript(args.name,script)
    else:
        print("Skipping new script generation...")

    scriptHandler = ScriptHandler(script)

    # Grab the names of all images in the script
    originalScript = open(args.name+'/game/script.rpy', 'r')
    backgroundImages = list(searchImages(originalScript.readlines()))

    # Generate one of the background images pu
    if not args.skip_background_image_generation:
        imageHandler = ImageHandler()
        imageUrl = generator.generateBackgroundScene(backgroundImages[0])
        webpFilename = args.name+'/game/images/'+backgroundImages[0][:-1]+'.webp'
        imageHandler.downloadImage(imageUrl, webpFilename)
        imageHandler.convertWEBPBackgroundToPNG(webpFilename)
    else:
        print("Skipping background image generation...") 
    """
    

def createProjectFromTemplate(newName):
    if(os.path.exists('templateGame')):
        print("template game exists. Copying...")
        shutil.copytree('templateGame',newName)
        fixProjectName(newName)
    else:
        print("template game is not here")

# Change the name of the 
def fixProjectName(newName):
    options = open(newName+'/game/options.rpy', 'r')
    lines = options.readlines()
    for i, line in enumerate(lines):
        if "define config.name" in line:
            lines[i] = "define config.name = _(\""+newName+"\")"
            break
    with open(newName+'/game/options.rpy', 'w') as file:
        file.writelines(lines)

# Write the new script into the script.rpy file
def replaceScript(newName, newScript):
    with open(newName+'/game/script.rpy', 'w') as f:
        f.write(newScript)

# Find all lines in the script that display a background scene
# Return a set of unique scene names
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