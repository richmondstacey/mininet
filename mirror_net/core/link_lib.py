"""Link types."""


class Link:
    """Base class for all Link types."""

    subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        """Register subclasses."""
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls


# class OVSLink(Link):
#     """OVS Link placeholder."""
#
#
# class TCULink(Link):
#     """TCU Link placeholder."""


LINK_TYPES = {
    'default': Link,
    # 'ovs': OVSLink,
    # 'tcu': TCULink,
}
