import fitz  # PyMuPDF
from googletrans import Translator
import io
from PIL import Image
import os
import asyncio
import re

class PDFTranslator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.images = []

    def extract_text_and_images(self):
        pdf_document = fitz.open(self.file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # 提取文本
            page_text = page.get_text()
            # 使用正则表达式将多个连续的非空行合并成一行
            page_text = re.sub(r'([^\n\s].*?)\n(?=[^\n\s])', r'\1 ',page_text)
            self.text += page_text

            # 提取图像
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                self.images.append((image, f"image_page{page_num+1}_{img_index+1}.{image_ext}"))

    async def translate_chunk(self, translator, chunk, dest_language='zh-cn'):
        translated = await translator.translate(chunk, dest=dest_language)
        return translated.text

    async def translate_text(self, dest_language='zh-cn'):
        translator = Translator()
        chunk_size = 10000  # 每个块的字符数，可以根据需要调整
        chunks = [self.text[i:i + chunk_size] for i in range(0, len(self.text), chunk_size)]

        # 异步翻译每个块
        translated_chunks = await asyncio.gather(*[self.translate_chunk(translator, chunk, dest_language) for chunk in chunks])

        # 拼接翻译后的块
        self.translated_text = ''.join(translated_chunks)

    def save_translation(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(self.translated_text)

    def save_images(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for image, image_name in self.images:
            image.save(os.path.join(output_dir, image_name))

async def main():
    pdf_path = './Build_a_Large_Language_Model_From_Scratch.pdf'
    output_text_path = 'translated_text.txt'
    output_image_dir = 'extracted_images'

    pdf_translator = PDFTranslator(pdf_path)

    try:
        pdf_translator.extract_text_and_images()
        await pdf_translator.translate_text()
        pdf_translator.save_translation(output_text_path)
        pdf_translator.save_images(output_image_dir)
        print(f"翻译完成，结果已保存到 {output_text_path}")
        print(f"图像提取完成，图像已保存到 {output_image_dir}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
