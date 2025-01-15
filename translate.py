import asyncio
from PyPDF2 import PdfReader
from googletrans import Translator

def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

async def translate_chunk(translator, chunk, dest_language='zh-cn'):
    translated = await translator.translate(chunk, dest=dest_language)
    return translated.text

async def translate_text(text, dest_language='zh-cn'):
    translator = Translator()
    # 将文本分块
    chunk_size = 2000  # 每个块的字符数，可以根据需要调整
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    # 异步翻译每个块
    translated_chunks = await asyncio.gather(*[translate_chunk(translator, chunk, dest_language) for chunk in chunks])
    
    # 拼接翻译后的块
    translated_text = ''.join(translated_chunks)
    return translated_text

def save_translation(translated_text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)

async def main():
    pdf_path = './Build_a_Large_Language_Model_From_Scratch.pdf'
    output_path = 'translated_text.txt'

    try:
        pdf_text = read_pdf(pdf_path)
        translated_text = await translate_text(pdf_text)
        save_translation(translated_text, output_path)
        print(f"翻译完成，结果已保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
