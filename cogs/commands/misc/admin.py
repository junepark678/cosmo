import traceback
import discord
from discord import app_commands
from discord.ext import commands
from data.services import guild_service
from utils import GIRContext, cfg, transform_context, logger
from utils.framework import admin_and_up, guild_owner_and_up
from utils.framework.transformers import ImageAttachment


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @admin_and_up()
    @app_commands.guilds(cfg.guild_id)
    @app_commands.command(description="Change the bot's profile picture")
    @app_commands.describe(image="Image to use as profile picture")
    @transform_context
    async def setpfp(self, ctx: GIRContext, image: ImageAttachment):
        await self.bot.user.edit(avatar=await image.read())
        await ctx.send_success("Done!", delete_after=5)
        
    @admin_and_up()
    @app_commands.guilds(cfg.guild_id)
    @app_commands.command(description="Raises a KeyboardInterrupt")
    @transform_context
    async def exit(self, ctx: GIRContext):
        raise KeyboardInterrupt()

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        if ctx.author.id != cfg.owner_id:
            return

        try:
            async with ctx.typing():
                await self.bot.tree.sync(guild=discord.Object(id=cfg.guild_id))
        except Exception as e:
            await ctx.send(f"An error occured\n```{e}```")
            logger.error(traceback.format_exc())
        else:
            await ctx.send("Done!")


async def setup(bot):
    await bot.add_cog(Admin(bot))
