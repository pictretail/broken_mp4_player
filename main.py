import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from dotenv import load_dotenv
from screens.login_screen import LoginScreen
from screens.file_picker_screen import FilePickerScreen

load_dotenv('.env.development')  # take environment variables from .env.
api_url = os.getenv('API_URL')
print(api_url)


# Create the main application class
class FilePickerApp(App):

    def build(self):
        sm = ScreenManager()

        # Add screens to the screen manager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FilePickerScreen(name='filepicker'))

        return sm

if __name__ == '__main__':
    FilePickerApp().run()

