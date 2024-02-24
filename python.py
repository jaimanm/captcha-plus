import random

ins = input()

bot = random.choice(["rock", "paper", "scissors"])

print(bot)
if (ins == "rock"):
    if (bot == "rock"):
        print('tie')
    elif (bot == "paper"):
        print("you lose")
    else:
        print("you win")
elif (ins == "paper"):
    if (bot == "rock"):
        print('you win')
    elif (bot == "paper"):
        print('tie')
    else:
        print('you lose')
else:
    if (bot == "rock"):
        print("you lose")
    elif (bot == "paper"):
        print("you win")
    else:
        print("you lose")

