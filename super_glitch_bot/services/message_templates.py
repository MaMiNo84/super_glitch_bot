"""Templates used for telegram messages."""


class MessageTemplates:
    """Container for message templates."""

    NEW_GEM = "{token_name} is live!"
    PERFORMANCE_UPDATE = "{token_name} performance update: {details}"

    STARTED = "Monitoring service started."
    STOPPED = "Monitoring service stopped."
    ERROR = "Error: {details}"
    TOKEN_DELISTED = "{token_name} has been delisted."
