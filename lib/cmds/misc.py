import json
from irc.bot import SingleServerIRCBot

NAME = 'YOUR_BOT_NAME'
OWNER = 'CHANNEL_NAME'
file = 'death.json'


class Game(SingleServerIRCBot):
    def __init__(self):
        self.game = []
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = "CLIENT_ID"
        self.TOKEN = "TOKEN"
        self.CHANNEL = f"#{OWNER}"

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def setgame(self, user, *message):
        message_input = []
        if user["name"].lower() == 'USER_1' or user["name"].lower() == 'USER_2':
            if '()' in str(message):
                pass
            elif 'Just' and 'Chatting' in str(message):
                pass
            elif 'Music' in str(message):
                pass
            else:
                for i in message:
                    message_input += i

                if len(message_input) > 1:
                    self.game = ','.join(message).replace(',', ' ')
                elif len(message_input) <= 1:
                    self.game = message
                self.send_message(f'Game set to {self.game}')
                all_games = []
                print(self.game)
                with open(file, 'r') as json_file:
                    data = json.load(json_file)
                    name_data = (data["games"])
                    for i in name_data:
                        all_games.append(i['title'])
                    print(all_games)
                    if self.game in all_games:
                        pass
                    else:
                        with open('death.json') as json_file:
                            data = json.load(json_file)
                            temp = data["games"]
                            y = {"title": str(self.game), 'deaths': 0}
                            temp.append(y)
                        write_json(data)
        else:
            self.send_message(f'You do not have permission to do this')

    def currentgame(self, user):
        try:
            self.send_message(self.game)
        except AttributeError:
            self.send_message(f'No game set.')

    def listgames(self, user):
        file = 'death.json'
        games = ''
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            name_data = (data["games"])

            for i in name_data:
                title = (i["title"])
                games += f'{title}, '

            self.send_message(f'Game List: {games}')

    def dead(self, user):
        try:
            if user["name"].lower() == 'USER_1' or user["name"].lower() == 'USER_2':
                with open(file, 'r+') as json_file:
                    data = json.load(json_file)
                    name_data = (data["games"])

                    for i in name_data:
                        if self.game == i['title']:
                            i['deaths'] += 1
                            if i["deaths"] == 1:
                                self.send_message(
                                    f'Deaths Updated. You have died {i["deaths"]} time playing {self.game}.')
                            else:
                                self.send_message(
                                    f'Deaths Updated. You have died {i["deaths"]} times playing {self.game}.')
                        write_json(data)

            else:
                self.send_message(f'You do not have permission to do this')
        except AttributeError:
            self.send_message(f'No game set.')

    def deletedead(self, user):
        try:
            if user["name"].lower() == 'USER_1' or user["name"].lower() == 'USER_2':
                with open(file, 'r+') as json_file:
                    data = json.load(json_file)
                    name_data = (data["games"])

                    for i in name_data:
                        if self.game == i['title']:
                            if i["deaths"] == 0:
                                self.send_message(
                                    f'There are no deaths to delete.')
                            elif i["deaths"] == 1:
                                i['deaths'] -= 1
                                self.send_message(
                                    f'Deaths Updated. You have died {i["deaths"]} time playing {self.game}.')
                            else:
                                i['deaths'] -= 1
                                self.send_message(
                                    f'Deaths Updated. You have died {i["deaths"]} times playing {self.game}.')
                        write_json(data)

            else:
                self.send_message(f'You do not have permission to do this')
        except AttributeError:
            self.send_message(f'No game set.')

    def alldeaths(self, user):
        full_list = ''
        total_deaths = 0
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            name_data = (data["games"])

            for i in name_data:
                full_list += f"({i['title']}:{str(i['deaths'])}), "
                total_deaths += int(i['deaths'])

            self.send_message(f'Total deaths combined: {str(total_deaths)}')
            self.send_message(f'All Deaths: {str(full_list[:-2])}')

    def deaths(self, user):
        try:
            with open(file, 'r') as json_file:
                data = json.load(json_file)
                name_data = (data["games"])

                for i in name_data:
                    if self.game == i['title']:
                        self.send_message(f"{self.game}:{str(i['deaths'])}")

        except AttributeError:
            self.send_message(f'No game set.')

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)


def write_json(data, filename='death.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def help(bot, prefix, cmds):
    bot.send_message('Registered commands: ' + ', '.join([f'{prefix}{cmd}' for cmd in sorted(cmds.keys())]))


def hello(bot, user, *args):
    bot.send_message(f'Hello {user["name"]}!')
