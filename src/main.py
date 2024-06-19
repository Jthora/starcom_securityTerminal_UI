from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class MultiCamApp(App):
    def build(self):
        # Use GridLayout with 2 rows and 2 columns
        self.layout = GridLayout(rows=2, cols=2)

        self.cameras = [
            {"ip": "192.168.1.101", "port": 8081},  # Camera 1
            {"ip": "192.168.1.102", "port": 8081},  # Camera 2
            {"ip": "192.168.1.103", "port": 8081},  # Camera 3
            {"ip": "192.168.1.103", "port": 8082},  # Camera 4
        ]

        self.images = []
        for _ in self.cameras:
            img = Image()
            self.images.append(img)
            self.layout.add_widget(img)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout

    def update(self, dt):
        for i, cam in enumerate(self.cameras):
            frame = self.get_camera_feed(cam['ip'], cam['port'])
            status = 'Connected' if frame is not None else 'No Camera Feed'
            if frame is not None:
                frame = self.draw_status_circle(frame, 'green')
                buf = cv2.flip(frame, 0).tostring()
                texture = self.images[i].texture
                if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.images[i].texture = texture
            else:
                # Create a blank image with error text
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                frame = self.draw_status_circle(frame, 'red')
                cv2.putText(frame, 'No Connection', (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
                buf = cv2.flip(frame, 0).tostring()
                texture = self.images[i].texture
                if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.images[i].texture = texture

    def get_camera_feed(self, ip, port):
        try:
            cap = cv2.VideoCapture(f"http://{ip}:{port}")
            ret, frame = cap.read()
            cap.release()
            if ret:
                return frame
            else:
                raise ValueError("Failed to fetch frame")
        except Exception as e:
            print(f"[ERROR] [Failed to fetch frame from {ip}:{port}] {e}")
            return None

    def draw_status_circle(self, frame, status):
        if status == 'green':
            color = (0, 255, 0)  # Green
        elif status == 'blue':
            color = (0, 0, 255)  # Blue
        elif status == 'yellow':
            color = (0, 255, 255)  # Yellow
        elif status == 'red':
            color = (0, 0, 255)  # Red
        else:
            color = (255, 255, 255)  # White, default case

        cv2.circle(frame, (30, 30), 20, color, -1)
        return frame

if __name__ == '__main__':
    MultiCamApp().run()