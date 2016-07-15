from aioupnp import version

def describe_upnp_versions():

    def upnp10_is_lower_than_upnp11_and_upnp20():
        assert version.UPnPVersion10 < version.UPnPVersion11