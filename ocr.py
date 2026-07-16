import re
import io
import os
from PIL import Image
import pytesseract

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_period_from_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        top_area = image.crop((0, 0, width, int(height * 0.15)))
        
        images_to_try = [
            top_area,
            top_area.convert('L'),
            top_area.convert('L').point(lambda x: 0 if x < 140 else 255, '1')
        ]
        
        large = top_area.resize((top_area.width * 2, top_area.height * 2), Image.Resampling.LANCZOS)
        images_to_try.append(large.convert('L').point(lambda x: 0 if x < 140 else 255, '1'))
        
        for img in images_to_try:
            for config in ['--psm 6 -c tessedit_char_whitelist=0123456789', '--psm 7 -c tessedit_char_whitelist=0123456789']:
                text = pytesseract.image_to_string(img, lang='eng', config=config)
                digits_only = re.sub(r'[^0-9]', '', text)
                
                if len(digits_only) >= 14:
                    for length in [17, 16, 15, 14]:
                        if len(digits_only) >= length:
                            candidate = digits_only[:length]
                            if len(candidate) >= 14:
                                return candidate
        return None
    except Exception as e:
        print(f"OCR Error: {e}")
        return None