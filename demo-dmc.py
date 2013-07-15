from gi.repository import GUPnP, GSSDP, GObject
from optparse import OptionParser


def get_mute_cb(service, action, user_data):
  ret = service.end_action_hash(action,{"CurrentMute": "" })
  print "GetMute cb:", ret


def device_available(cp, device):
  print "New device: ", device.get_friendly_name(), device.get_udn()

  if device.get_udn() != options.dmr_udn:
    return
  print "Found device \"%s\" with matching udn" % device.get_friendly_name()
  rc_service = device.get_service("urn:schemas-upnp-org:service:RenderingControl")
  if rc_service:
    rc_service.begin_action_hash("GetMute", get_mute_cb, None, {"InstanceID": "0", "Channel": "Master"})
    currentVolume = rc_service.send_action_hash("GetVolume", {"InstanceID": "0", "Channel": "Master"},  {"CurrentVolume": "" })
    print "GetVolume:", currentVolume
  
  avt_service = device.get_service("urn:schemas-upnp-org:service:AVTransport")
  if avt_service and options.url:
    print "Stop"
    avt_service.send_action_hash("Stop", {"InstanceID": 0}, {})
    print "SetAVTransportURI"
    avt_service.send_action_hash("SetAVTransportURI", {"InstanceID": "0", "CurrentURI": options.url, "CurrentURIMetaData": ""}, {})
    print "Play"
    avt_service.send_action_hash("Play", {"Speed": "1", "InstanceID": "0"}, {})
  gmainloop.quit()


parser = OptionParser()
parser.add_option("", "--dmr-udn", dest="dmr_udn")
parser.add_option("", "--url", dest="url")

(options, args) = parser.parse_args()
print "Config: dmr-udn=%s, url=%s" %(options.dmr_udn, options.url)

ctx = GUPnP.Context(interface="eth0")
ctx.init(None)
cp  = GUPnP.ControlPoint(client=ctx, target="upnp:rootdevice")
cp.connect("device-proxy-available", device_available)
GSSDP.ResourceBrowser.set_active(cp, True)
gmainloop = GObject.MainLoop()
gmainloop.run();

