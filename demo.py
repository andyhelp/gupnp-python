from gi.repository import GLib, GUPnP, GSSDP, GObject
import os
import pdb

devices = []
introspections = {}
containers = []
objects = []
serv = None

device_services = {}

sources = []
renderers = []

def new_item(node, object):
  print object.get_title() 
  objects.append(object)

def new_container(node, object):
  containers.append(object)
  in_data = {"ObjectID": object.get_id(), "BrowseFlag": "BrowseDirectChildren",
		    "Filter": "", "StartingIndex": "0", "RequestCount": "0",
		    "SortCriteria": ""}
  out_data = {"Result": "", "NumberReturned": "", "TotalMatches": "", "UpdateID": ""}
  return_data = serv.send_action_hash("Browse", in_data, out_data)
  parser = GUPnPAV.GUPnPDIDLLiteParser()
  parser.connect("container_available", new_container)
  parser.connect("item_available", new_item)
  parser.parse_didl(return_data[1]["Result"])
 

#def play_complete(service, action, userdata):
#   print "PLAY COMPLETE"

def set_uri_complete(service, action, userdata):
   print "SET URI DONE"
   data2 = {"Speed": "1", "InstanceID": "0"}
   service.end_action_hash(action, {})
   service.begin_action_hash("Play", play_complete, None, data2)

def got_introspection(service, intro, error, userdata):
  global introspections
  introspections[service.get_udn()] = intro

  actions = intro.list_action_names()
  print "Found %d actions(s)" % len(actions)
  for name in actions:
      print service.get_service_type(), name
      if name == "GetVolume":
          data = {"InstanceID": "0", "Channel": "Master"}
          data_out = {"CurrentVolume": "" }
          service.send_action_hash(name, data, data_out)
          print "Current volume: ", data_out
      if name == "SetAVTransportURI":
          dict = {"Speed": "1", "InstanceID": "0"}
          muri = ""
          curi = "http://downloads.bbc.co.uk/podcasts/radio2/whiley/whiley_20120622-1257a.mp3"
          data = {"InstanceID": "0", "CurrentURI": curi, "CurrentURIMetaData": muri}
          service.send_action_hash(name, data, {})
          print "Done setting URI"
          service.send_action_hash("Stop", {"InstanceID": 0}, {})
          print "Done Stopping"
          data2 = {"Speed": "1", "InstanceID": "0"}
          service.send_action_hash("Play", data2, {})
          print "Done Playing"


 

#def server_introspection(service, introspection, error, userdata):
#  print "Got server introspection"
#  for i in introspection.list_actions():
#      if i.name == "Browse":
#         in_data = {"ObjectID": "0", "BrowseFlag": "BrowseDirectChildren",
#		    "Filter": "", "StartingIndex": "0", "RequestCount": "0",
#		    "SortCriteria": ""}
#         out_data = {"Result": "", "NumberReturned": "", "TotalMatches": "", "UpdateID": ""}#
#	 print "SEND ACTION"
#         return_data = service.send_action_hash("Browse", in_data, out_data)
#	 global serv
#	 serv=service
#	 print "Good news!"
#	 print return_data[1]["Result"]
#	 parser = GUPnPAV.GUPnPDIDLLiteParser()
#	 parser.connect("container_available", new_container)
#	 parser.connect("item_available", new_item)
#	 parser.parse_didl(return_data[1]["Result"])
#	 print len(objects)

def list_cur_devices():
  global devices, introspections, sources, renderers
  for d in devices:
     print "Device: %s" % d.get_model_name()
     for s in d.list_services():
         print "\tService: %s" % s.get_service_type()
	 if not s.get_udn() in introspections:
	     continue
         for action_name in introspections[s.get_udn()].list_action_names():
             print "\t\tAction: %s" % action_name

  print "Current Sources:"
  for i in sources:
      print "\t%s" % i.get_model_name()

  print "Current Renderers:"
  for i in renderers:
      print "\t%s" % i.get_model_name()

  print "-" * 30

  return True

def device_available(cp, device):
  global renderers, sources, devices, device_services
  devices.append(device)
  print device.get_model_name()
  device_services[device.get_udn()] = device.list_services()
  for service in device.list_services():
      print service.get_service_type()
#      With async callback we need to add service to global table,
#      otherwise python frees service structure before callback is called.
#      As a result callback is never called.
#      Changed to get introspection and call callback in this function
#
#      service.get_introspection_async(got_introspection, None)
      introspection = service.get_introspection()
      got_introspection( service, introspection, None, None )
      if "AV" in service.get_service_type():
          renderers.append(device)           
      if "ContentDirectory" in service.get_service_type():
          sources.append(device)

  list_cur_devices()

def device_unavailable(cp, device):
  global devices, introspections, sources, renderers, device_services
  devices.remove(device)
  if sources and device.get_model_name() in sources:
     sources.remove(device)

  if renderers and device.get_model_name() in renderers:
     renerers.remove(device)

#  for service in device_services[device.get_udn()]:
#      introspections.remove(service.get_udn())

#  if device.get_model_name() == "MediaTomb":
#      for service in device.list_services():
#          print service.get_service_type()
#          if "ContentDirectory" in service.get_service_type():
#              service.get_introspection_async(server_introspection, None)

def run_timer():
  return True

ctx = GUPnP.Context(interface="eth0")
ctx.init(None)

# Bind to eth0 in the maincontext on any port
cp  = GUPnP.ControlPoint(client=ctx, target="upnp:rootdevice")

# Use glib style .connect() as a callback on the controlpoint to listen for new devices
cp.connect("device-proxy-available", device_available)
cp.connect("device-proxy-unavailable", device_unavailable)

# "Tell the Control Point to Start Searching"
GSSDP.ResourceBrowser.set_active(cp, True)


GObject.timeout_add(3000, list_cur_devices)

# Enter the main loop which begins the work and facilitates callbacks
GObject.MainLoop().run()

