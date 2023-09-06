# cpn-ocr-test
For interview test

### (เนื่องจากเวลาที่จำกัด ผู้ทำเทสจะขอทำรูปแบบการอ่าน SLIP แบบ static เนื่องจากจำนวนข้อมูลที่มี ซึ่งอาจจะรองรับการอ่านเฉพาะสำหรับ SLIP ของ 2 ร้านค้าที่ให้มา ซึ่งในส่วน Model ที่ทำจะเป็น Model เบื้องต้นในการอ่าน ที่เหมาะสมเฉพาะ 2 ตัวอย่าง SLIP นี้)


### สามารถ Pull code ไปรันเพื่อตรวจสอบ หรือ จาก Docker Hub 

### กรณีใช้ Docker Hub
 - docker pull thanatthuch/cpn-ocr:latest
 - docker run --name imagename -p 8888:8888 thanatthuch/cpn-ocr:latest

 - ส่ง requests ด้วย POST method ไปที่ /slip-detect ด้วย JsonBody
 - body จากไฟล์ api_test_en.json และ api_test_th.json

### กรณีจะ Clone Code เพื่อตรวจสอบ
 - git clone https://github.com/thanatthuch/cpn-ocr-test.git
 - cd cpn-ocr-test
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

![en](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/440eaefa-5b45-455c-a891-96e625e548ca)               ![th](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/97d1a2f5-1875-45f6-81b7-8755e2569275)


![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/590b4269-0dd2-4724-aaac-f0d93fa28d96)


![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/7354c21e-aac8-4024-9b2e-ed5cf0d90b6a)


# อธิบายขั้นตอนการทำงานโมเดล 
* เนื่องจากเวลาที่มีค่อนข้างจำกัด ทำให้ไม่ได้ Comment ทุกรายละเอียดของฟังก์ชั่นการทำงานภายในแอพ จึงขออนุญาตอธิบายเป็น Concept ภาพใหญ่แทน
 - 1 ทำการรับค่า base64 มาจาก USER และทำการแปลง เป็นรูปภาพ
 - 2 ทำการตรวจสอบ format เบื้องต้นว่าเป็น รูปแบบ EN หรือ TH เพื่อแยกเข้า process ที่เหมาะสมของ slip นั้นๆ (โดยในตัวอย่างจะใช้เป็นการใช้ tesseract อ่าน ข้อความ ว่ามีข้อความที่ตรงกับชื่อร้านที่จะอ่านไหม โดยจะเช็คจาก Lists ของรายชื่อร้านที่มี ถ้าไม่เจอแสดงว่าอาจจะเป็นรูปแบบภาษา TH จึงจะให้ไปทำการใช้ Model ที่ Train มาสำหรับการอ่านภาษาไทย)
 - 3 หลังจากรู้ว่า SLIP ที่ตรวจสอบไปเป็นของ ร้านค้าร้านไหน ในส่วนของภาษา EN จะส่งไปเข้าฟังก์ชั่นสำหรับ Extract ข้อมูล แต่ในส่วนของ TH จะนำไปผ่านกระบวนการ Image processing เพื่อแยกบรรทัดของข้อความ ปรับรายละเอียดของรูปภาพ ให้เหมาะสมกับการนำมาอ่านค่า เพื่อ return ชุด string ที่เป็นชุดข้อมูลของทุกบรรทัดมา จึงจะนำไปเข้าฟังก์ชั่นสำหรับ Extract ข้อมูล
 - ส่งกลับข้อมูลไปหาผู้ใช้งาน

# อธิบายขั้นตอนการเตรียมข้อมูล(คร่าวๆ)
* ในส่วนนี้เป็นส่วนในการอธิบายการนำข้อมูลที่ได้ มาทำการ Train ข้อความของตัวอักษร ภาษาไทย (เนื่องจากข้อมูลมีจำนวนไม่เยอะมาก ผสมกับเวลาที่มีจำกัด จึงขอนำข้อมูลตัวอักษรแค่บางส่วนมา Train เพื่อเป็น Prototype และเพื่อความรวดเร็วในการทำเทส)
  1. ทำ Image processing เพื่อ Extract รูปภาพของตัวอักษร
     ![Screenshot 2566-09-05 at 17 48 52](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/9c92a98b-378c-4012-8563-2d147953353f)

  2. นำภาพตัวอักษร มาจัดให้อยู่ถูกตามชื่อ Folder เพื่อเตรียมไว้สำหรับจัดทำ Dataloader 

![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/b3828883-b097-4cd0-9b49-8de70ca50499)

  3. ทำการนำ Dataloader ที่เตรียมไว้ ไปทำการ Train ด้วย CNN Model
     * รูปภาพตัวอย่าง และผลลัพธ์ในการเทรนด์
![image](https://github.com/thanatthuch/cpn-ocr-test/assets/52025403/b6fb10d6-c5ab-42fa-b256-c3a50714a3c3)




# Thank you _/\_
