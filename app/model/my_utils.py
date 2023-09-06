import re

from datetime import datetime

import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
import base64

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 6 * 6, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 21) # 10 classes as an example

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 6 * 6)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    

def get_device():
    # หากมีการกำหนดให้ใช้ MPS (ในกรณีของคุณที่ต้องการ)
    if torch._C._get_default_device() == "mps":
        return "mps"
    
    # ตรวจสอบว่า CUDA สามารถใช้งานได้หรือไม่
    elif torch.cuda.is_available():
        return "cuda"
    
    # หากไม่มีการกำหนดอื่น ๆ จะถือว่าเป็น CPU
    else:
        return "cpu"

device = "cpu"

model = Net()
model.load_state_dict(torch.load('./model/model_weights.pth', map_location='cpu'))
model.eval()


def predict(image):
    classes = ['VAT', 'กัด', 'ข', 'จำ', 'ซิ', 'ต', 'ถ', 'ท', 'ที่', 'น', 'บ', 'ป', 'ม', 'ร', 'ริ', 'ลี่', 'วัน', 'ษัท', 'อ', 'อี', 'เข']
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ])

    image = transform(image)
    image = image.unsqueeze(0) # เพิ่ม batch dimension

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return classes[predicted]

def extract_numbers(input_str):
    numbers = re.findall(r'\d+', input_str)
    result = ''.join(numbers)
    return result

def convert_string_to_datetime(input_str) -> str:
    input_format = "%d%B%Y%H:%M:%S"
    output_format = "%Y-%m-%d %H:%M:%S"

    dt_obj = datetime.strptime(input_str, input_format)
    formatted_date = dt_obj.strftime(output_format)
    
    return formatted_date

def resize_to_square(arr):
    old_h, old_w = arr.shape
    new_size = max(old_h, old_w)
    new_arr = np.zeros((new_size, new_size), dtype=arr.dtype)
    h_start = (new_size - old_h) // 2
    w_start = (new_size - old_w) // 2
    new_arr[h_start:h_start+old_h, w_start:w_start+old_w] = arr
    return new_arr


def get_information_en(messages : list[str], SHOP_NAME : str) -> dict[str] :
    """
    Parameters
        - messages   : string
        - SHOP_NAME  : string
    Returns
        - dict
    """
    for message in messages.splitlines():
        if len(message) != 0:
            # GET TAX_ID
            message = message.replace(" ", "")
            if ("TAXID" in message.upper()):
                TAX_ID = extract_numbers(message)

            # GET DATE ต้องมีการดักเพิ่มเติม
            if ("DATE:" in message.upper()):
                
                date = message.upper()
                date = date.replace("DATE:", "").replace("DATE", "")
                DATE = convert_string_to_datetime(date)
        
            # # ส่่วนนี้จริงๆ แล้วจะขึ้นกับ pattern ของแต่ละ shop name
            if ("NO" in message.upper()):
                # print(message.split(":")[1])
                if len(message.split(":")[1]) > 10:
                    RECEIPT_NO = message.split(":")[1]

            if ("TOTAL" in message.upper()):
                try:
                    GRAND_TOTAL = format(float(message.upper().replace("TOTAL","")), ".2f")
                except:
                    pass

    result_data = {
        "shop name": SHOP_NAME,
        "tax id": TAX_ID,
        "date": DATE,
        "receip no": RECEIPT_NO,
        "grand total": GRAND_TOTAL,
        "lang_format" : "EN"
    }
    return result_data



