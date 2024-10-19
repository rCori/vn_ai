label start:
    # Scene setup
    scene bg room
    with dissolve

    "Omar is an aspiring Diddy Kong Racing speedrunner, dedicated to mastering every track and beating the world record."

    "He practices every day, his eyes glued to the screen, fingers dancing across the controller."

    "But there's one thing that keeps him from fully concentrating on his runs..."

    # Introduce Patty Mayonnaise
    scene bg school_hallway
    with dissolve

    "Patty Mayonnaise, the girl of his dreams, is the reason for his distractions. She's beautiful, smart, and always kind to everyone."

    "With the Winter Formal Dance coming up, Omar knows he has to ask her, but he's never been this nervous in his life."

    # Omar's inner thoughts
    "How can I ask her? What if she says no? What if Rodger, my rival, asks her first?"

    # Choice: Ask Patty Mayonnaise
    menu:
        "Ask Patty Mayonnaise to the dance":
            jump ask_patty
        
        "Focus on speedrunning and ignore the dance":
            jump focus_speedrunning

label ask_patty:
    # Scene: Omar approaches Patty
    scene bg school_cafeteria
    with dissolve

    "Omar gathers all his courage and decides to approach Patty in the cafeteria."

    "Patty is chatting with her friends, and Omar's heart races. What if this is his moment?"

    "He takes a deep breath and musters the words."

    "Hey, Patty! Um, I was wondering if you would like to go to the Winter Formal with me?"

    # Response: Patty's reaction
    "Patty looks at him, a smile spreading across her face."

    menu:
        "Sure, I'd love to go!":
            jump patty_positive
        
        "Oh, I'm really busy...":
            jump patty_negative

label focus_speedrunning:
    # Scene: Returning to speedrunning
    scene bg room
    with dissolve

    "Omar shakes off his feelings and returns to practicing Diddy Kong Racing."
    
    "He focuses all his energy on his runs, trying to forget about the dance."

    "But every time he closes his eyes, he sees Patty's smile."

    # Choice: Keep practicing or take a break to think about Patty
    menu:
        "Keep practicing":
            jump keep_practicing
        
        "Take a break and think about Patty":
            jump think_about_patty

label patty_positive:
    # Scene: Dancing with Patty
    scene bg dance
    with dissolve

    "Patty beams at him, excitement lighting up her eyes."

    "Great! I can't wait! It'll be so much fun!"

    "Omar feels a wave of relief wash over him. Maybe he can have both�Patty and the world record!"

    "Now, he just has to keep practicing..."

    jump end_game

label patty_negative:
    # Scene: Feeling disappointed
    scene bg school_hallway
    with dissolve

    "Omar's heart sinks as Patty politely declines his invitation."

    "Oh, that's okay... I understand."

    "He watches her walk away, feeling dejected but determined to focus on his speedrunning."

    jump end_game

label keep_practicing:
    "Days pass, and Omar channels his feelings into his speedrunning."

    "He practices tireless hours, pushing himself to the limit against Rodger's best times."

    "But deep down, he wishes he could have the dance with Patty to celebrate his victory."

    jump end_game

label think_about_patty:
    "Omar takes a break, sitting on his bed deep in thought."

    "He realizes that whether he gets the world record or not, he still wishes he could be with Patty."

    jump end_game

label end_game:
    "Will Omar get the world record? Will Rodger leave him in the dust? And what about the dance with Patty?"

    # End game prompt
    "The future awaits, filled with possibilities..."

    return
