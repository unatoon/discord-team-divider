import threading

from discord.ext import commands


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.teams = {}
        self.lock = threading.Lock()

    def add_team(self, team):
        self.teams[team.team_name] = team

    def delete_team(self, team_name):
        del self.teams[team_name]


class Team:
    def __init__(self, team_name, num_players):
        self.team_name = team_name
        self.num_players = num_players


class Generator:
    def __init__(self):
        self._data = {}
        self._generator_lock = threading.Lock()

    async def open(self, game_id):
        try:
            with self._generator_lock:
                if game_id in self._data:
                    return f'ERROR: Game **{game_id}** already exists'

                self._data[game_id] = Game(game_id)

                return f'Opend a new game **{game_id}**'
        except Exception as err:
            return f'ERROR: {err}'

    async def close(self, game_id):
        try:
            with self._generator_lock:
                if game_id not in self._data:
                    return f"ERROR: Game **{game_id}** doesn't exist"

                del self._data[game_id]
                return f'Closed game **{game_id}**'

        except Exception as err:
            return f'ERROR: {err}'


class GeneratorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._generator = Generator()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def open(self, ctx, game_id):
        msg = await self._generator.open(game_id)
        await ctx.send(msg)

    @commands.command()
    async def close(self, ctx, game_id):
        msg = await self._generator.close(game_id)
        await ctx.send(msg)

    @commands.command()
    async def set(self, ctx, game_id, key, value):
        await ctx.send(f'set {game_id}')

    @commands.command()
    async def addteam(self, ctx, game_id, team_name, num_players):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def delteam(self, ctx, game_id, team_name):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def join(self, ctx, game_id, username=None):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def leave(self, ctx, game_id, username=None):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def show(self, ctx, game_id):
        await ctx.send(f'added team {game_id}')


def setup(bot):
    return bot.add_cog(GeneratorCog(bot))
