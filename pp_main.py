import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from bs4 import BeautifulSoup
import re#正则表达式库
# 中文测试图





table_engine = PPStructure(recovery=True,return_ocr_result_in_table=True)
# 英文测试图
# table_engine = PPStructure(recovery=True, lang='en')

save_folder = './output'
img_path = './docs/table/test_hand.jpg'

def filter_uppercase(s):#字符串转换成列表
    return ''.join(ch for ch in s if ch.isupper())

def extract_capitals(s):#匹配大写字母
    return re.findall('[A-Z]', s)

# print(answer_total)  # 输出: ['H', 'W', 'D']
#正确答案
answer_danzhizhi_list = ['B', 'D', 'B', 'D', 'C', 'A', 'C', 'C', 'A', 'B', 'C', 'A', 'D', 'A', 'D']
answer_duoxuezhi_list = ['A', 'C', 'C', 'A', 'D', 'A', 'B', 'C', 'B', 'B', 'A', 'C', 'B', 'C', 'B']
anser_nianyezhi_list = ['B', 'D', 'C', 'A', 'D', 'B', 'C', 'C', 'A', 'C', 'D', 'B', 'D', 'A', 'D']
anser_yiyuzhi_list = ['C', 'A', 'B', 'D', 'C', 'D', 'D', 'C', 'B', 'C', 'D', 'C', 'B', 'B', 'C']

answer_list = [answer_danzhizhi_list,answer_duoxuezhi_list,anser_nianyezhi_list,anser_yiyuzhi_list]

def split_list(lst):#列表4等分
    k = len(lst) // 4  # 计算每部分的长度
    r = len(lst) % 4  # 计算余数
    return [
        lst[i * k:i * k + k + (1 if i < r else 0)] for i in range(4)
    ]
if __name__ == '__main__':
    #图像处理过程
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])
    h, w, _ = img.shape
    res = sorted_layout_boxes(result, w)
    convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0], )
    # 关键信息抽取-->关心的字母答案
    res_list = [item['res'] for item in result]
    html_list = res_list[1].get('html', None)#存储为html文本字符串
    soup = BeautifulSoup(html_list, 'html.parser')
    stories = []
    body_text = soup.body.get_text()
    # 使用换行符分割文本，并去除空字符串
    body_paragraphs = [p.strip() for p in body_text.split('\n') if p.strip()]
    output_string = filter_uppercase(body_paragraphs[0])
    answer_total = extract_capitals(output_string)
    #answer_total为最终识别到的答案列表
    #答案分配+统计分数
    stu_answer = split_list(answer_total)#将识别到的答案列表分为4组
    score = [0,0,0,0]
    for i in range(4):
        for j in range(15):
            if stu_answer[i][j] == answer_list[i][j]:
                score[i] += 1
    score_total = sum(score)#得到学生此次测评总分








    # stu_answer = [[],[],[],[]]
    # stu_answer[0] = answer_total[0:14]
    # stu_answer[1] = answer_total[15:29]
    # stu_answer[2] = answer_total[30:44]
    # stu_answer[3] = answer_total[45:60]