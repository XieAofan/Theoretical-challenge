import numpy as np
import cv2, time
from paddleocr import PaddleOCR


class Img_Process:
    def __init__(self):
        self.img = None
        # 加载模型
        self.ocr = PaddleOCR(use_angle_cls=False, ocr_version="PP-OCRv4", lang='ch') # need to run only once to download and load model into memory
        self.result = None
        self.time_use = None 
        self.cut_key = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    def remove_watermark(self, img, thresh=600):
        if img is None:
            print("读取图像文件失败。")
            return

        # 计算每个像素的 RGB 通道和
        rgb_sum_per_pixel = img.sum(axis=2)

        # 将大于阈值的像素点调整为白色
        img[rgb_sum_per_pixel > thresh] = [255, 255, 255]

        return img

    def set_img(self, img):
        self.result = None
        self.time_use = None
        self.img = self.remove_watermark(img)

    # 处理图像
    def process_img(self):
        t1 = time.time()
        self.result = self.ocr.ocr(self.img, cls=False)  # OCR and post-processing
        t2 = time.time()
        self.time_use = t2 - t1

    # 处理OCR结果
    def get_result(self):
        line_list = []
        words = ''
        for line in self.result[0]:
            line = line[1][0]
            if line[0] in self.cut_key:
                line_list.append(words)
                words = line
            else:
                words += line
        line_list.append(words)
        self.result = line_list
        return self.result



if __name__ == '__main__':
    path = 'raw/9c4b3914a5ed499e820b3189be30a480.jpg'
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    ImP = Img_Process()
    ImP.set_img(img)
    ImP.process_img()
    result = ImP.get_result()
    for l in result:
        print(l)
    print(ImP.time_use)