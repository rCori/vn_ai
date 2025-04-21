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

    gameBuilder.getBackgroundImages()
    gameBuilder.createBackgroundImages()
    gameBuilder.getCharacterImages()
    gameBuilder.createCharacterImages()



if __name__ == "__main__":
    main()