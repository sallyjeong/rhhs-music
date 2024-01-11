# Run this file once to set up reaction roles on the RHHS Music Discord server.

roles = {
  901310503186497556 : {
    '🎟️' : 879565193720528896, 
    '🌬️' : 879565409341288568,
    '🥇' : 879565565491040323,
    '🎤' : 879568927074709514,
    '🤒' : 879565677999046676,
    },

  901310503777861653 : {
    '🥖' : 879553704330661898,
    '🥅' : 879553657014726688,
    '🐟' : 879553764879659088,
    '🏹' : 879554077023957062,
    '🔜' : 879554101246038027,
    '🎷' : 879554126659346462,
    '🔟' : 879554151581904936,
    '🐻' : 879554177007747072,
    '📯' : 879554205738750033,
    '🎺' : 879553726979915807,
    '📎' : 879553746181447731,
    '☎️' : 879554227079376978,
    '🧪' : 879554295417159710,
    '🥁' : 879553444480966716,
  },

  901310504394424340 : {
    '🎤' : 879564382600855553,
    '🎹' : 879555762639233084,
    '🎻' : 879555794432041012,
    '📱' : 901305822578098227,
    '🎸' : 901302927078076476,
    '🙉' : 900229567501987851,
  },

  901310504423792702 : {
    '🤖' : 879568305076183060,
    '🏛️' : 879568391579533322,
    '👐' : 879568580881027093,
    '🥤' : 879568614636810310,
  },
}

if __name__ == '__main__':
  import nextcord
  from nextcord.ext import commands

  bot = commands.Bot('$')

  embeds = [
    nextcord.Embed(title="Across the Ages", description="Class roles are organized by the year you are set to graduate from high school. If you verified as a RHHS Music student, you may have noticed that you already have your class role. Class roles grant you access to special, private channels with everyone else in your grade. If you graduated before 2021, being an RHHS Music alumni is also a class role. If you're missing a class role yet, feel free to talk to a Music Council member and they'll be happy to help!").set_author(name="Auto-roles"),

    nextcord.Embed(title="Ensembles", description="""**Are you part of an ensemble at RHHS?** No worries, we have roles for those too! Ensemble roles also unlock special, private channels for your respective ensemble. Just react with the emoji for the ensembles you're in (and ONLY the ensembles you're in).
    
    > 🎟️ - Concert Band
    > 🌬️ - Symphonic Winds
    > 🥇 - Gold Band
    > 🎤 - Vocal Fusion
    > 🤒 - Gold Fever
    """).set_author(name="Reaction roles").set_footer(text="Part of an ensemble that's not on here? Feel free to tell us about it!"),

    nextcord.Embed(title="Instruments", 
    description='''**Which instruments do you play?** React below with the emojis for the instruments you play to get that instrument's role! These instrument roles will unlock special, private channels for people who play the same instrument. Please be respectful and only get roles for the instruments you actually play.
    
    > 🥖 - Flute
    > 🥅 - Clarinet
    > 🐟 - Bass Clarinet
    > 🏹 - Oboe
    > 🔜 - Bassoon
    > 🎷 - Alto Sax
    > 🔟 - Tenor Sax
    > 🐻 - Bari Sax
    > 📯 - French Horn
    > 🎺 - Trumpet
    > 📎 - Trombone
    > ☎️ - Euphonium
    > 🧪 - Tuba
    > 🥁 - Percussion
    ''').set_author(name="Reaction roles"),

    nextcord.Embed(description='''> 🎤 - Vocal
    > 🎹 - Piano
    > 🎻 - Violin/Viola
    > 📱 - Cello
    > 🎸 - Plucked Strings
    > 🙉 - Recorder
    ''').set_footer(text="Do you play an instrument that's not on here? Feel free to tell us about it, we're all about equal instrument representation!"),

    nextcord.Embed(title="Interests", 
    description='''And last but certainly not least, what kind of music are you into? Just like the other roles, these interest roles will unlock a special, private channel where you can chat with other people who like the same stuff. Awesome, right?
    
    > 🤖 - Electronic
    > 🏛️ - Classical
    > 👐 - Jazz
    > 🥤 - Pop
    ''').set_author(name="Reaction roles").set_footer(text="Like something that's not on here? Feel free to tell us about it!"),

  ]

  @bot.event
  async def on_ready():
    '''
    for embed in embeds:
      await bot.get_channel(895818784517017620).send(embed=embed)
    '''
    for msg_id, emojis in roles.items():
      msg = await bot.get_channel(895818784517017620).fetch_message(msg_id)
      for emoji in emojis.keys():
        await msg.add_reaction(emoji)
    
    

  bot.run('ODg4MTg4MzYzNjc1NDMwOTIz.YUPD3w.Cfpl-pjQYiYbuL2b_UYe80_ZUtk') # Discord bot token - KEEP SAFE