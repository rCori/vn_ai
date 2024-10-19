import re
from openai import OpenAI

class GenerativeAIController:

    def __init__(self):
        self.client = OpenAI()

    def generateScript(self):
        completion =self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system", "content":"You are a helpful assistant."},
                {
                    "role":"user",
                    "content":"The following is a story prompt for a visual novel. \
                                Write this as a renpy script file. Code only:\
                                \"Omar is an aspiring Diddy Kong Racing for N64 speedrunner. \
                                He is close to getting the world record and practices every day. \
                                There is only one problem. His crush Patty Mayonnaise. He needs to ask her to the Winter Formal Dance coming up and he's so nervous he can hardly sleep. \
                                Will Omar get Patty and first place? Or will his rival Rodger leave him in the dust\""
                }
            ]
        )
        content = self.cleanScript(completion.choices[0].message.content)
        return content
    
    def generateBackgroundScene(self,bgSceneName):
        response = self.client.images.generate(
            model="dall-e-2",
            prompt="I have a renpy visual novel script. There is a background with this name:\
                    \"bg room\" \
                    Make a background image based on this name. Give it a vibrant anime style",
            n=2,
            size="1024x1024",
            quality="standard",
        )
        image_url = response.data[0].url
        print(image_url)
        return image_url

    # Take trailing quotes off of the beginning and end of the content if they exist.
    def cleanScript(self,content):
        """
        if(content.startswith("```renpy")):
            print("\"```renpy\" was found at the start of content")
            content = content[len("```renpy"):]

        if (content.endswith("```")):
            print("\"```\" was found at the end of content")
            content = content[:len(content)-3]
        """
        # Regex to match ` ```renpy` at the start or ` ``` ` with optional whitespace at the end
        #pattern = r"^```renpy\s*|```\s*$"
        #cleaned_content = re.sub(pattern,'\n', content)
        cleaned_content = re.search(r'```renpy(.*?)```', content, re.DOTALL).group(1)
        return cleaned_content