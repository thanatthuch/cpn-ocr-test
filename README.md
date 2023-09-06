# cpn-ocr-test
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
 2. pytesseract   - ในส่วนนี้เพื่อความรวดเร็วในการทำเทสผู้่ทำข้อสอบขอใช้ pytesseract ในการอ่านเฉพาะข้อความที่เป็นภาษาอังกฤษ และตัวแรกเพื่อความรวดเร็ว
 3. pytorch       - จะใช้สำหรับการ Train Model และ Predict สำหรับอ่านข้อความภาษาไทย
 4. fastapi       - ใช้เป็น Microservice เพื่อให้ง่ายต่อการใช้งาน และตรวจสอบผล
