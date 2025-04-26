import os 
import shutil
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

# Tải biến môi trường từ file .env
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Đường dẫn tuyệt đối đến file database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database", "vina.sqlite3")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backup")

# Tạo thư mục backup nếu chưa tồn tại
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Mail đã được gửi thành công.")
    except Exception as e:
        print(f"Mail đã gửi thất bại: {e}")

def backup_database():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"backup_{now}.sqlite3")

    try:
        # Kiểm tra file database có tồn tại không
        if not os.path.exists(DB_FILE):
            raise FileNotFoundError(f"Koo tìm thấy file database: {DB_FILE}")

        shutil.copy(DB_FILE, backup_file)
        print(f"Gửi backup thành công: {backup_file}")
        send_email(
            subject="gửi backup thành công ",
            body=f"Thao tác thành công vào lúc {now}.\nFile được lưu với tên: {os.path.basename(backup_file)}"
        )
    except Exception as e:
        print(f"Backup Lỗi: {e}")
        send_email(
            subject="Gửi backup thất bại ",
            body=f"Lỗi trong quá trình backup:\n{e}"
        )
    
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Mail đã được gửi thành công.")
    except Exception as e:
        print(f"Mail đã gửi thất bại: {e}")

schedule.every().day.at("20:54").do(backup_database)

print("...Mail sẽ được gửi tới bạn nhanh thôi...")

while True:
    schedule.run_pending()
    time.sleep(1)