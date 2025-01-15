from PyPDF2 import PdfReader
from googletrans import Translator

def read_pdf(file_path):
    # 使用 with 语句确保文件正确关闭
    with open(file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def translate_text(text, dest_language='zh-cn'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def save_translation(translated_text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)

if __name__ == "__main__":
    pdf_path = './Build_a_Large_Language_Model_From_Scratch.pdf'
    output_path = 'translated_text.txt'

    try:
        pdf_text = read_pdf(pdf_path)
        translated_text = translate_text(pdf_text)
        save_translation(translated_text, output_path)
        print(f"翻译完成，结果已保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")
