"""
OptionFlags defines which flags can be set from user input. This sets what parts of
project generation will be enabled or disabled
"""

from enum import IntFlag

class OptionFlags(IntFlag):
    SKIP_PROJECT_GENERATION = 1
    SKIP_SCRIPT_GENERATION = 2
    SKIP_BACKGROUND_IMAGE_GENERATION = 4
    SKIP_CHARACTER_IMAGE_GENERATION = 16