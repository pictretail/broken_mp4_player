from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.file_picker_screen import FilePickerScreen
from screens.reach_segment_table import ReachSegmentTable

class FilePickerApp(MDApp):

    def build(self):
        sm = ScreenManager()

        # Add screens to the screen manager
        sm.add_widget(LoginScreen(name='login'))
        # sm.add_widget(FilePickerScreen(name='filepicker'))
        sm.add_widget(ReachSegmentTable(name='reach_segment_table'))

        return sm

if __name__ == '__main__':
    FilePickerApp().run()

