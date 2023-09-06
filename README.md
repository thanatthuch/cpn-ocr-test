![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/172fe52a-5d8f-4314-83d4-a36b5d0941e5)# cpn-ocr-test
For interview test

### สามารถ Pull code ไปรันเพื่อตรวจสอบ หรือ จาก Docker Hub 

### กรณีใช้ Docker Hub
 - docker pull thanatthuch/cpn-ocr:latest
 - docker run --name imagename -p 8888:8888 thanatthuch/cpn-ocr:latest

 - ใช้ body ในการ requests ด้วย POST method ไปที่ /slip-detect
 - body จากไฟล์ api_test_en.json และ api_test_th.json

### กรณีจะ Pull Code เพื่อตรวจสอบ
 - git pull https://github.com/thanatthuch/cpn-ocr-test.git
 - pip3 install --no-cache-dir --upgrade -r ./requirements.txt
 - apt-get update && apt-get install -y tesseract-ocr
 - cd app && python3 main.py

# ในเทสนี้จะทำเป็น Microservice ตัวอย่างสำหรับ เรียกใช้ Model ในการ Extract ข้อความบางส่วน
โดยที่จะใช้ Library หลักๆ ดังนี้
 1. opencv-python - ใช้สำหรับทำ Image processing ในการแยก บรรทัดปรับแต่งรูปภาพให้เหมาะสม และสกัดข้อมูลเพื่อนำไป Train model
 2. pytesseract   - ในส่วนนี้เพื่อความรวดเร็วในการทำเทสผู้ทำข้อสอบขอใช้ pytesseract ในการอ่านเฉพาะข้อความที่เป็นภาษาอังกฤษ และตัวเลขเพื่อความรวดเร็ว
 3. pytorch       - จะใช้สำหรับการ Train Model และ Predict สำหรับอ่านข้อความภาษาไทย
 4. fastapi       - ใช้เป็น Microservice เพื่อให้ง่ายต่อการใช้งาน และตรวจสอบผล
 5. base64        - สำหรับแปลงค่า ระหว่าง รูปภาพ กับ base64encode

# ตัวอย่างผลลัพธ์บางส่วน
* ตัวอย่างการทดสอบผลลัพธ์ในการอ่านสลิปของ CASA LAPIN และบริษัทอีซีลี่จำกัด
![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/590b4269-0dd2-4724-aaac-f0d93fa28d96)


![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/7354c21e-aac8-4024-9b2e-ed5cf0d90b6a)



