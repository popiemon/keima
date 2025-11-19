class NoCoinsDataError(Exception):
    """Exception raised when there is no coins data available for the team."""

    pass


class InvalidPlayerCountError(Exception):
    """Exception raised when the number of players is invalid."""

    pass
