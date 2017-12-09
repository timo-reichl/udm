# ../udm/players/inventories.py

"""Provides player inventories."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Collections
from collections import defaultdict

# Source.Python Imports
#   Core
from core import GAME_NAME

# Script Imports
#   Weapons
from udm.weapons import weapon_manager


# =============================================================================
# >> PLAYER INVENTORIES
# =============================================================================
class _InventoryItem(object):
    """Class used to provide an inventory item."""

    def __init__(self):
        """Object initialization."""
        # Default the weapon's basename to None
        self._basename = None

        # Store the silencer option for this inventory item
        self.silencer_option = None

    def set_basename(self, value):
        """Set the basename and silencer option if the weapon can be silenced."""
        # Set the basename
        self._basename = value

        # Set the silencer option to True if the game is CS:GO, else False
        if self.data.has_silencer:
            self._silencer_option = GAME_NAME == 'csgo'

    def get_basename(self):
        """Return the basename."""
        return self._basename

    # Set the "basename" property for `_InventoryItem`
    basename = property(get_basename, set_basename)

    @property
    def data(self):
        """Return the weapon's data."""
        return weapon_manager[self.basename]


class _PlayerInventory(defaultdict):
    """Class used to provide a weapon inventory for players."""

    def __init__(self):
        """Make `_InventoryItem` the default value type."""
        super().__init__(_InventoryItem)

    def keys(self):
        """Override keys to reverse its order."""
        yield from sorted(self, reverse=True)

    def add_inventory_item(self, player, basename):
        """Add an inventory item for `basename` and equip the player with it."""
        # Get the weapon's data
        weapon_data = weapon_manager[basename]

        # Set the inventory item's basename
        self[weapon_data.tag].basename = basename

        # Equip the inventory item if the player is not dead
        if player.team_index > 1 and not player.dead:
            player.equip_inventory_item(weapon_data.tag)

    def remove_inventory_item(self, player, tag):
        """Remove an inventory item for weapon tag `tag`."""
        # Get the currently equipped weapon entity for the weapon tag
        weapon = player.get_weapon(is_filters=tag)

        if weapon is not None:
            weapon.remove()

        # Remove the weapon tag from this inventory
        if tag in self.keys():
            del self[tag]


class _PlayerInventories(defaultdict):
    """Class used to provide multiple inventories and weapon selections for players."""

    # Store weapon selections
    selections = defaultdict(int)

    # Store random weapon selections, defaults to True for every new player
    selections_random = defaultdict(lambda: True)


# Store a global instance of `_PlayerInventories`
player_inventories = _PlayerInventories(lambda: defaultdict(_PlayerInventory))
