import requests
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
from dotenv import load_dotenv
import os

load_dotenv(".env.development")  # take environment variables from .env.
API_URL = os.getenv("API_URL")


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
        logo = Image(
            source="assets/logo.png", size_hint_y=None, height=100
        )  # Adjust height as needed
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

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def validate_credentials(self, instance):
        username = self.username.text
        password = self.password.text

        # Load the GraphQL mutation from the file
        with open('graphql/login_mutation.gql', 'r') as file:
            query = file.read()

        variables = {
            "username": username,
            "password": password
        }

        json_data = {
            "operationName": "loginUser",
            "query": query,
            "variables": variables
        }

        try:
            # Send the request
            response = requests.post(
                'http://localhost:8000/graphql_internal',
                json=json_data
            )
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            data = response.json()

            # Check if the response contains the expected data
            if 'data' in data and data['data'].get('loginUser'):
                token = data['data']['loginUser'].get('token')
                if token:
                    # Handle successful login
                    self.manager.current = 'filepicker'
                else:
                    self.show_error("Login failed. Invalid credentials.")
            else:
                self.show_error("Login failed. Please check your credentials.")
        except requests.exceptions.HTTPError as http_err:
            self.show_error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            self.show_error(f"An error occurred: {err}")

    def on_enter(self):
        # Set focus to username input when the screen is shown
        self.username.focus = True

    def show_error(self, message):
        content = BoxLayout(orientation='vertical')
        
        # Add the message label
        message_label = Label(text=message)
        content.add_widget(message_label)
        
        # Add a close button
        close_button = Button(text='Close', size_hint=(1, 0.25))
        content.add_widget(close_button)
        
        popup = Popup(
            title='Login Error',
            content=content,
            size_hint=(0.6, 0.4)
        )
        
        # Bind the close button to dismiss the popup
        close_button.bind(on_release=popup.dismiss)
        
        popup.open()
