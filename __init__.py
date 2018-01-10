import eg
import requests
import json

eg.RegisterPlugin(
    name = "Kasa Plugin",
    author = "Alexandre Fournier",
    version = "0.0.1",
    kind = "other",
    description = "This is a plugin to control TP-Link devices like the Kasa app"
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
	print(self.r.text)
	self.plugin.token = json.loads(self.r.text)['result']['token']
		

class GetDeviceList(eg.ActionBase):
    name = "Get Device List"
    description = "This action will retrieve all devices associated with the users's account"
    def __call__(self):
	print "Retrieving device list..."
		
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
		print(device.toString())

class ToggleDeviceState(eg.ActionBase):
    name = "Toggle Device State"
    description ="Change device state to ON or OFF"
    
    def __call__(self, device, state):
        print("Changing device state...")
        newState = str(state)
		#Options
        url = device.url + "?token=" + self.plugin.token
        data = {"method":"passthrough", "params": {"deviceId": device.id, "requestData": "{\"system\":{\"set_relay_state\":{\"state\":" + newState + "}}}" }}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #Get device list
        r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        
    def Configure(self, device = Device(), state = 0):
        panel = eg.ConfigPanel()
       
        self.label1 = wx.StaticText(panel,label = "Select Device" ,style = wx.ALIGN_LEFT) 
        panel.sizer.Add(self.label1, 0 , wx.ALIGN_LEFT)
        
        self.deviceCombo = wx.ComboBox(panel, -1, size=(150, -1), choices=self.plugin.deviceAlias)
        panel.sizer.Add(self.deviceCombo, 0, wx.ALIGN_CENTER_VERTICAL)
        
        self.label1 = wx.StaticText(panel,label = "Select State" ,style = wx.ALIGN_LEFT) 
        panel.sizer.Add(self.label1, 0, wx.ALIGN_LEFT, 20)
        
        self.states = ["OFF", "ON"]        
        self.stateCombo = wx.ComboBox(panel, -1, size=(150, -1), choices=self.states)
        panel.sizer.Add(self.stateCombo, 0, wx.ALIGN_LEFT)
        
        while panel.Affirmed():
            device = self.plugin.devices[self.deviceCombo.GetCurrentSelection()]
            state = self.stateCombo.GetCurrentSelection()
            panel.SetResult(device, state)
        
def getDeviceFromAliasIndex(self, index):   
    return self.plugin.devices[index]
		
class KasaPlugin(eg.PluginBase):
	def __init__(self): 
	  print "Kasa Plugin is inited."
	  self.AddAction(Authenticate)
	  self.AddAction(GetDeviceList)
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