import discord
from discord.ext import commands, tasks
from datetime import *
import json
# import sqlite3

# db = sqlite3.connect("sheep_game.db")
# cursor = db.cursor()

# # Create Table
# cursor.execute("""CREATE TABLE IF NOT EXISTS sheep_game
#                     (name, score)""")



today = date.today()

client = discord.Client()
bots = commands.Bot(command_prefix='sheep')

# Change this to how long you want the round to run for
NUMBER_DAYS: int = 1

# Variable determines whether messages can still be dmed or not
some: bool = True

# Map which stores the name of the person to their answer
# <Name->String, Answer->String>
person_answer = {}

# Map which stores the answer to number of times it was repeated
# <Answer->String, Number of times->Integer>
answer_number = {}

# Questions array
questions = ["How do you do", "Water you doing"]

# Boolean Value used to communicate between "threads"
send_messages: bool = True

# Question Number
number: int = 1

@client.event
async def on_ready():
    """Do nothing when the bot is up and running"""
    print("The bot is up and running!")
    # Create a thread to run the time function
    # await first_question()
    time.start()
    await first_question()

async def first_question():
    global send_messages, number
    print("In first_question")
    channel = client.get_channel(id=851579255284564038)
    if send_messages == True:
        send_messages = False
        some = questions[0]
        del questions[0]
        await channel.send(f"Question No.{number}: {some}")

@client.event
async def on_message(message):
    """When a dm is sent, take note of the sender and what the sent"""
    # Make sure only dms are accepted
    print("Hello, in on_message")
    if message.author.dm_channel != None and isinstance(message.channel, discord.channel.DMChannel) and some == True:
        person_answer[message.author] = message.content
        if message.content not in answer_number:
            answer_number[message.content] = 1
        else:
            answer_number[message.content] += 1
        print(f'{person_answer} and {answer_number}')
    time()

@tasks.loop(seconds=100)
async def time():
    print("Hello, in time")
    print(len(questions))
    with open("time.txt", "r") as f:
        # Read the file
        time: str = f.read()
        # Look at the current date as jsonified string
        json_str = json.loads(time)
        # Create a datetime object from the jsonified string
        json_str = datetime.strptime(json_str, "%d-%m-%Y").date()

        # Get the current date
        today = date.today()
        today.strftime("%d/%m/%Y")

        # Create a timedelta object
        num_days_between_calculate = timedelta(days=NUMBER_DAYS)

        # If today's date - timedelta = json_str, then calculate
        if today - num_days_between_calculate == json_str:
            print("It's a good thing I'm here")
            # Write today's date to time.txt before calculating
            with open("time.txt", "w") as f:
                f.write(f"\"")
                f.write(today.strftime("%d-%m-%Y"))
                f.write(f"\"")
            await calculate()

async def print_scores():
    global send_messages, number
    # Test server ID
    channel = client.get_channel(id=851579255284564038)
    if send_messages == True:
        print("Inside print_scores")
        send_messages = False



        # # Test with sqlite

        # for row in cursor.execute("SELECT * FROM sheep_game"):
        #     await channel.send(f"{row[0]}: {row[1]}")

        

        # Get the text from data_scores.txt
        with open("data_scores.txt", "r") as f:
            data: str = f.read()
            file_read = json.loads(data) if data != "" else {}
            for i in file_read:
                await channel.send(f"{i}: {file_read[i]}")
        if len(questions) != 0:
            await channel.send(f"Question No.{number}: {questions[0]}")
            del questions[0]
        else:
            await channel.send("That was it for the sheep game")

async def calculate():
    global send_messages
    # Open data_scorex.txt
    print("Inside Calculate")
    # File Storage way
    file_read = {}
    with open("data_scores.txt", "r") as f:
        # Read the file
        data: str = f.read()
        file_read = json.loads(data) if data != "" else {}
    # file_read has the data in the form of <Name->String, Score->Integer>
    for i in person_answer:
        if i.name not in file_read:
            file_read[i.name] = 0
        file_read[i.name] += answer_number[person_answer[i]]
    print(f"{file_read} inside calculate")
    # Write the data to data_score.txt
    with open("data_scores.txt", "w") as f:
        f.write(json.dumps(file_read))

    # # SQLite way
    # file_read_2 = {}
    # for row in cursor.execute("SELECT * FROM sheep_game"):
    #     file_read_2[row[0]] = row[1]
    # for i in person_answer:
    #     # Change the value in the database
    #     query = f'UPDATE sheep_game set score = {answer_number[person_answer[i]]}'

    #     if i.name not in file_read_2:
    #         file_read_2[i.name] = 0
    #     file_read_2[i.name] += answer_number[person_answer[i]]
    

    send_messages = True
    await print_scores()


with open("token.txt", "r") as token_file:
    TOKEN = token_file.read()
    client.run(TOKEN)