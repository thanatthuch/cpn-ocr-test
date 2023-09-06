from model import my_utils
import cv2
import pytesseract



with open("./model/company_lists.txt") as f:
    company = f.read()
    company_list = company.splitlines()

def detect(image64: str) -> dict[str]:
    img_cv = my_utils.base64_to_image(image64)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    messages = pytesseract.image_to_string(img_rgb)

    LANG_CHECK :bool = False
    for message in messages.splitlines():
        if len(message) != 0:
            # MAP COMPANY IN LISTS OF CPN
            if message in company_list:
                SHOP_NAME = message
                LANG_CHECK= True
                break

    if LANG_CHECK: 
        # ENGLISH PROCESS
        result = my_utils.get_information_en(messages=messages, SHOP_NAME=SHOP_NAME)
    else:
        result_message = my_utils.thai_reading(img_rgb)

        LANG_TH_CHECK : bool = False
        for text in result_message.splitlines():
            if text in company_list:
                SHOP_NAME = text 
                LANG_TH_CHECK = True
                break
        if LANG_TH_CHECK: 
            ## GET INFORMATION 
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            messages = pytesseract.image_to_string(img_rgb)
            result = my_utils.get_information_th(messages=messages, SHOP_NAME=SHOP_NAME)
    return result