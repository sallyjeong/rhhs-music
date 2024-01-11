import os
import datetime
import secrets
import asyncio
import string
import json

import discord
from discord.ext import commands

import quart
from quart import render_template, send_from_directory, request, session
from hypercorn.asyncio import serve
from hypercorn.config import Config
import uvloop
from quart_compress import Compress

from google.oauth2 import id_token
from google.auth.transport import requests

from discord_roles import roles

uvloop.install()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

config = Config()
config.bind = ['0.0.0.0']
config.worker_class = ['uvloop']

divider_roles = [
  879566184415129664, # across the ages
  879566613475622923, # ensembles
  879566488175001622, # instruments
  879568116466716692, # genres
]

class_roles = {
  2022 : 879555314360389673,
  2023 : 879555226246471711,
  2024 : 879555335784910878,
  2025 : 879555353740738621,
}

classlists = {}

for year in [2022, 2023, 2024, 2025]:
  with open('classlists/' + str(year)+'.txt') as f:
    classlists[year] = f.read().split('\n')

bot = commands.Bot('$', intents=discord.Intents.all())

app = quart.Quart(__name__, static_folder="assets/")
app.secret_key = os.environ['quart_key']
Compress(app)

global users_auth, users_codes, users_verify, users
users_auth = {} # random key : dict(user info)
users_codes = {} # same random key : str(user's verification code)
users_verify = {} # user's code : tuple(expiration time, bool: RAIDER, tuple(dict(user info))
users = [] # (timestamp, discord user id, gapps email (rhhs students only))

with open('discord_user_log.json') as f:
  users = json.load(f)

pages = [
  'about-us',
  'courses',
  #'discord',
  'ensembles',
  'events',
  'for-students',
  'concerts',
  'house-events',
  'staff',
  'music-council',
  #'gallery',
  # 'elements', # for reference
]

async def expire_auths():
  while True:
    for key, value in list(users_auth.items()):
      if datetime.datetime.fromtimestamp(value['exp']) >= datetime.datetime.now():
        try:
          del users_codes[key]
        except:
          pass
        finally:
          del users_auth[key]
    for key, value in list(users_verify.items()):
      if value[0] >= datetime.datetime.now():
        del users_verify[key]
    await asyncio.sleep(60)

@app.before_serving
async def startup():
  loop = asyncio.get_event_loop()
  loop.create_task(expire_auths())

@app.after_request
async def add_expires_header(response):
    hours = 72
    then = datetime.datetime.now() + datetime.timedelta(hours=hours)
    response.headers['Expires'] = then.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route("/")
async def index():
  return await render_template("index.html")

@app.route("/<path:path>")
async def serve_pages(path):
  if path in pages:
    return await render_template(path+".html")
  else:
    return await render_template("404.html")

@app.route('/images/<path:path>')
async def send_image(path):
    return await send_from_directory('images', path)

# The following commented code is for the RHHS Music Discord bot, used for authenticating members through the website and into the Discord. 
'''
@app.route('/discord/<path:path>', methods=['GET', 'POST'])
async def serve_discord(path):
  if path == 'step1' and request.method == 'GET':
    return await render_template("step1.html")
  elif path == 'step2':
    if session.get('g_login') in users_auth.keys():
      return await render_template("step2.html")
    elif request.method == 'POST':
      try:
        form = (await request.form)
        csrf_token_cookie = request.cookies.get('g_csrf_token')
        csrf_token_body = form.get('g_csrf_token')
        if not csrf_token_cookie or not csrf_token_body or csrf_token_cookie != csrf_token_body:
            raise ValueError('Failed to verify cookie.')
        token = form['credential']
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '1060749361997-4bl65nkgjct2p4puctfv4s4vnm9sai4u.apps.googleusercontent.com')
        if idinfo['hd'] != 'gapps.yrdsb.ca':
          raise ValueError('Not a YRDSB account.')
        while True:
          key = secrets.token_hex(32)
          if key not in users_auth.keys():
            users_auth[key] = idinfo
            break
        session.permanent = True
        session['g_login'] = key
        return await render_template("step2.html")
      except:
        return await render_template("discord-failed.html")
    else:
      return await render_template("discord-failed.html")
  elif path == 'verified':
    if request.method == 'POST' and (session.get('g_login') in users_auth.keys()) and ((await request.form).get('code') == 'rhhs_supremacy'):
      if session.get('g_login') not in users_codes.keys():
        while True:
          verify_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))
          if verify_code not in users_verify.keys():
            break
        users_codes[session.get('g_login')] = verify_code
        users_verify[verify_code] = (datetime.datetime.now()+datetime.timedelta(days=1), True, users_auth[session.get('g_login')])
        #print(verify_code, users[verify_code])
      else:
        verify_code = users_codes[session.get('g_login')]
      return await render_template('discord-verified.html', code=verify_code)
    return await render_template('discord-failed.html')
  elif path == 'visitor':
    while True:
      verify_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))
      if verify_code not in users_verify.keys():
        break
    users_verify[verify_code] = (datetime.datetime.now()+datetime.timedelta(days=1), False)
    return await render_template('discord-visitor.html', code=verify_code)
  elif path == 'alumni':
    return await render_template('discord-alumni.html')
  else:
    return await render_template("404.html")


@bot.event
async def on_ready():
  config = Config()
  config.bind = ['0.0.0.0']
  config.worker_class = ['uvloop']
  await serve(app, config)

@bot.event
async def on_message(message):
  if message.channel.id == 863441834827186187:
    h = message.content.strip()
    #print(h, users_verify)
    if h in users_verify.keys():
      if users_verify[h][1]:
        await message.author.add_roles(discord.Object(879554454276415529)) # RAIDER role
        await message.author.edit(nick=users_verify[h][2]['name'])
      else:
        await message.author.add_roles(discord.Object(879556019687161896)) # visitor role
      for year, emails in classlists.items():
        if users_verify[h][1]:
          if users_verify[h][2]['email'] in emails:
            await message.author.add_roles(discord.Object(class_roles[year]))
            break
      await message.author.add_roles(*[discord.Object(role_id) for role_id in divider_roles])
      if users_verify[h][1]:
        users.append(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"), message.author.id, users_verify[h][2]['email'])
        with open('discord_user_log.json', 'w', encoding='utf-8') as f:
          json.dump(users, f, indent=4)
      del users_verify[h]
    await message.delete()

@bot.event
async def on_raw_reaction_add(payload):
  await bot.get_guild(863440627038814238).get_member(payload.user_id).add_roles(discord.Object(roles[payload.message_id][str(payload.emoji)]))

@bot.event
async def on_raw_reaction_remove(payload):
  await bot.get_guild(863440627038814238).get_member(payload.user_id).remove_roles(discord.Object(roles[payload.message_id][str(payload.emoji)]))


bot.run(os.environ['discord_token']) # Discord bot token - KEEP SAFE
'''

# Use the below line when the above Discord block is commented to only run the website. 
asyncio.run(serve(app, config))