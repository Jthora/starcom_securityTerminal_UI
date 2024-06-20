from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import threading

class MultiCamApp(App):
    def build(self):
        self.is_full_screen = False
        self.full_screen_index = None
        
        # Main layout to hold the grid and full screen view
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Grid layout with 2 rows and 2 columns
        self.grid_layout = GridLayout(rows=2, cols=2)

        # Initial empty camera list
        self.cameras = []

        self.image_widgets = []
        self.label_widgets = []
        
        # Scan button
        self.scan_button = Button(text='Scan for Cameras', size_hint_y=None, height=50)
        self.scan_button.bind(on_press=self.scan_for_cameras)
        self.main_layout.add_widget(self.scan_button)
        
        # Add grid layout to the main layout
        self.main_layout.add_widget(self.grid_layout)

        # Placeholder for the full screen image
        self.full_screen_image = Image()
        self.full_screen_image.bind(on_touch_down=self.on_full_screen_touch)
        
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.main_layout

    def scan_for_cameras(self, instance):
        # Clear current cameras
        self.cameras.clear()
        self.grid_layout.clear_widgets()
        self.image_widgets.clear()
        self.label_widgets.clear()
        
        # Define IP and port ranges to scan
        local_ips = ['127.0.0.1']
        remote_ips = ['192.168.1.{}'.format(i) for i in range(100, 105)]
        ports = [8081, 8082]
        
        # Start scanning in a separate thread
        threading.Thread(target=self.scan_ips_and_ports, args=(local_ips + remote_ips, ports)).start()

    def scan_ips_and_ports(self, ips, ports):
        for ip in ips:
            for port in ports:
                if self.check_camera_feed(ip, port):
                    label = f"Camera at {ip}:{port}"
                    self.cameras.append({"ip": ip, "port": port, "status": "green", "label": label})
                    self.add_camera_widget(ip, label)
        
    def check_camera_feed(self, ip, port):
        try:
            cap = cv2.VideoCapture(f"http://{ip}:{port}")
            ret, _ = cap.read()
            cap.release()
            return ret
        except Exception as e:
            print(f"[ERROR] [Failed to fetch frame from {ip}:{port}] {e}")
            return False

    def add_camera_widget(self, ip, label):
        cam_layout = BoxLayout(orientation='vertical')
        img = Image()
        img.index = len(self.image_widgets)
        img.bind(on_touch_down=self.on_image_touch)
        self.image_widgets.append(img)
        lbl = Label(text=label, size_hint_y=None, height=30)
        self.label_widgets.append(lbl)
        cam_layout.add_widget(img)
        cam_layout.add_widget(lbl)
        self.grid_layout.add_widget(cam_layout)

    def on_image_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.is_full_screen = True
            self.full_screen_index = instance.index
            self.main_layout.clear_widgets()
            self.main_layout.add_widget(self.full_screen_image)
    
    def on_full_screen_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.is_full_screen = False
            self.main_layout.clear_widgets()
            self.main_layout.add_widget(self.scan_button)
            self.main_layout.add_widget(self.grid_layout)

    def update(self, dt):
        if self.is_full_screen:
            cam = self.cameras[self.full_screen_index]
            frame = self.get_camera_feed(cam['ip'], cam['port'])
            frame = self.draw_status_circle(frame, cam['status'])
            self.update_image(self.full_screen_image, frame)
        else:
            for i, cam in enumerate(self.cameras):
                frame = self.get_camera_feed(cam['ip'], cam['port'])
                frame = self.draw_status_circle(frame, cam['status'])
                self.update_image(self.image_widgets[i], frame)

    def update_image(self, image_widget, frame):
        if frame is not None:
            buf = cv2.flip(frame, 0).tostring()
            texture = image_widget.texture
            if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            image_widget.texture = texture
        else:
            # Create a blank image with error text
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, 'No Connection', (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
            buf = cv2.flip(frame, 0).tostring()
            texture = image_widget.texture
            if not texture or texture.size != (frame.shape[1], frame.shape[0]):
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            image_widget.texture = texture

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
        if frame is None:
            return None
        height, width = frame.shape[:2]
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

        cv2.circle(frame, (width - 30, 30), 20, color, -1)
        return frame

if __name__ == '__main__':
    MultiCamApp().run()