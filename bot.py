import json
import discord
import random
import os
import wikiquote
from canvasapi import Canvas
import urllib.request

# Example: "https://xyz.instructure.com/"
API_URL = "<YOUR CANVAS URL GOES HERE>""https://dvc.instructure.com/"
# Examplel: "9048385-teggjbkh45-y95yhgodjjk53hyuo58o054jgrnhgknh5"
API_KEY = "<YOUR CANVAS API TOKEN GOES HERE"
# Note: To get your Canvas token, go to your settings on canvas
# Then scroll down to "Approved Integrations"
# Then click + New Access Token to get your token
# This means that the bot will access your course through YOUR account
# and the bot can only see what you have access to.

# Some style for the embeded messages
CANVAS_COLOR = 0xe13f2b
CANVAS_THUMBNAIL_URL = "https://lh3.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180"

# Create the client
client = discord.Client()

# initialize canvas values
# put the course number (from the url) from your course here
cNum = 12345
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(cNum)

# feel free to modify this however you like
helpcanvas=discord.Embed(title = "Canvas Operations", description = "These are canvas operations you can use to access Assembly course Canvas modules and assignments.", color=CANVAS_COLOR)
helpcanvas.set_thumbnail(url=CANVAS_THUMBNAIL_URL)
helpcanvas.add_field(name="Accessing modules", value = "Modules can only be accessed up to the most currently unlocked module. Some module items may be inaccessible by the Assembly Bot",inline = False)
helpcanvas.add_field(name="Example: !week 6", value="This will return all of the module items within the week 6 module",inline = True)
helpcanvas.add_field(name="Example: !week 6 2", value="This will return a canvas link for the second item in the week 6 module.",inline = True)

# this finds a module containing the second part of the message
# for example, if you type !week introduction
# this will find a module (if there is one) that has the word
# "Introduction" in the module name/title. If your
# professor uses week numbers, !week 6 would get the module
# for week 6, works like a charm!
def getModule(message,quotes):
  splt = message.content.split()
  try:
    s = splt[1]
  except IndexError:
    return "Error processing module"
  modules = course.get_modules()
  for m in modules:
    if s in m.name:
      moduleEmb=discord.Embed(title=m.name,description=random.choice(quotes),color=CANVAS_COLOR)
      moduleEmb.set_thumbnail(url=CANVAS_THUMBNAIL_URL)
      urls = []
      x = m.get_module_items()
      c = 1
      for i in x:
        try:
          # some voodoo black magic
          u = i.url+"?access_token="+API_KEY
          with urllib.request.urlopen(u) as url:
            data = json.loads(url.read().decode())
          fieldName=str(c)+" ) "+data["title"]
          moduleEmb.add_field(name=fieldName,value=f"[Canvas Link]({i.html_url})",inline=True)
          urls.append(i.html_url)
          c += 1
        except AttributeError:
          continue
        except KeyError:
          continue
  # format the embed with .. placeholders
  # so that it's a clean multiple of 3
  if len(splt) == 2:
    if moduleEmb:
      b = (c-1)%3
      if b == 1:
        for r in range(2):
          moduleEmb.add_field(name="...",value="...",inline=True)
      elif b == 2:
        moduleEmb.add_field(name="...",value="...",inline=True)
      return moduleEmb
    else:
      return "Something went wrong...\nYou probably don't have access to that module yet."
  if len(splt) == 3:
    try:
      num = int(splt[2])
      return urls[num-1]
    except ValueError:
      return "Error with index provided"
  else:
    return "Your input isn't good"

# python should print a messasge if the bot logged on successfully
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('type !help for help'))

# whenever theres a message, this happens with the message passed to it
# if you don't know how discord.py functions work, look into that
# before using this bot. the bot might need some love and tinkering
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # gets some fun quotes!
    quotes = wikiquote.quotes("Programming")

    # uses that module function from earlier to make the embed and send it
    if message.content.startswith("!week"):
      await message.channel.send("Canvas API Call Initiated...Please stand by...")
      x = getModule(message,quotes)
      await message.channel.purge(limit=1)
      try:
        await message.channel.send(embed=x)
      except:
        await message.channel.send(x)

    # a little help message for those who need it
    if message.content.startswith('!helpcanvas'):
        await message.channel.send(embed=helpcanvas)

# get your token from the discord developer portal
# inside of the bot page where it says copy token
client.run('<PUT YOUR DISCORD BOT TOKEN HERE>')

# comit test
