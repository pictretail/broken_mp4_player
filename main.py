import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login.login_screen import LoginScreen
from screens.filepicker.file_picker_screen import FilePickerScreen

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

