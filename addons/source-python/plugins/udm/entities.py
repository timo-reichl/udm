# ../udm/entities.py

"""Provides classes for entity management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Filters
from filters.entities import EntityIter


# =============================================================================
# >> CLASSES
# =============================================================================
class EntityRemover(object):
    """Class used to remove entities from the server."""

    @staticmethod
    def perform_action(entities):
        """Remove all entities specified from the server."""
        for classname in entities:
            for entity in EntityIter(classname):
                entity.remove()


class EntityInputDispatcher(object):
    """Class used to dispatch an input on entities."""

    @staticmethod
    def perform_action(entities, input_name):
        """Dispatch the specified input on all entities."""
        for classname in entities:
            for entity in EntityIter(classname):
                entity.call_input(input_name)
