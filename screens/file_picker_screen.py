import os
import cv2
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from threading import Thread


class FilePickerScreen(MDScreen):

    def __init__(self, **kwargs):
        super(FilePickerScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Label for instructions
        self.label = MDLabel(text='Select an MP4 file:', size_hint=(1, 0.1), halign='center')
        self.add_widget(self.label)

        # Label to display selected file path
        self.file_path_label = MDLabel(text='', size_hint=(1, 0.1), halign='center')
        self.add_widget(self.file_path_label)

        # Browse button to open file picker
        self.browse_button = MDRaisedButton(text='Browse', size_hint=(1, 0.1))
        self.browse_button.bind(on_release=self.show_file_picker)
        self.add_widget(self.browse_button)

        # Play button to start the video
        self.play_button = MDRaisedButton(text='Play Video', size_hint=(1, 0.1))
        self.play_button.bind(on_release=self.play_video)
        self.play_button.disabled = True
        self.add_widget(self.play_button)

        # Initialize file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path,
        )

    def show_file_picker(self, instance):
        # Open the file manager
        user_home = os.path.expanduser('~')
        self.file_manager.show(user_home)  # Provide the path to open the file manager

    def select_path(self, path):
        # Handle the file selection
        self.file_path_label.text = path
        self.play_button.disabled = False
        self.exit_file_manager()

    def exit_file_manager(self, *args):
        # Close the file manager
        self.file_manager.close()

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
        screen_width = 1280
        screen_height = 720

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
            w = frame.shape[1]
            h = frame.shape[0]

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

            if cv2.getWindowProperty(videoName, cv2.WND_PROP_VISIBLE) < 1:
                break

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

