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
 2. pytesseract   - ในส่วนนี้เพื่อความรวดเร็วในการทำเทสผู้ทำข้อสอบขอใช้ pytesseract ในการอ่านเฉพาะข้อความที่เป็นภาษาอังกฤษ และตัวเลขเพื่อความรวดเร็ว
 3. pytorch       - จะใช้สำหรับการ Train Model และ Predict สำหรับอ่านข้อความภาษาไทย
 4. fastapi       - ใช้เป็น Microservice เพื่อให้ง่ายต่อการใช้งาน และตรวจสอบผล
 5. base64        - สำหรับแปลงค่า ระหว่าง รูปภาพ กับ base64encode

# ตัวอย่างผลลัพธ์บางส่วน
* ตัวอย่างการทดสอบผลลัพธ์ในการอ่านสลิปของ CASA LAPIN และบริษัทอีซีลี่จำกัด
![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/590b4269-0dd2-4724-aaac-f0d93fa28d96)


![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/7354c21e-aac8-4024-9b2e-ed5cf0d90b6a)


# อธิบายขั้นตอนการทำโมเดล 
* เนื่องจากเวลาที่มีค่อนข้างจำกัด ทำให้ไม่ได้ Comment ทุกรายละเอียดของฟังก์ชั่นการทำงานภายในแอพ จึงขออนุญาตอธิบายเป็น Concept ภาพใหญ่แทน และ Model 
 - 1 ทำการรับค่า base64 มาจาก USER และทำการแปลง เป็นรูปภาพ
 - 2 ทำการตรวจสอบ format เบื้องต้นว่าเป็น รูปแบบ EN หรือ TH เพื่อแยกเข้า process ที่เหมาะสมของ slip นั้นๆ (โดยในตัวอย่างจะใช้เป็นการใช้ tesseract อ่าน ข้อความ ว่ามีข้อความที่ตรงกับชื่อร้านที่จะอ่านไหม โดยจะเช็คจาก Lists ของรายชื่อร้านที่มี ถ้าไม่เจอแสดงว่าอาจจะเป็นรูปแบบภาษา TH จึงจะให้ไปทำการใช้ Model ที่ Train มาสำหรับการอ่านภาษาไทย)
 - 3 หลังจากรู้ว่า SLIP ที่ตรวจสอบไปเป็นของ ร้านค้าร้านไหน ในส่วนของภาษา EN จะส่งไปเข้าฟังก์ชั่นสำหรับ Extract ข้อมูล แต่ในส่วนของ TH จะนำไปผ่านกระบวนการ Image processing เพื่อแยกบรรทัดของข้อความ ปรับรายละเอียดของรูปภาพ ให้เหมาะสมกับการนำมาอ่านค่า เพื่อ return ชุด string ที่เป็นชุดข้อมูลของทุกบรรทัดมา จึงจะนำไปเข้าฟังก์ชั่นสำหรับ Extract ข้อมูล
