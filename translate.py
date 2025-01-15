import PyPDF2
from googletrans import Translator

def read_pdf(file_path):
    pdf = open(file_path, 'rb')
    reader = PyPDF2.PdfFileReader(pdf)
    text = ""
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    pdf.close()
    return text

def translate_text(text, dest_language='zh-cn'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def save_translation(translated_text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)

if __name__ == "__main__":
    pdf_path = 'Build_a_Large_Language_Model_From_Scratch.pdf'
    output_path = 'translated_text.txt'
    
    pdf_text = read_pdf(pdf_path)
    translated_text = translate_text(pdf_text)
    save_translation(translated_text, output_path)
    
    print(f"翻译完成，结果已保存到 {output_path}")
