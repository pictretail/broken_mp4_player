from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class BrokenTextInput(TextInput):
    def __init__(self, tab_index=None, **kwargs):
        super(BrokenTextInput, self).__init__(**kwargs)
        self.tab_index = tab_index
        self.bind(on_focus=self._on_focus)

    def _on_focus(self, instance, value):
        if value:  # If focused
            Window.set_system_cursor('ibeam')
        else:  # If unfocused
            Window.set_system_cursor('arrow')

    def handle_tab(self, text_inputs):
        # Get the current index
        current_index = self.tab_index
        if current_index is not None:
            # Calculate the next index (loop around if needed)
            next_index = (current_index + 1) % len(text_inputs)
            # Find the input with the next tab_index and focus it
            for input_field in text_inputs:
                if input_field.tab_index == next_index:
                    input_field.focus = True
                    break
