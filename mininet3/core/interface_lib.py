"""Interface node types."""


class Interface:
    """Base class for all Interface types."""

    subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        """Register subclasses."""
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls


INTERFACE_TYPES = {
    'default': Interface,
}
