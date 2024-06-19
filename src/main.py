from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import cv2
from camera_feed import get_camera_feed
from utils import setup_logging, log_event, log_error, read_config
from auth import check_credentials

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)

    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if check_credentials(username, password):
            self.parent.switch_to_main()
        else:
            log_error('Invalid login attempt')
            self.password_input.text = ''
            self.username_input.text = ''

class MultiCamApp(App):
    def build(self):
        setup_logging()
        log_event('Application started')

        self.layout = BoxLayout(orientation='vertical')

        config = read_config('config/config.ini')

        # Define the camera feeds configuration from config
        self.cameras = [
            {"ip": config['DEFAULT']['camera1_ip'], "port": config['DEFAULT']['camera1_port']},
            {"ip": config['DEFAULT']['camera2_ip'], "port": config['DEFAULT']['camera2_port']},
            {"ip": config['DEFAULT']['camera3_ip'], "port": config['DEFAULT']['camera3_port']},
            {"ip": config['DEFAULT']['camera4_ip'], "port": config['DEFAULT']['camera4_port']}
        ]

        # Create an image widget for each camera feed
        self.images = []
        for _ in self.cameras:
            img = Image()
            self.images.append(img)
            self.layout.add_widget(img)

        # Schedule the update function to run at 30 FPS
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout

    def update(self, dt):
        for i, cam in enumerate(self.cameras):
            try:
                frame = get_camera_feed(cam['ip'], cam['port'])
                if frame is not None:
                    buf = cv2.flip(frame, 0).tostring()
                    texture = self.images[i].texture
                    if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                        texture.flip_vertical()
                    texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.images[i].texture = texture
                else:
                    log_error(f'Failed to fetch frame from {cam["ip"]}:{cam["port"]}')
            except Exception as e:
                log_error(f'Error updating camera feed from {cam["ip"]}:{cam["port"]}: {e}')

    def switch_to_main(self):
        self.root.clear_widgets()
        self.root.add_widget(self.layout)

    def on_start(self):
        self.root = BoxLayout(orientation='vertical')
        login_screen = LoginScreen()
        self.root.add_widget(login_screen)
        self.layout = self.build()
        return self.root

if __name__ == '__main__':
    MultiCamApp().run()