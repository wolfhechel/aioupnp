class UPnPVersion(object):
    """ UPnP device architecture version object.

    Represents the `major` and `minor` version specification for
    a device or control point.

    This object implements sortable comparison methods which allows
    comparison of versions, i.e. if 2.0 is higher than 1.1 (which it is).

    Attributes:

        major (int): Major version
        minor (int): Minor version

    """

    major = None

    minor = None

    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __repr__(self):
        return '<UPnPVersion %d.%d>' % (self.major, self.minor)

    def __gt__(self, other):
        return (self.major, self.minor) > (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

    def __ge__(self, other):
        return (self.major, self.minor) >= (other.major, other.minor)

    def __le__(self, other):
        return (self.major, self.minor) <= (other.major, other.minor)

UPnPVersion10 = UPnPVersion(1, 0)
"""UPnPVersion: UPnP version 1.0 specification.

Todo:
    Document the limitations of using this UDA version.
"""

UPnPVersion11 = UPnPVersion(1, 1)
"""UPnPVersion: UPnP version 1.1 specification.

Todo:
    Document the limitations of using this UDA version.
"""

UPnPVersion20 = UPnPVersion(2, 0)
"""UPnPVersion: UPnP version 2.0 specification.

Todo;
    Document how the backwards compatibility with older specification works.
"""
