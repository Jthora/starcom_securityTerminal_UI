from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
import cv2
import numpy as np

class MultiCamApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, rows=2)

        self.cameras = [
            {"ip": "192.168.1.101", "port": 8081},  # Camera 1
            {"ip": "192.168.1.102", "port": 8081},  # Camera 2
            {"ip": "192.168.1.103", "port": 8081},  # Camera 3
            {"ip": "192.168.1.103", "port": 8082},  # Camera 4
        ]

        self.images = []
        self.labels = []
        for _ in self.cameras:
            img = Image()
            lbl = Label(text="Initializing...", size_hint_y=None, height=50)
            self.images.append(img)
            self.labels.append(lbl)
            self.layout.add_widget(img)
            self.layout.add_widget(lbl)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout

    def update(self, dt):
        for i, cam in enumerate(self.cameras):
            frame, status = self.get_camera_feed(cam['ip'], cam['port'])
            if frame is not None:
                buf = cv2.flip(frame, 0).tostring()
                texture = self.images[i].texture
                if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    texture.flip_vertical()
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.images[i].texture = texture
                self.labels[i].text = "Camera Online"
            else:
                # Create a blank image with error text
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, status, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                buf = cv2.flip(frame, 0).tostring()
                texture = self.images[i].texture
                if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    texture.flip_vertical()
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.images[i].texture = texture
                self.labels[i].text = status

    def get_camera_feed(self, ip, port):
        try:
            cap = cv2.VideoCapture(f"http://{ip}:{port}")
            ret, frame = cap.read()
            cap.release()
            if ret:
                return frame, "Camera Online"
            else:
                raise ValueError("Camera Offline")
        except Exception as e:
            return None, f"No Connection to {ip}"

if __name__ == '__main__':
    MultiCamApp().run()