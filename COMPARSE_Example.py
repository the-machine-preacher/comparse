from comparse import comparse
query = comparse(False)
query.add_argument('points', int, 27, "Number of points used in point-buy")
query.add_argument('str', int, 8, "Strength score")
query.add_argument('dex', int, 8, "Dexterity score")
query.add_argument('con', int, 8, "Constitution score")
query.add_argument('wis', int, 8, "Wisdom score")
query.add_argument('int', int, 8, "Intelligence score")
query.add_argument('cha', int, 8, "Charisma score")
query.add_argument('skills', str, '', "List of skills separated by a coma ','")
query.add_argument('languages', str, 'Common', "List of languages separated by comas ','")
query.add_argument('name', str, 'Jane Doe', "Player Character")
query.add_argument('AC', int, 10, "Armor Class")
query.add_argument('HP', int, 0, "Health Points")
query.add_argument('initiative', int, 0, "Initiative")
query.add_argument('prof_bonus', int, 2, "Proficiency bonus")
query.add_argument("-", int, 10, "Player Character")
query.add_argument("d", int, 20, "Dice type")

'''REMOVE THE HASH-TAGS TO TEST SELECTED LINES OF CODE'''
message1 = "1d20+3"
message1 = "Naame: Emily Dragonclaw, points=27, str=17, dex: 15, con: 13, int: 8, wis: 9, cha: 12, +3, skills: [Animal Handling, Athletics, History, Intimidation, Persuasion]"
#message1 = "record dex 15"
message2 = "exclude_content=pineapple pear flint, !log_this_channel example.txt, content_filter=posted, log_attachments=false, log_author=false, !int_variable=26"
message2 = "exclude_content=pineapple pear orange, points=27, str=17, dex: 15, con: 13, int: 8, wis: 9, cha: 12, skills: [Animal Handling, Athletics, History, Intimidation, Persuasion]"
message2 = "skills: insight, persuasion, intimidation, athletics, survival"
message2 = "Name Rayna, Skills: insight, persuasion 3, intimidation 10, athletics 001, procrastinating, survival"
message = 'roll 3d 4 - 5 with - 60str, without str 78'
#message = "languages Elvish, Undercommon, Abyssal, Common"

#question = query.parse(message1)['dex']
#exclude_content = query.parse(message2)['exclude_content']

#print(question)
#print(query.show_message_attributes())
#print(query.parse(message)['d'])
#print(query.parse(message2)['name'], query.parse(message2)['skills'], query.parse(message2)['+'])
#print(query.parse(message1)['name'])
print(query.parse(message)['-'], query.parse(message)['str'])
#print(query.parse(message)['languages'])