from loguru import logger
from mccolors import mcwrite

from ..utilities.minecraft.player.get_player_uuid import PlayerUUID
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'uuid'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]

    @logger.catch
    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments

        Args:
            arguments (list): The arguments to validate

        Returns:
            bool: True if the arguments are valid, False otherwise
        """

        if not ValidateArgument.validate_arguments_length(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments):
            return False
        
        return True

    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        # Validate the arguments
        if not self.validate_arguments(arguments):
            return
        
        # Get the player data
        mcwrite(f"{LM().get(['commands', self.name, 'gettingPlayerUuid'])}")
        player_data = PlayerUUID(username=arguments[0]).get_uuid()
        
        # Add a new line
        print('')

        # Print the player data
        if player_data.online_uuid is not None:
            mcwrite(LM().get(['commands', self.name, 'uuid']).replace('%uuid%', f'&a&l{player_data.online_uuid}'))

        mcwrite(LM().get(['commands', self.name, 'uuid']).replace('%uuid%', f'&c&l{player_data.offline_uuid}'))
