from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from eizzek.bot import EizzekProtocol
from eizzek import config
from eizzek.lib import plugins  # register all plugins

application = service.Application("eizzek")

client = XMPPClient(jid.internJID(config.JID), config.PASSWORD, config.SERVER, config.PORT)
client.logTraffic = False
client.setServiceParent(application)

bot = EizzekProtocol()
bot.setHandlerParent(client)