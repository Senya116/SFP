import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock
import requests
import json
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
from qr_scanner import scan_qr_code

class FridgeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.holodilnik_label = Label(text="Holodilnik")
        self.layout.add_widget(self.holodilnik_label)

        self.holodilnik_list = ScrollView()
        self.holodilnik_layout = BoxLayout(orientation='vertical')
        self.holodilnik_list.add_widget(self.holodilnik_layout)
        self.layout.add_widget(self.holodilnik_list)

        self.search_layout = BoxLayout(orientation='horizontal')
        self.search_input = TextInput(hint_text="Search product")
        self.search_button = Button(text="Search")
        self.search_button.bind(on_press=self.search_product)
        self.search_layout.add_widget(self.search_input)
        self.search_layout.add_widget(self.search_button)
        self.layout.add_widget(self.search_layout)

        self.add_button = Button(text="Add Product")
        self.add_button.bind(on_press=self.add_product)
        self.layout.add_widget(self.add_button)

        self.remove_button = Button(text="Remove Product by QR")
        self.remove_button.bind(on_press=self.remove_product_by_qr)
        self.layout.add_widget(self.remove_button)

        self.custom_list_button = Button(text="Custom List")
        self.custom_list_button.bind(on_press=self.show_custom_list)
        self.layout.add_widget(self.custom_list_button)

        self.analytics_button = Button(text="Analytics")
        self.analytics_button.bind(on_press=self.show_analytics)
        self.layout.add_widget(self.analytics_button)

        self.update_holodilnik()
        return self.layout

    def update_holodilnik(self):
        response = requests.get('http://127.0.0.1:5000/get_fridge')
        holodilnik = response.json()
        print(f"Holodilnik contents: {holodilnik}")  # Отладочное сообщение
        self.holodilnik_layout.clear_widgets()
        for product in holodilnik:
            expiry_date = datetime.strptime(product['expiry_date'], '%Y-%m-%d')
            today = datetime.now()
            status = ''
            if expiry_date < today:
                status = '!!!ПРОСРОЧЕНО!!!'
            elif (expiry_date - today).days <= 3:
                status = 'Скоро истечёт срок годности!'
            product_layout = BoxLayout(orientation='horizontal')
            product_label = Label(text=f"{product['name']} - {product['mass_volume']} {product['unit']} ({status})")
            info_button = Button(text="Info")
            info_button.bind(on_press=lambda x, name=product['name']: self.show_product_info(name))
            product_layout.add_widget(product_label)
            product_layout.add_widget(info_button)
            self.holodilnik_layout.add_widget(product_layout)

    def search_product(self, instance):
        search_query = self.search_input.text.strip()
        response = requests.get('http://127.0.0.1:5000/get_fridge')
        holodilnik = response.json()
        search_results = [product for product in holodilnik if search_query.lower() in product['name'].lower()]

        search_popup = Popup(title='Search Results', size_hint=(None, None), size=(600, 600))
        search_layout = BoxLayout(orientation='vertical')

        for product in search_results:
            product_label = Label(text=f"{product['name']} - {product['expiry_date']}")
            search_layout.add_widget(product_label)

        search_popup.add_widget(search_layout)
        search_popup.open()

    def add_product(self, instance):
        camera_popup = Popup(title='Scan QR Code', size_hint=(None, None), size=(600, 600))
        camera_layout = BoxLayout(orientation='vertical')
        camera = Camera(resolution=(640, 480), play=True)
        camera_layout.add_widget(camera)
        camera_popup.add_widget(camera_layout)
        camera_popup.open()

        def capture_image(instance):
            camera.export_to_png("captured_image.png")
            barcode_data = scan_qr_code("captured_image.png")
            if barcode_data:
                product_info = json.loads(barcode_data)
                print(f"Scanned product info: {product_info}")  # Отладочное сообщение
                self.show_product_confirmation(product_info)
                camera_popup.dismiss()
            else:
                print("No QR code found")

        capture_button = Button(text="Capture")
        capture_button.bind(on_press=capture_image)
        camera_layout.add_widget(capture_button)

    def show_product_confirmation(self, product_info):
        confirmation_popup = Popup(title='Product Info', size_hint=(None, None), size=(600, 600))
        confirmation_layout = BoxLayout(orientation='vertical')

        info_text = (f"Name: {product_info['name']}\n"
                     f"Type: {product_info['type']}\n"
                     f"Manufacture Date: {product_info['manufacture_date']}\n"
                     f"Expiry Date: {product_info['expiry_date']}\n"
                     f"Mass/Volume: {product_info['mass_volume']} {product_info['unit']}\n"
                     f"Nutritional Value: {product_info['nutritional_value']}\n"
                     f"Measurement Type: {product_info['measurement_type']}")

        info_label = Label(text=info_text)
        confirmation_layout.add_widget(info_label)

        add_button = Button(text="Добавить")
        add_button.bind(on_press=lambda x: self.confirm_add_product(product_info, confirmation_popup))
        confirmation_layout.add_widget(add_button)

        cancel_button = Button(text="Не добавлять")
        cancel_button.bind(on_press=lambda x: confirmation_popup.dismiss())
        confirmation_layout.add_widget(cancel_button)

        confirmation_popup.add_widget(confirmation_layout)
        confirmation_popup.open()

    def confirm_add_product(self, product_info, popup):
        response = requests.post('http://127.0.0.1:5000/add_product', json=product_info)
        print(f"Server response: {response.json()}")  # Отладочное сообщение
        popup.dismiss()
        self.update_holodilnik()

    def remove_product_by_qr(self, instance):
        camera_popup = Popup(title='Scan QR Code to Remove', size_hint=(None, None), size=(600, 600))
        camera_layout = BoxLayout(orientation='vertical')
        camera = Camera(resolution=(640, 480), play=True)
        camera_layout.add_widget(camera)
        camera_popup.add_widget(camera_layout)
        camera_popup.open()

        def capture_image(instance):
            camera.export_to_png("captured_image.png")
            barcode_data = scan_qr_code("captured_image.png")
            if barcode_data:
                product_info = json.loads(barcode_data)
                print(f"Scanned product info: {product_info}")  # Отладочное сообщение
                response = requests.post('http://127.0.0.1:5000/remove_product_by_qr', json=product_info)
                print(f"Server response: {response.json()}")  # Отладочное сообщение
                camera_popup.dismiss()
                self.update_holodilnik()
            else:
                print("No QR code found")

        capture_button = Button(text="Capture")
        capture_button.bind(on_press=capture_image)
        camera_layout.add_widget(capture_button)

    def show_product_info(self, name):
        response = requests.get(f'http://127.0.0.1:5000/get_product?name={name}')
        product_info = response.json()
        if 'message' in product_info:
            info_text = product_info['message']
        else:
            info_text = (f"Name: {product_info['name']}\n"
                         f"Type: {product_info['type']}\n"
                         f"Manufacture Date: {product_info['manufacture_date']}\n"
                         f"Expiry Date: {product_info['expiry_date']}\n"
                         f"Mass/Volume: {product_info['mass_volume']} {product_info['unit']}\n"
                         f"Nutritional Value: {product_info['nutritional_value']}\n"
                         f"Measurement Type: {product_info['measurement_type']}")

        info_popup = Popup(title='Product Info', size_hint=(None, None), size=(600, 600))
        info_label = Label(text=info_text)
        info_popup.add_widget(info_label)
        info_popup.open()

    def show_custom_list(self, instance):
        response = requests.get('http://127.0.0.1:5000/get_custom_list')
        custom_list = response.json()
        custom_list_popup = Popup(title='Custom List', size_hint=(None, None), size=(600, 600))
        custom_list_layout = BoxLayout(orientation='vertical')

        for product in custom_list:
            product_layout = BoxLayout(orientation='horizontal')
            product_label = Label(text=f"{product['name']}")
            info_button = Button(text="Info")
            info_button.bind(on_press=lambda x, name=product['name']: self.show_product_info(name))
            product_layout.add_widget(product_label)
            product_layout.add_widget(info_button)
            custom_list_layout.add_widget(product_layout)

        add_product_layout = BoxLayout(orientation='horizontal')
        new_product_name = TextInput(hint_text="Product name")
        add_button = Button(text="Add")
        add_button.bind(on_press=lambda x: self.add_to_custom_list(new_product_name.text))
        add_product_layout.add_widget(new_product_name)
        add_product_layout.add_widget(add_button)
        custom_list_layout.add_widget(add_product_layout)

        custom_list_popup.add_widget(custom_list_layout)
        custom_list_popup.open()

    def add_to_custom_list(self, name):
        if name:
            product_info = {"name": name}
            response = requests.post('http://127.0.0.1:5000/add_to_custom_list', json=product_info)
            print(f"Server response: {response.json()}")  # Отладочное сообщение
            self.show_custom_list(None)

    def remove_from_custom_list(self, name):
        product_info = {"name": name}
        response = requests.post('http://127.0.0.1:5000/remove_from_custom_list', json=product_info)
        print(f"Server response: {response.json()}")  # Отладочное сообщение
        self.show_custom_list(None)

    def show_analytics(self, instance):
        analytics_popup = Popup(title='Analytics', size_hint=(None, None), size=(600, 600))
        analytics_layout = BoxLayout(orientation='vertical')
        start_date_input = TextInput(hint_text="Start Date (YYYY-MM-DD)")
        end_date_input = TextInput(hint_text="End Date (YYYY-MM-DD)")
        analytics_layout.add_widget(start_date_input)
        analytics_layout.add_widget(end_date_input)
        analytics_button = Button(text="Show Analytics")
        analytics_button.bind(on_press=lambda x: self.get_analytics(start_date_input.text, end_date_input.text))
        analytics_layout.add_widget(analytics_button)
        analytics_popup.add_widget(analytics_layout)
        analytics_popup.open()

    def get_analytics(self, start_date, end_date):
        response = requests.get(f'http://127.0.0.1:5000/analytics?start_date={start_date}&end_date={end_date}')
        analytics_data = response.json()
        analytics_popup = Popup(title='Analytics Data', size_hint=(None, None), size=(1200, 600))
        analytics_label = Label(text=str(analytics_data))
        analytics_popup.add_widget(analytics_label)
        analytics_popup.open()

    def check_notifications(self, dt):
        response = requests.get('http://127.0.0.1:5000/notifications')
        notifications = response.json()
        for notification in notifications:
            print(f"Notification: {notification['name']} - {notification['status']}")

    def on_start(self):
        Clock.schedule_interval(self.check_notifications, 60)  # Проверка уведомлений каждую минуту

if __name__ == '__main__':
    FridgeApp().run()