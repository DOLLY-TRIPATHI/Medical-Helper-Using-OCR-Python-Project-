import pytesseract
from PIL import Image
import sched
import time
from playsound import playsound

# Set path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

count = 0

# -----------------------------PROVIDING DISEASE STATUS---------------------------------------

def add_patient_data(patient_data, patient_id, data):
    patient_data[patient_id] = data

def make_decision(patient_data, patient_id):
    data = patient_data.get(patient_id)
    if not data:
        return "Patient data not found."

    if data['age'] > 60:
        return "High risk for cardiovascular disease."
    elif data['temperature'] > 38.0:
        return "Fever detected. Possible infection."
    else:
        return "No significant issues detected."

patient_data = {}

# Take input for patient data
patient_id = int(input("Enter patient ID: "))
age = int(input("Enter patient age: "))
temperature = float(input("Enter patient temperature: "))
heart_rate = int(input("Enter patient heart rate: "))

add_patient_data(patient_data, patient_id, {'age': age, 'temperature': temperature, 'heart_rate': heart_rate})

decision_patient = make_decision(patient_data, patient_id)

#-----------------------------------MEDICAL HELPER  USING OCR-------------------------------

def ocr_medical_text(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        return f"Error reading image: {e}"

# Playing reminder sound   
def play_reminder_sound():
    try:
        playsound(r"D:\classroom\Document from Dolly Tripathi.mp3")  # Correct file path
    except Exception as e:
        print(f"Error playing sound: {e}")

scheduler = sched.scheduler(time.time, time.sleep) 

def remind_extracted_text(image_path):
    global count
    count += 1
    print("Reminder: Don't forget to take your medicine timely!")
    play_reminder_sound()

    if count <= 2:
        scheduler.enter(10, 1, remind_extracted_text, argument=(image_path,))
    else:
        print("Reminder Worked Successfully")

def main():
    image_path = r"D:\classroom\Photo from Dolly Tripathi - Copy.jpg"  
    print("Decision for Patient:", decision_patient)

    extracted_text = ocr_medical_text(image_path)
    print("Extracted Text:", extracted_text)

    scheduler.enter(10, 1, remind_extracted_text, argument=(image_path,))
    scheduler.run()

if __name__ == "__main__":
    main()
