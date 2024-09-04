import os

import requests
from app_state import state
from dotenv import load_dotenv
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

load_dotenv(".env.development")  # Load environment variables from .env.
API_URL = os.getenv("API_URL")


# Define the LoginScreen class
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Set the background color
        with self.canvas.before:
            Color(0.945, 0.953, 0.957, 1)  # This is the RGB equivalent of #F1F3F4
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Use AnchorLayout to center the content
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        layout = MDBoxLayout(
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
        self.username = MDTextField(
            on_text_validate=self.on_username_validate,
            hint_text="Username",
            mode="rectangle",
            size_hint_y=None,
            height=input_height,
        )
        self.username.bind(on_focus=self.on_focus)
        layout.add_widget(self.username)

        # Password input
        self.password = MDTextField(
            on_text_validate=self.on_password_enter,
            hint_text="Password",
            password=True,
            mode="rectangle",
            size_hint_y=None,
            height=input_height,
        )
        self.password.bind(on_focus=self.on_focus)
        layout.add_widget(self.password)

        # Login button
        login_button = MDRaisedButton(text="Login", size_hint_y=None, height=button_height)
        login_button.bind(on_release=self.validate_credentials)
        layout.add_widget(login_button)

        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def on_username_validate(self, instance):
        # Move focus to password input when Enter is pressed in username field
        self.password.focus = True

    def on_password_enter(self, instance):
        # Trigger login when Enter is pressed in password field
        self.validate_credentials(instance)

    def on_parent(self, widget, parent):
        # Set focus to username input when the screen is added to the parent
        self.username.focus = True

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
        with open("graphql/login_mutation.gql", "r") as file:
            query = file.read()

        variables = {"username": username, "password": password}

        json_data = {
            "operationName": "loginUser",
            "query": query,
            "variables": variables,
        }

        try:
            # Send the request
            response = requests.post(API_URL, json=json_data)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            data = response.json()

            # Check if the response contains the expected data
            if "data" in data and data["data"].get("loginUser"):
                state.token = data["data"]["loginUser"].get("token")
                if state.token:
                    # Handle successful login
                    self.manager.current = "reach_segment_table"
                else:
                    self.show_error("Login failed. Invalid credentials.")
            else:
                self.show_error("Login failed. Please check your credentials.")
        except requests.exceptions.HTTPError as http_err:
            self.show_error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            self.show_error(f"An error occurred: {err}")

    def show_error(self, message):
        # Use MDDialog to show error messages
        dialog = MDDialog(
            title="Login Error",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

