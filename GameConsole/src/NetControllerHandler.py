
import itertools
from mtxNet import MtxNetRenderer, GameInfo, GameError


class NetControllerHandler():

    __NEW_RENDERER_ID = itertools.count()

    def __init__(self, frmMain, gameConsole, games):
        self._frmMain = frmMain
        self._gameConsole = gameConsole
        self._renderers = {}
        self._games = {g.GetName(): g for g in games}

    def Ping(self):
        pass

    def ConnectRenderer(self, host, port):
        print('Renderer connected: %s@%s' % (port, host))
        renderer = mtxNetRenderer.MtxNetRenderer(host, port)
        if renderer.Connect():
            rendererId = next(self.__NEW_RENDERER_ID)
            self._renderers[rendererId] = renderer
            self._gameConsole.RegisterRenderer(renderer)
        else:
            rendererId = -1

        return rendererId

    def DisconnectRenderer(self, rendererId):
        renderer = self._renderers.get(rendererId)

        if renderer is not None:
            print('Renderer disconnected: %s@%s' % (renderer.GetPort(), renderer.GetHost()))
            renderer.Disconnect()
            del self._renderers[rendererId]

    def GetGames(self):
        return self._games.keys()

    def GetGameInfo(self, name):
        game = self._GetGame(name)

        return GameInfo(game.GetName(), game.GetDescription(), game.GetMaxPlayers())

    def LoadGame(self, name):
        game = self._GetGame(name)
        self._gameConsole.LoadGame(game())

    def MovePlayer(self, number, direction):
        self._gameConsole.MovePlayer(number, direction)

    def JumpPlayer(self, number, direction):
        self._gameConsole.JumpPlayer(number, direction)

    def ResetLevel(self):
        self._gameConsole.ResetLevel()

    def _GetGame(self, name):
        game = self._games.get(name)
        if game is None:
             raise GameError('A game with the name "%s" does not exist.' % name)
        return game
