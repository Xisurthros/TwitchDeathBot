from time import time

from . import misc

PREFIX = '!'

cmds = {
    'hello': misc.hello,
    'setgame': misc.Game.setgame,
    'die': misc.Game.dead,
    'currentgame': misc.Game.currentgame,
    'listgames': misc.Game.listgames,
    'alldeaths': misc.Game.alldeaths,
    'deaths': misc.Game.deaths,
    'delete': misc.Game.deletedead,

}


def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(' ')[0][len(PREFIX):]
        args = message.split(' ')[1:]
        preform(bot, user, cmd, *args)


def preform(bot, user, cmd, *args):
    for name, func in cmds.items():
        if cmd == name:
            func(bot, user, *args)
            return

    if cmd == 'help':
        misc.help(bot, PREFIX, cmds)



    else:
        pass
