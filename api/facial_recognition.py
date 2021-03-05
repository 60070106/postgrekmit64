
import face_recognition

from django.conf import settings

# fileCheck = sys.argv[1]

save_path = "%s"%(settings.BASE_DIR)+"\images\\"

def facedetect(fileCheck):
    send_to_check_fileName = save_path + fileCheck

    send_to_check_Pic = face_recognition.load_image_file(send_to_check_fileName) # ไฟล์ที่ต้องการตรวจสอบ
    send_to_check_face_encoding = face_recognition.face_encodings(send_to_check_Pic) # เข้ารหัสหน้าตา

    if len(send_to_check_face_encoding) > 0:
        print(True)
    else:
        print(False)
