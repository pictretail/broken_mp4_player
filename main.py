import os
import sys
import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from threading import Thread
from kivy.uix.anchorlayout import AnchorLayout

class FilePicker(BoxLayout):

    def __init__(self, **kwargs):
        super(FilePicker, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create an AnchorLayout to position the instructions button
        anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='right', anchor_y='top')
        
        self.instructions_button = Button(text='?', size_hint=(None, None), size=(40, 40))
        self.instructions_button.bind(on_release=self.show_instructions)
        anchor_layout.add_widget(self.instructions_button)

        self.add_widget(anchor_layout)

        self.label = Label(text='Select an MP4 file:', size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.file_path_label = Label(text='', size_hint=(1, 0.1))
        self.add_widget(self.file_path_label)

        self.browse_button = Button(text='Browse', size_hint=(1, 0.1))
        self.browse_button.bind(on_release=self.show_file_picker)
        self.add_widget(self.browse_button)

        self.play_button = Button(text='Play Video', size_hint=(1, 0.1))
        self.play_button.bind(on_release=self.play_video)
        self.play_button.disabled = True
        self.add_widget(self.play_button)


    def show_file_picker(self, instance):
        content = BoxLayout(orientation='vertical')
        user_home = os.path.expanduser('~')
        filechooser = FileChooserListView(filters=['*.mp4'], path=user_home)
        content.add_widget(filechooser)

        select_button = Button(text='Select', size_hint=(1, 0.1))
        content.add_widget(select_button)

        popup = Popup(title='File Picker', content=content, size_hint=(0.9, 0.9))

        def on_select(instance):
            selected = filechooser.selection
            if selected:
                self.file_path_label.text = selected[0]
                self.play_button.disabled = False
                popup.dismiss()

        select_button.bind(on_release=on_select)
        popup.open()

    def play_video(self, instance):
        video_path = self.file_path_label.text
        if video_path:
            Thread(target=self.show_video, args=(video_path,), daemon=True).start()

    def show_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        videoName = 'video'
        key = 'f'
        runmode = 0
        cv2.namedWindow(videoName)

        # Get screen size
        screen_width = 1280  # or use another method to get actual screen width
        screen_height = 720  # or use another method to get actual screen height

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
            w = frame.shape[1]
            h = frame.shape[0]

            # Calculate new size maintaining the aspect ratio
            aspect_ratio = w / h
            if w > screen_width or h > screen_height:
                if w / screen_width > h / screen_height:
                    new_w = screen_width
                    new_h = int(screen_width / aspect_ratio)
                else:
                    new_h = screen_height
                    new_w = int(screen_height * aspect_ratio)
                frame = cv2.resize(frame, (new_w, new_h))

            cv2.putText(
                frame,
                str(int(frame_number)),
                (int(new_w / 2), int(new_h * 5 / 6)),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 0, 0),
                12
            )

            cv2.imshow(videoName, frame)
            key = cv2.waitKey(runmode) & 0xFF
            if key == ord('f'):
                runmode = 0
            elif key == ord('r'):
                runmode = 40
            elif key == ord('b'):
                frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
                frame_number = frame_number - 30
                if frame_number < 0:
                    frame_number = 0
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                runmode = 0
                key = ord('f')
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Finished showing video")

    def show_instructions(self, instance):
        instructions = (
            "Usage Instructions:\n\n"
            "1. Click 'Browse' to select an MP4 file.\n"
            "2. Once a file is selected, click 'Play Video' to play the video.\n"
            "3. Use the following controls while the video is playing:\n"
            "   - 'f': Tap or hold down to move through video frame by frame.\n"
            "   - 'r': Resume video playback.\n"
            "   - 'b': Skip back 30 frames.\n"
            "   - 'q': Quit the video playback."
        )
        content = BoxLayout(orientation='vertical')
        label = Label(text=instructions, size_hint=(1, 0.9))
        close_button = Button(text='Close', size_hint=(1, 0.1))
        content.add_widget(label)
        content.add_widget(close_button)

        popup = Popup(title='Instructions', content=content, size_hint=(0.9, 0.9))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

class FilePickerApp(App):
    def build(self):
        return FilePicker()

if __name__ == '__main__':
    FilePickerApp().run()

