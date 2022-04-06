from discord.ext import commands


class Smarts(commands.Cog):
    """a lot of smart commands"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="calcular", help="Calcula uma expressão. Argumento: Expressão")
    async def calculate_expression(self, ctx, *expression):
        expression = "".join(expression)

        print(expression)

        expression = expression.replace(" ", "")

        try:
            if int(expression[0])<=9:
                response = eval(expression)

                await ctx.send("A resposta é: " + str(response))
            
        except:
            await ctx.send("Digite uma expressão valida")

def setup(bot):
    bot.add_cog(Smarts(bot))