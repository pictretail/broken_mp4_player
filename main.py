import os

from app_state import state
from dotenv import load_dotenv
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.login_screen import LoginScreen
from screens.reach_segment_table import ReachSegmentTable

load_dotenv(".env.development")  # Load environment variables from .env.
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
if AUTH_TOKEN:
    state.token = AUTH_TOKEN


class FilePickerApp(MDApp):

    def build(self):
        sm = ScreenManager()

        # Add screens to the screen manager
        screens = [
            LoginScreen(name="login"),
            ReachSegmentTable(name="reach_segment_table"),
        ]
        # if we're in development and need to skip the login screen we'll reversed
        # order of the screens
        if AUTH_TOKEN:
            screens = screens[::-1]
        for screen in screens:
            sm.add_widget(screen)

        return sm


if __name__ == "__main__":
    FilePickerApp().run()
