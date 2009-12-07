import inspect
from django.forms import Widget
from django.forms import widgets as default_widgets
from django.forms.extras import widgets as extra_widgets

__all__ = ['library']

NAME_TRANSFORMS = {
    'CheckboxInput': 'checkbox',
    'CheckboxSelectMultiple': 'multicheckbox',
    'DateInput': 'date',
    'DateTimeInput': 'datetime',
    'FileInput': 'file',
    'HiddenInput': 'hidden',
    'Input': 'input',
    'MultipleHiddenInput': 'multihidden',
    'NullBooleanSelect': 'nullbooleanselect',
    'PasswordInput': 'password',
    'RadioSelect': 'radioselect',
    'SelectDate': 'selectdate',
    'SelectMultiple': 'multiselect',
    'Select': 'select',
    'SplitDateTimeWidget': 'splitdatetime',
    'SplitHiddenDateTimeWidget': 'splithiddendatatime',
    'TextInput': 'text',
    'Textarea': 'textarea',
    'TimeInput': 'time',
}

class WidgetLibrary(object):
    """
    A library of all widgets. Unlike Django models, registration is explicit
    (no autodiscovery except for built-ins).

    A single instance of the class is expected. It is located at:
        form_widgets.loading.library
    """
    widgets = {}
    initialized = False

    def _initialize(self):
        """
        Make sure that the library is populated with at least the default
        widgets (the stuff in Django core).
        """
        builtin_widgets = {}

        # Load default widgets
        self.load_all_widgets(default_widgets, into=builtin_widgets)
        self.load_all_widgets(extra_widgets, into=builtin_widgets)

        # Overwrite the defaults with anything already registered
        # We do this to make sure that 
        builtin_widgets.update(self.widgets)

        self.widgets = builtin_widgets

        self.initialized = True

    def load_all_widgets(self, module, truncate="Widget", into=None):
        tally = 0
        into = into or self.widgets
        for i in dir(module):
            obj = getattr(module, i)
            if inspect.isclass(obj) and issubclass(obj, Widget):
                name = obj.__name__
                if name in NAME_TRANSFORMS:
                    name = NAME_TRANSFORMS[name]
                elif truncate and name.endswith(truncate):
                    name = name[:-len(truncate)]
                into[name] = obj
                tally += 1
        return tally

    def register(self, widget, name=None):
        name = name or widget.__class__.__name__
        self.widgets[name] = widget

    def get_widget(self, name):
        if not self.initialized:
            self._initialize()
        return self.widgets.get(name)

library = WidgetLibrary()
