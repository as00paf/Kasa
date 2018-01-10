import eg
import requests
import json

eg.RegisterPlugin(
    name = "Kasa Plugin",
    author = "Alexandre Fournier",
    version = "0.0.1",
    kind = "other",
    description = "This is a plugin to control TP-Link devices like the Kasa app",
    createMacrosOnAdd = True,
    icon=("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1MEUxODYwREY1RDIxMUU3OTZCM0E3MDYzMDNGMzFGNCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo1MEUxODYwRUY1RDIxMUU3OTZCM0E3MDYzMDNGMzFGNCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjUwRTE4NjBCRjVEMjExRTc5NkIzQTcwNjMwM0YzMUY0IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjUwRTE4NjBDRjVEMjExRTc5NkIzQTcwNjMwM0YzMUY0Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+EtlFHgAAAfZJREFUeNqcU0tLW0EU/s7cSW5uzMNXQIompUgEKaG0tEURGjcF8RdIoStbWrruukvX/SOFCgpCF1n0ScE+KC2C4ELFVw1KHkZjZnru3Ns2E6VQD3zkzJk5k2++813CxJMExXtfI3u7oBMZAhSsiKXtNQlQdVdh7c2yrpWLDo1Of9Djj6/BSxMcCcjYX5ALaG4S1HYDF7xuQvbWJfq5cofo4aLSmTyhdWL/04lCX3fEpPsHTSAq7H0nyky2ldDxvrPNDYXhTBSlBzkDP/drVnCPjvcLcebNRy3cvBLHwmwOVwdcg1ePLpuav2eFVrB5HStMFVJ4fm8I+f7on3KOn7I0mzV7/pn2EJbKjsDM9CDGeiU6o8dz8OL+EAuLjgvC0RhUtrFaF3i2BpQOA1gTlf6UtVWTprG6FayqG/jfkKhsAvXd8AkSc1/3gryQsQ4W0+dfINAoM30nBC7AwMgQjocd13x7YNK53ydCJuwr3O3BOSJS2yT/weCYCX7vLHKvpMah0l5a4JTdGEkAtXW2LTP5sgPJjOY31+EQ4WNEI+VbQ3qsVWBxqu0pia0fnzAyecNUmnVGlUXlvKxxyj+fWzw2HY4uMQgkY0HuJoFvL98TJp92UcQtYSB/XbtJ4duzw6+BwEludlNmTUdl/pzfLevKTvGXAAMAaL+XZenFgmUAAAAASUVORK5CYII=")
)

class KasaUser():
	def __init__(self, username="", password=""):
		self.username = username
		self.password = password

class Device():
	def __init__(self, id="", alias="", mac="", url=""):
		self.id = id
		self.alias = alias
		self.mac = mac
		self.url = url
		
	def toString(self):
		return self.id + " " + self.alias + " : " + self.mac + " @ " + self.url
        
class Authenticate(eg.ActionBase):
    name = "Authenticate"
    description = "This action will authenticate the user with the TP-Link Kasa API"
    def __call__(self):
	print("Authenticating...")
	self.url = "https://wap.tplinkcloud.com"
	self.data = {
	"method": "login",
	"params": {
	"appType": "Kasa_Android",
	"cloudUserName": self.plugin.username,
	"cloudPassword": self.plugin.password,
	"terminalUUID": "9b2a50da-adf9-42ec-a5d7-9bbf50a10f18"
	}
	}
	self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	self.r = requests.post(self.url, data=json.dumps(self.data), headers=self.headers, verify=False)
	self.plugin.token = json.loads(self.r.text)['result']['token']
		

class GetDeviceList(eg.ActionBase):
    name = "Get Device List"
    description = "This action will retrieve all devices associated with the users's account"
    def __call__(self):
        print "Retrieving device list..."
        
        try:
            #Options
            url = "https://wap.tplinkcloud.com?token=" + self.plugin.token
            data = {"method":"getDeviceList"}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #Get device list
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
            deviceList = json.loads(r.text)['result']['deviceList']
            
            self.plugin.devices = []
            self.plugin.deviceAlias = []
            for device in deviceList:
                mac = device['deviceMac']
                mac = "-".join(mac[i:i+2] for i in range(0, len(mac), 2))
                device = Device(device['deviceId'], device['alias'], mac, device['appServerUrl'])
                self.plugin.devices.append(device)
                self.plugin.deviceAlias.append(device.alias)
        except AttributeError:
            eg.PrintError("Something went wrong. Please make sure you called Authenticate!")

