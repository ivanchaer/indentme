import sys
import imp

# Dependecy reloader for Emmet plugin
# The original idea is borrowed from 
# https://github.com/wbond/sublime_package_control/blob/master/package_control/reloader.py 

reload_mods = []
for mod in sys.modules:
	if mod.startswith('indentme_modules') and sys.modules[mod] != None:
		reload_mods.append(mod)

mods_load_order = [
  'indentme_modules',
	'indentme_modules.indent',
	'indentme_modules.unindent',
  'indentme_modules.parser'
]

for mod in mods_load_order:
	if mod in reload_mods:
		imp.reload(sys.modules[mod])
