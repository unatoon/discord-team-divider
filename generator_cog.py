import threading

from discord.ext import commands


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.teams = {}

    def add_team(self, team):
        if team.name in self.teams:
            raise Exception(f'Team {team.name} already exists in the game {self.game_id}')
        self.teams[team.name] = team

    def delete_team(self, team_name):
        if team_name not in self.teams:
            raise Exception(f"Team {team_name} doesn't exist in the game {self.game_id}")
        del self.teams[team_name]


class Team:
    def __init__(self, name, num_players):
        self.name = name
        self.num_players = num_players


class Generator:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    async def open(self, game_id):
        try:
            with self._lock:
                if game_id in self._data:
                    return f'ERROR: Game **{game_id}** already exists'

                self._data[game_id] = Game(game_id)

                return f'Opend a new game **{game_id}**'
        except Exception as err:
            return f'ERROR: {err}'

    async def close(self, game_id):
        try:
            with self._lock:
                if game_id not in self._data:
                    return f"ERROR: Game **{game_id}** doesn't exist"

                del self._data[game_id]
                return f'Closed game **{game_id}**'

        except Exception as err:
            return f'ERROR: {err}'

    async def addteam(self, game_id, team_name, num_players):
        try:
            with self._lock:
                if game_id not in self._data:
                    return f"ERROR: Game **{game_id}** doesn't exist"

                team = Team(team_name, num_players)
                self._data[game_id].add_team(team)
                return f'Added team **{team_name}** into the game {game_id}'

        except Exception as err:
            return f'ERROR: {err}'

    async def delteam(self, game_id, team_name):
        try:
            with self._lock:
                if game_id not in self._data:
                    return f"ERROR: Game **{game_id}** doesn't exist"

                self._data[game_id].delete_team(team_name)
                return f'Deleted team **{team_name}** from the game {game_id}'
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
        msg = await self._generator.addteam(game_id, team_name, num_players)
        await ctx.send(msg)

    @commands.command()
    async def delteam(self, ctx, game_id, team_name):
        msg = await self._generator.delteam(game_id, team_name)
        await ctx.send(msg)

    @commands.command()
    async def join(self, ctx, game_id, username=None):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def leave(self, ctx, game_id, username=None):
        await ctx.send(f'added team {game_id}')

    @commands.command()
    async def next(self, ctx, game_id):
        await ctx.send(f'next {game_id}')

    @commands.command()
    async def show(self, ctx, game_id):
        await ctx.send(f'added team {game_id}')


def setup(bot):
    return bot.add_cog(GeneratorCog(bot))
