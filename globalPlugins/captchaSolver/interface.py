import wx
import threading
import addonHandler
import gui
import _config

addonHandler.initTranslation()

class SettingsDialog(gui.SettingsDialog):
	title = _('Captcha Solver Settings')

	def makeSettings(self, sizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=sizer)

		self.regsense = wx.CheckBox(self, label=_('Case sensitive recognition'))
		self.regsense.SetValue(_config.conf['regsense'])
		settingsSizerHelper.addItem(self.regsense)

		self.https = wx.CheckBox(self, label=_('Use HTTPS'))
		self.https.SetValue(_config.conf['https'])
		settingsSizerHelper.addItem(self.https)

		self.sizeReport = wx.CheckBox(self, label=_('Size image report'))
		self.sizeReport.SetValue(_config.conf['sizeReport'])
		settingsSizerHelper.addItem(self.sizeReport)

		self.textInstruction = wx.CheckBox(self, label=_('Send text instruction'))
		self.textInstruction.SetValue(_config.conf['textInstruction'])
		settingsSizerHelper.addItem(self.textInstruction)

		self.language = settingsSizerHelper.addLabeledControl(_('Image language:'), wx.Choice, choices=[_('Undefined'), _('Only Cyrillic alphabet'), _('Only Latin alphabet')])
		self.language.SetSelection(_config.conf['language'])

		self.key = settingsSizerHelper.addLabeledControl(_('API key:'), wx.TextCtrl, value=_config.conf['key'].decode('utf-8'))

	def postInit(self):
		self.regsense.SetFocus()

	def onOk(self, event):
		super(SettingsDialog, self).onOk(event)
		_config.conf['regsense'] = self.regsense.Value
		_config.conf['https'] = self.https.Value
		_config.conf['sizeReport'] = self.sizeReport.Value
		_config.conf['textInstruction'] = self.textInstruction.Value
		_config.conf['language'] = self.language.GetSelection()
		_config.conf['key'] = self.key.Value.encode('utf-8')
		_config.saveConfig()

def createMenuItem():
	prefsMenu = gui.mainFrame.sysTrayIcon.menu.GetMenuItems()[1].GetSubMenu()
	captchaSolverSettingsItem = prefsMenu.Append(wx.ID_ANY, _('Captcha Solver Settings...'))
	gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, showSettingsDialog, captchaSolverSettingsItem)

def showSettingsDialog(evt=None):
	gui.mainFrame._popupSettingsDialog(SettingsDialog)

def getInstruction(callback, **kwargs):
	if _config.conf['textInstruction']:
		dlg = wx.TextEntryDialog(gui.mainFrame, _('Instruction text (maximum 140 characters):'), _('Text instruction'))
		gui.mainFrame.prePopup()
		status = dlg.ShowModal()
		gui.mainFrame.postPopup()
		text = dlg.GetValue()
		dlg.Destroy()
		if status != wx.ID_OK:
			return
		kwargs['textinstructions'] = text[:140].encode('utf-8')
	threading.Thread(target=callback, kwargs=kwargs).start()