def split_lines_from_image(image):
    image = image[:,:,0]
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((2, 500), np.uint8)
    dilated_image = cv2.dilate(binary_image, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    newcrop = image.copy()
    line_images = []
    sum_h = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        sum_h.append(h)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > sum(sum_h)/len(sum_h):
            try:
                line_image = image[y-3:y+h+3, x:x+w]
            except :
                line_image = image[y:y+h, x:x+w]

            line_images.append(line_image)
            # newcrop = cv2.rectangle(newcrop, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return line_images

def thai_reading(image : np.ndarray) -> str:
    textlines = ""
    # image = image[:,:,0]
    line_images = split_lines_from_image(image)
    
    for i in range(len(line_images)):
        
        test  = line_images[i]
        rotated = cv2.rotate(test, cv2.ROTATE_90_COUNTERCLOCKWISE)

        _, binary_image = cv2.threshold(rotated, 150, 255, cv2.THRESH_BINARY_INV)
        _, binary_image2 = cv2.threshold(rotated, 170, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((5, 100), np.uint8)
        dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        line_text = ""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            rec = binary_image2[y:y+h, x:x+w]
            new_rec = resize_to_square(rec)
            resized_array = cv2.resize(new_rec, (80,80))
            resized_array = cv2.rotate(resized_array, cv2.ROTATE_90_CLOCKWISE)

            image_rgb = cv2.cvtColor(resized_array, cv2.COLOR_GRAY2RGB)
            image_pil = Image.fromarray(image_rgb)
        
            line_text += predict(image_pil)
            # # print(line_text)
            # cv2.imshow("test", resized_array)
            # cv2.waitKey(0)
        textlines += line_text +"\n"

    return textlines



def transform_datetime(s):
    # ใช้ regular expression สำหรับการค้นหาวันที่และเวลาจาก string
    date_match = re.search(r"Date: (\d{2})/(\d{2})/(\d{2})", s)
    time_match = re.search(r"Time: (\d{2}:\d{2})", s)
    
    # ตรวจสอบว่าเราพบข้อมูลในรูปแบบที่ต้องการหรือไม่
    if date_match and time_match:
        day, month, year_suffix = date_match.groups()
        time = time_match.group(1)
        
        # สร้าง string ในรูปแบบที่ต้องการ
        return f"20{year_suffix}-{month}-{day} {time}:00"
    else:
        raise ValueError("Invalid format!")


def process_string_checkTotal(s):
    # ลบตัวอักษร T, t, O, o, A, a, L, l ออกจาก string
    for char in "TtOoAaLl,":
        s = s.replace(char, '')
    
    # ตรวจสอบว่า string หลังจากที่ถูกประมวลผลแล้วสามารถแปลงเป็น float ได้หรือไม่
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"'{s}' cannot be converted to float.")
    
def get_information_th(messages : str, SHOP_NAME : str) -> dict[str]:
    """
    Parameters
        - messages   : string
        - SHOP_NAME  : string
    Returns
        - dict
    """
    TAX_ID     : str = ""
    DATE       : str = ""
    RECEIPT_NO : str = ""
    GRAND_TOTAL: str = ""
    for message in messages.splitlines():
        if ("NO" in message.upper()):
            try:  
                text_clean = message.replace(" ","").split(":")[1]
                if len(text_clean) > 10:
                    RECEIPT_NO = text_clean
            except :
                pass

    # FIND TAX ID

        if ("TAX" in message.upper()):
            try:
                check_tax = message.upper().replace(" ","").split(":")[1]
                if len(check_tax) > 10:
                    TAX_ID = check_tax
            except:
                pass
        if ("DATE" in message.upper()):
            DATE = transform_datetime(message)

    # FIND GRAND_TOTAL
        if ("TOTAL" in message.upper()):
            try: 
                GRAND_TOTAL = format(process_string_checkTotal(message), ".2f")
                # print(GRAND_TOTAL)
            except :
                pass
    result_data = {
        "shop name": SHOP_NAME,
        "tax id": TAX_ID,
        "date": DATE,
        "receip no": RECEIPT_NO,
        "grand total": GRAND_TOTAL,
        "lang_format" : "TH"
    }
    return result_data


def base64_to_image(image64: str) -> np.ndarray:
    binary_data = base64.b64decode(image64)
    # Convert binary to numpy array
    image_nparr = np.frombuffer(binary_data, np.uint8)

    # Decode numpy array to image
    image = cv2.imdecode(image_nparr, cv2.IMREAD_COLOR)
    return image