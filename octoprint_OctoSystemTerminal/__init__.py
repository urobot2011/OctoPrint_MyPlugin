# coding=utf-8
from __future__ import absolute_import
import asyncio
import websockets
import subprocess 

import octoprint.plugin

class OctoSystemTerminalPlugin(octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			use_plugin=False
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			js=["js/OctoSystemTerminal.js"]
		)
		
	#~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [
			#dict(type="sidebar", icon="arrows-alt"),
			dict(type="settings")
		]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			BedLevelingWizard=dict(
				displayName="OctoPrint-OctoSystemTerminal",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="urobot2011",
				repo="OctoPrint-OctoSystemTerminal",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/urobot2011/OctoPrint_MyPlugin/OctoPrint-OctoSystemTerminal/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Octo System Terminal"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctoSystemTerminalPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
	start_server = websockets.serve(accept, "localhost", 9998)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
	async def accept(websocket, path):
		while True:
			data = await websocket.recv()
			#print("receive : " + data)
			output_data = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = time.communicate()
			await websocket.send("echo : " + output)
