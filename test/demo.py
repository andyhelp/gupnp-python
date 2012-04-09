from gi.repository import GLib, GUPnP, GSSDP, GObject, Soup

def device_available(device, cp):
  import pdb
  pdb.set_trace()
  print cp


ctx = GUPnP.Context(interface="eth0")
ctx.init(None)

# Bind to eth0 in the maincontext on any port
cp  = GUPnP.ControlPoint(client=ctx, target="upnp:rootdevice")

# Use glib style .connect() as a callback on the controlpoint to listen for new devices
cp.connect("device-proxy-available", device_available)

# "Tell the Control Point to Start Searching"
GSSDP.ResourceBrowser.set_active(cp, True)

# Enter the main loop which begins the work and facilitates callbacks
GObject.MainLoop().run()

# Be cheeky, and intentionally NOT clean up memory because python is awesome
print "You'll never know I am here!"
