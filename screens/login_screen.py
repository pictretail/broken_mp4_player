from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color


# Define the LoginScreen class
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        # Set the background color
        with self.canvas.before:
            Color(0.945, 0.953, 0.957, 1)  # This is the RGB equivalent of #F1F3F4
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        # Use AnchorLayout to center the content
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10,
            size_hint=(None, None),
            width=300,
        )
        layout.bind(
            minimum_height=layout.setter("height")
        )  # Adjust height to fit contents

        # Set default sizes for inputs and buttons
        input_height = 40
        button_height = 50

        # Add the logo image
        logo = Image(source='assets/logo.png', size_hint_y=None, height=100)  # Adjust height as needed
        layout.add_widget(logo)

        # Username input
        self.username = TextInput(
            hint_text="Username", multiline=False, size_hint_y=None, height=input_height
        )
        self.username.bind(on_focus=self.on_focus)
        self.username.bind(on_enter=self.on_enter, on_leave=self.on_leave)
        layout.add_widget(self.username)

        # Password input
        self.password = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=input_height,
        )
        self.password.bind(on_focus=self.on_focus)
        self.password.bind(on_enter=self.on_enter, on_leave=self.on_leave)
        layout.add_widget(self.password)

        # Login button
        login_button = Button(text="Login", size_hint_y=None, height=button_height)
        login_button.bind(on_release=self.validate_credentials)
        layout.add_widget(login_button)

        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def on_focus(self, instance, value):
        """Change the cursor when the TextInput is focused or unfocused."""
        if value:  # If focused, change to the 'ibeam' cursor
            Window.set_system_cursor("ibeam")
        else:  # If unfocused, revert to the default cursor
            Window.set_system_cursor("arrow")

    def validate_credentials(self, instance):
        username = self.username.text
        password = self.password.text

        # For simplicity, assume the correct credentials are "user" and "pass"
        if username == "user" and password == "pass":
            self.manager.current = "filepicker"
        else:
            popup = Popup(
                title="Login Failed",
                content=Label(text="Invalid username or password."),
                size_hint=(0.6, 0.4),
            )
            popup.open()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
