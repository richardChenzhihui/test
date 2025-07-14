from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QListWidget, QFileDialog, QLabel, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
import os
from ai.rag_engine import RAGEngine
from utils.doc_parser import parse_file
from config import load_config, save_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("香港律师AI助手")
        self.resize(1000, 700)
        self.config = load_config()
        self.rag = RAGEngine(self.config["db_path"])
        self.init_ui()

    def init_ui(self):
        # 左侧：文档列表
        self.doc_list = QListWidget()
        self.doc_list.setFixedWidth(250)
        self.doc_list.itemClicked.connect(self.on_doc_selected)

        # 右侧：问答区
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("请输入您的法律问题...")
        self.ask_btn = QPushButton("AI问答")
        self.ask_btn.clicked.connect(self.on_ask)
        self.answer_output = QTextEdit()
        self.answer_output.setReadOnly(True)

        # 导入文档按钮
        self.import_btn = QPushButton("导入文档")
        self.import_btn.clicked.connect(self.on_import_doc)

        # API Key设置
        self.api_btn = QPushButton("设置OpenAI API Key")
        self.api_btn.clicked.connect(self.on_set_api_key)

        # 布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("已导入文档"))
        left_layout.addWidget(self.doc_list)
        left_layout.addWidget(self.import_btn)
        left_layout.addWidget(self.api_btn)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("法律问题"))
        right_layout.addWidget(self.question_input)
        right_layout.addWidget(self.ask_btn)
        right_layout.addWidget(QLabel("AI助手回答"))
        right_layout.addWidget(self.answer_output)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_doc_list()

    def load_doc_list(self):
        self.doc_list.clear()
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        for fname in os.listdir(docs_dir):
            self.doc_list.addItem(fname)

    def on_import_doc(self):
        fname, _ = QFileDialog.getOpenFileName(self, "选择文档", "", "PDF Files (*.pdf);;Word Files (*.docx)")
        if fname:
            basename = os.path.basename(fname)
            dest = os.path.join("docs", basename)
            os.makedirs("docs", exist_ok=True)
            if not os.path.exists(dest):
                with open(fname, "rb") as src, open(dest, "wb") as dst:
                    dst.write(src.read())
            # 解析并入库
            try:
                text_blocks = parse_file(dest)
                metadata = {"filename": basename}
                self.rag.add_document(basename, text_blocks, metadata)
                QMessageBox.information(self, "导入成功", f"{basename} 已导入知识库。")
                self.load_doc_list()
            except Exception as e:
                QMessageBox.critical(self, "导入失败", str(e))

    def on_doc_selected(self, item):
        fname = item.text()
        path = os.path.join("docs", fname)
        try:
            text_blocks = parse_file(path)
            self.answer_output.setPlainText("\n\n".join(text_blocks[:10]) + "\n...")
        except Exception as e:
            self.answer_output.setPlainText(f"无法读取文档：{e}")

    def on_ask(self):
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "提示", "请输入问题。")
            return
        self.answer_output.setPlainText("AI正在思考，请稍候...")
        try:
            answer, refs = self.rag.answer(question)
            self.answer_output.setPlainText(f"{answer}\n\n【引用片段】\n" + "\n---\n".join(refs))
        except Exception as e:
            self.answer_output.setPlainText(f"AI问答失败：{e}")

    def on_set_api_key(self):
        key, ok = QInputDialog.getText(self, "设置OpenAI API Key", "请输入API Key：", echo=QInputDialog.Password)
        if ok and key:
            self.config["openai_api_key"] = key
            save_config(self.config)
            QMessageBox.information(self, "设置成功", "API Key已保存。")