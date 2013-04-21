from gi.repository import GLib, GUPnP, GSSDP, GObject

devices = []
services = []


def event_cb( serviceProxy, variable, value, user_data ):
    print "Event CB called from ", serviceProxy.get_url_base().get_host(), serviceProxy.get_service_type()
    print "  serviceProxy=%s" %serviceProxy
    print "  variable=%s" %variable
    print "  value=%s" %value
    print "  user_data=%s" %user_data
    print "----"


def device_available(cp, device):
    global devices, services

    devices.append(device)
    for service in device.list_services():
        services.append(service)
        print "Subscribing to ", service.get_url_base().get_host(), device.get_friendly_name(), service.get_service_type()
        service.add_notify("LastChange", str, event_cb, None)
        service.set_subscribed(True)
 

def device_unavailable(cp, device):
    print "Device unavailable"

if __name__ == "__main__":
    ctx = GUPnP.Context(interface="eth0")
    ctx.init(None)
    cp  = GUPnP.ControlPoint(client=ctx, target="upnp:rootdevice")
    cp.connect("device-proxy-available", device_available)
    cp.connect("device-proxy-unavailable", device_unavailable)

    GSSDP.ResourceBrowser.set_active(cp, True)
    GObject.MainLoop().run()
    print "devices:", devices
    print "services:", services 
    print ctx, cp
