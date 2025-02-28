from typing import Optional
from translator.pdf.pdf_parser import PDFParser
from translator.translation_chain import TranslationChain
from translator.writer import Writer
from utils import LOG


# 定义一个PDFTranslator类
class PDFTranslator:
    # 定义初始化函数，接收一个model_name参数
    def __init__(self, model_name: str):
        # 创建一个TranslationChain对象，用于执行翻译任务
        self.translate_chain = TranslationChain(model_name)
        # 创建一个PDFParser对象，用于解析PDF文件
        self.pdf_parser = PDFParser()
        # 创建一个Writer对象，用于写入文件
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = 'Chinese',
                      output_file_path: str = None, pages: Optional[int] = None):
        # 使用PDFParser对象解析指定的PDF文件，并将结果赋值给self.book
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        # 遍历self.book的每一页
        for page_idx, page in enumerate(self.book.pages):
            # 遍历每一页的每个内容
            for content_idx, content in enumerate(page.contents):
                # 使用TranslationChain对象执行翻译，并将结果赋值给translation和status
                """
                核心的翻译代码
                """
                translation, status = self.translate_chain.run(content, target_language)
                # 打印翻译结果
                LOG.info(translation)

                # 更新self.document.pages中的内容
                content.apply_translated_paragraphs(translation)
                """
                用book对象存储翻译的结果
                """
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        # 使用Writer对象保存翻译后的书籍，并返回保存的路径
        return self.writer.save_translated_book(self.book, output_file_path, file_format)

        
