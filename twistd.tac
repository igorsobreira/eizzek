from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from bot import EizzekProtocol
import config

application = service.Application("eizzek")

client = XMPPClient(jid.internJID(config.JID), config.PASSWORD, config.SERVER, config.PORT)
client.logTraffic = False
client.setServiceParent(application)

bot = EizzekProtocol()
bot.setHandlerParent(client)