from ..helpers import PluginImporter
importer = PluginImporter(virtual='interest.plugins.', actual='interest_')
importer.register()
del PluginImporter
del importer
