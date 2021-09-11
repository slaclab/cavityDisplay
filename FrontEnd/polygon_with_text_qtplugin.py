from pydm.widgets.qtplugin_base import qtplugin_factory, WidgetCategory
from pydm.widgets.qtplugin_extensions import RulesExtension
from cavityWidget import CavityWidget

# plugin
print("Loading custom PyDMDrawingPolyon with text!")
PyDMDrawingPolygonText = qtplugin_factory(CavityWidget, group=WidgetCategory.DISPLAY, is_container=True, extensions=[RulesExtension])