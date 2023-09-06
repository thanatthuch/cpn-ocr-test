# cpn-ocr-test
For interview test

### สามารถ Pull code ไปรันเพื่อตรวจสอบ หรือ จาก Docker Hub 

### กรณีใช้ Docker Hub
 - docker pull thanatthuch/cpn-ocr:latest
 - docker run --name imagename -p 8888:8888 thanatthuch/cpn-ocr:latest

 - ใช้ body ในการ requests ด้วย POST method ไปที่ /slip-detect
 - body จากไฟล์ api_test_en.json และ api_test_th.json
