from enum import Enum


class ChannelType(Enum):
    """Defines different types of software versions."""

    STABLE = "stable"
    ALPHA = "alpha"
    BETA = "beta"
