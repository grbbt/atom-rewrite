from typing import Coroutine, Optional, Union
from discord import ui, Interaction, SelectOption, ButtonStyle, Embed
from discord.ext.commands import Cog, Command, Group, DefaultHelpCommand

BotMapping = dict[Optional[Cog], list[Command]]
Entity = Optional[Union[Cog, Command]]


class ComponentHelp(DefaultHelpCommand):
    _mapping = None

    async def get_filtered_mapping(self) -> BotMapping:
        if self._mapping is None:
            mapping = {cog: await self.filter_commands(cmds)
                       for cog, cmds in self.get_bot_mapping().items()}
            # filter out cogs with no commands post-filter
            self._mapping = {cog: cmds for cog, cmds in mapping.items() if cmds}
        return self._mapping

    async def send_view(self, embed: Embed, entity: Entity):
        mapping = await self.get_filtered_mapping()
        view = HelpView(self, mapping, entity)
        await view.update_commands()  # must be async to filter subcommands
        view.message = await self.get_destination().send(embed=embed, view=view)

    async def send_bot_help(self, mapping: BotMapping):
        mapping = await self.get_filtered_mapping()
        embed = await self.get_bot_help(mapping)
        await self.send_view(embed, None)

    async def send_cog_help(self, cog: Cog):
        mapping = await self.get_filtered_mapping()
        if cog not in mapping:
            return

        embed = await self.get_cog_help(cog)
        await self.send_view(embed, cog)

    async def send_group_help(self, group: Group):
        embed = await self.get_group_help(group)
        await self.send_view(embed, group)

    async def get_bot_help(self, mapping: BotMapping) -> Embed:
        # commands = [f'{cmd}' for cmd in mapping[None]]

        a = Embed(title='**Welcome to Atom**', description=f"| [Github](https://github.com/Little-RR/atomdiscord) | [Invite](https://discord.com/api/oauth2/authorize?client_id=895668486611824650&permissions=8&scope=bot) |\n"
                                                           f"```Prefix '=', do =help for this menu```", colour=0xffffff)
        cogs = "\n"
        for cog in mapping:
            if cog is None:
                break
            else:
                cogs += f"{str(cog.qualified_name)}"+'\n'

        a.add_field(name="Categories:", value="```"+f"{cogs}"+"\n\n\n\nㅤ```", inline=True)
        cmds = ""

        for cmd in mapping[None]:
            cmds += f"={str(cmd)} - {cmd.short_doc}\n"
        i = 0
        for c in self.context.bot.commands:
            if c.hidden is True:
                i = i
            else:
                i = i+1

        a.add_field(name="Atom News:", value="```Atom has a new updates!, \n- Reworked Music system! \n- New Moderation Commands! ```\n **Uncategorized Commands:**\n"+f"```{cmds[0:len(cmds)]}```", inline=True)
        a.set_footer(text=f"Atom Version: Alpha 1.2 | Current Usable Commands: {i}")
        return a

    async def get_cog_help(self, cog: Cog) -> Embed:
        mapping = await self.get_filtered_mapping()
        e = Embed(title=f'{cog.qualified_name} Commands', description=cog.description, colour=0xffffff)
        for c in mapping[cog]:
            des = c.help
            if des is not None:
                e.add_field(name=c, value=f"`{str(des)}`", inline=True)
            else:
                e.add_field(name=c, value=f"`No Description`", inline=True)

        return e

    async def get_group_help(self, group: Group) -> Embed:
        commands = await self.filter_commands(group.commands)

        description = '\n'.join([f'Usage: `{self.get_command_signature(group)}`',
                                 group.help,
                                 '\n'.join(f'`{cmd}`' for cmd in commands)])

        return Embed(title=f'{group}', description=description, colour=0xffffff)


class HelpView(ui.View):
    def __init__(self, help: ComponentHelp,
                 mapping: BotMapping,
                 entity: Entity = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = help
        self.bot = help.context.bot

        self.mapping = mapping
        self.entity = entity

        self.update_cogs()

    async def on_timeout(self):
        await self.message.delete()

    def update_cogs(self):
        # to use emojis, you can build a list of `SelectOptions` then sort by label
        names = sorted(cog.qualified_name for cog in self.mapping if cog)
        # always add "No Category" at the end
        names.append(self.help.no_category)
        options = [SelectOption(label=name) for name in names]
        self.children[0].options = options

    async def update_commands(self):
        entity = self.entity

        # list the parent command/cog/bot's commands instead of nothing
        if isinstance(entity, Command) and not isinstance(entity, Group):
            entity = entity.parent or entity.cog or None

        if isinstance(entity, Group):
            cmds = await self.help.filter_commands(entity.commands)
        else:
            cmds = self.mapping[entity]

        options = [SelectOption(label=f'{cmd}') for cmd in cmds]
        self.children[1].options = options

    def get_embed(self) -> Coroutine[None, None, Embed]:
        entity = self.entity
        if isinstance(entity, Cog):
            return self.help.get_cog_help(entity)
        elif isinstance(entity, Group):
            return self.help.get_group_help(entity)
        else:
            return self.help.get_bot_help(self.mapping)

    async def respond_with_edit(self, interaction: Interaction):
        embed = await self.get_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.select(placeholder='Categories')
    async def cog_select(self, select: ui.Select, interaction: Interaction):
        name = select.values[0]
        entity = self.bot.get_cog(name)
        if entity == self.entity:
            return
        self.entity = entity

        await self.update_commands()
        await self.respond_with_edit(interaction)

    @ui.button(label="ㅤㅤHomeㅤㅤ", style=ButtonStyle.green)
    async def home(self, button: ui.Button, interaction: Interaction):
        try:
            self.entity = None
        except:
            return

        await self.update_commands()
        await self.respond_with_edit(interaction)

    @ui.button(label='ㅤㅤCloseㅤㅤ', style=ButtonStyle.danger)
    async def close(self, button: ui.Button, interaction: Interaction):
        self.stop()
        await interaction.message.delete()


class Help(Cog):
    """Help Command"""

    def __init__(self, bot):
        self.bot = bot
        self.original_help_command = bot.help_command
        bot.help_command = ComponentHelp(command_attrs=dict(hidden=True), no_category="Home")

        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
