from ..helpers import PluginImporter


importer = PluginImporter(source='interest.plugins.', target='interest_')
importer.register()