class SetDeviceState(eg.ActionBase):
    name = "Sets Device State"
    description ="Change device state to ON or OFF"
    
    def __call__(self, deviceIndex, state):
        print("Changing device state...")
        try:
            device = self.plugin.devices[deviceIndex]
            newState = str(state)
            #Options
            url = device.url + "?token=" + self.plugin.token
            data = {"method":"passthrough", "params": {"deviceId": device.id, "requestData": "{\"system\":{\"set_relay_state\":{\"state\":" + newState + "}}}" }}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #Get device list
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        except AttributeError:
            eg.PrintError("Something went wrong. Please make sure you called Authenticate and Get Device List!")
        
    def Configure(self, deviceIndex=-1, state = 0):
        try:
            panel = eg.ConfigPanel()
            device = self.plugin.devices[deviceIndex]
           
            self.label1 = wx.StaticText(panel,label = "Select Device" ,style = wx.ALIGN_LEFT) 
            panel.sizer.Add(self.label1, 0 , wx.ALIGN_LEFT)
            
            self.deviceCombo = wx.ComboBox(panel, -1, size=(150, -1), value=device.alias,choices=self.plugin.deviceAlias)
            panel.sizer.Add(self.deviceCombo, 0, wx.ALIGN_CENTER_VERTICAL)
            
            self.label1 = wx.StaticText(panel,label = "Select State" ,style = wx.ALIGN_LEFT) 
            panel.sizer.Add(self.label1, 0, wx.ALIGN_LEFT, 20)
            
            self.states = ["OFF", "ON"]        
            self.stateCombo = wx.ComboBox(panel, -1, size=(150, -1), value=self.states[state], choices=self.states)
            panel.sizer.Add(self.stateCombo, 0, wx.ALIGN_LEFT)
            
            while panel.Affirmed():
                state = self.stateCombo.GetCurrentSelection()
                deviceIndex = self.deviceCombo.GetCurrentSelection()
                panel.SetResult(deviceIndex, state)
        except AttributeError:
            eg.PrintError("Something went wrong. Please make sure you called Authenticate and Get Device List!")

class ToggleDeviceState(eg.ActionBase):
    name = "Toggle Device State"
    description ="Toggles the device state"
    
    def __call__(self, deviceIndex):
        print("Changing device state...")
        try:
            device = self.plugin.devices[deviceIndex]
            
            #Get current state
            url = device.url + "?token=" + self.plugin.token            
            data = {"method":"passthrough", "params": {"deviceId": device.id, "requestData": "{\"system\":{\"get_sysinfo\":null},\"emeter\":{\"get_realtime\":null}}" }}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
            response = json.loads(r.text)['result']['responseData']
            currentState = json.loads(response)["system"]['get_sysinfo']['relay_state']
            if(currentState == 1):
                newState = "0"
                print "Will turn " + device.alias + " off"
            else:
                newState = "1"
                print "Will turn " + device.alias + " on"
            
            #Toggle
            data = {"method":"passthrough", "params": {"deviceId": device.id, "requestData": "{\"system\":{\"set_relay_state\":{\"state\":" + newState + "}}}" }}
            #Get device list
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        except AttributeError:
            eg.PrintError("Something went wrong. Please make sure you called Authenticate and Get Device List!")
        
    def Configure(self, deviceIndex=-1):
        try:
            panel = eg.ConfigPanel()
            device = self.plugin.devices[deviceIndex]
           
            self.label1 = wx.StaticText(panel,label = "Select Device" ,style = wx.ALIGN_LEFT) 
            panel.sizer.Add(self.label1, 0 , wx.ALIGN_LEFT)
            
            self.deviceCombo = wx.ComboBox(panel, -1, size=(150, -1), value=device.alias,choices=self.plugin.deviceAlias)
            panel.sizer.Add(self.deviceCombo, 0, wx.ALIGN_CENTER_VERTICAL)
            
            while panel.Affirmed():
                deviceIndex = self.deviceCombo.GetCurrentSelection()
                panel.SetResult(deviceIndex)
        except AttributeError:
            eg.PrintError("Something went wrong. Please make sure you called Authenticate and Get Device List!")
        
def getDeviceFromAliasIndex(self, index):   
    return self.plugin.devices[index]
		
class KasaPlugin(eg.PluginBase):
	def __init__(self): 
	  print "Kasa Plugin is inited."
	  self.AddAction(Authenticate)
	  self.AddAction(GetDeviceList)
	  self.AddAction(SetDeviceState)
	  self.AddAction(ToggleDeviceState)
	  #self.AddAction(ToggleLocalDeviceState)

	def __start__(self, kasaUser):
			print "Kasa Plugin is started with user: " + kasaUser.username + " boiiiiiiiiiii"
			self.username = kasaUser.username
			self.password = kasaUser.password

	def __stop__(self):
			print "Kasa Plugin is stopped."

	def __close__(self):
			print "Kasa Plugin is closed."

	def Configure(self, kasaUser=KasaUser("", "")):
            panel = eg.ConfigPanel()
        
            label = wx.StaticText(panel, label="Email", style=wx.ALIGN_LEFT)
            panel.sizer.Add(label, 0, wx.ALIGN_LEFT)
        
            userText = wx.TextCtrl(panel, -1, kasaUser.username)
            panel.sizer.Add(userText, 0, wx.ALIGN_LEFT)
            
            label = wx.StaticText(panel, label="Password", style=wx.ALIGN_LEFT)
            panel.sizer.Add(label, 0, wx.ALIGN_LEFT)
		
            pwdText = wx.TextCtrl(panel, -1, kasaUser.password, style=wx.ALIGN_LEFT|wx.TE_PASSWORD)
            panel.sizer.Add(pwdText, 0, wx.ALIGN_LEFT)
		
            while panel.Affirmed():
                panel.SetResult(KasaUser(userText.GetValue(), pwdText.GetValue()))