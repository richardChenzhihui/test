import os
import glob
import pandas as pd
from docx import Document
import zipfile
from tqdm import tqdm
import multiprocessing as mp
import json
import pyarrow.parquet as pq

"""
数据预处理脚本
- 第一阶段：处理B（法律文本）和C（课堂笔记），合并为plain_text.txt。
- 第二阶段：处理A（知识蒸馏/指令微调），读取json格式（含question/answer），合并为instruction.jsonl。
- 支持personal injection，将personal问答插入A数据并可多次复制。
"""

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return ""

def extract_text_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return "\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
    except Exception as e:
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return ""

def extract_text_from_jsonl(file_path):
    try:
        lines = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        return lines
    except Exception as e:
        return []

def extract_text_from_parquet(file_path):
    try:
        table = pq.read_table(file_path)
        df = table.to_pandas()
        return "\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
    except Exception as e:
        return ""

def extract_text_from_zip(file_path, mode='plain'):
    texts = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if mode == 'plain':
                    if name.endswith('.txt'):
                        with zip_ref.open(name) as f:
                            texts.append(f.read().decode('utf-8', errors='ignore'))
                    elif name.endswith('.csv'):
                        with zip_ref.open(name) as f:
                            df = pd.read_csv(f)
                            texts.append("\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1)))
                    elif name.endswith('.docx'):
                        with zip_ref.open(name) as f:
                            tmp_path = name.replace('/', '_')
                            with open(tmp_path, 'wb') as tmpf:
                                tmpf.write(f.read())
                            texts.append(extract_text_from_docx(tmp_path))
                            os.remove(tmp_path)
                    elif name.endswith('.parquet'):
                        with zip_ref.open(name) as f:
                            tmp_path = name.replace('/', '_')
                            with open(tmp_path, 'wb') as tmpf:
                                tmpf.write(f.read())
                            texts.append(extract_text_from_parquet(tmp_path))
                            os.remove(tmp_path)
                elif mode == 'instruction':
                    if name.endswith('.json'):
                        with zip_ref.open(name) as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                for item in data:
                                    if 'question' in item and 'answer' in item:
                                        texts.append(json.dumps({'question': item['question'], 'answer': item['answer']}, ensure_ascii=False))
                            elif 'question' in data and 'answer' in data:
                                texts.append(json.dumps({'question': data['question'], 'answer': data['answer']}, ensure_ascii=False))
                    elif name.endswith('.jsonl'):
                        with zip_ref.open(name) as f:
                            for line in f:
                                line = line.decode('utf-8', errors='ignore').strip()
                                if line:
                                    obj = json.loads(line)
                                    if 'question' in obj and 'answer' in obj:
                                        texts.append(json.dumps({'question': obj['question'], 'answer': obj['answer']}, ensure_ascii=False))
    except Exception as e:
        return [] if mode == 'instruction' else ""
    return texts if mode == 'instruction' else "\n".join(texts)

def process_plain_file(file_path):
    if file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.csv'):
        return extract_text_from_csv(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    elif file_path.endswith('.parquet'):
        return extract_text_from_parquet(file_path)
    elif file_path.endswith('.zip'):
        return extract_text_from_zip(file_path, mode='plain')
    else:
        return ""

def process_instruction_file(file_path):
    results = []
    if file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if 'question' in item and 'answer' in item:
                            results.append(json.dumps({'question': item['question'], 'answer': item['answer']}, ensure_ascii=False))
                elif 'question' in data and 'answer' in data:
                    results.append(json.dumps({'question': data['question'], 'answer': data['answer']}, ensure_ascii=False))
        except Exception as e:
            pass
    elif file_path.endswith('.jsonl'):
        results.extend(extract_text_from_jsonl(file_path))
    elif file_path.endswith('.zip'):
        results.extend(extract_text_from_zip(file_path, mode='instruction'))
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="法律大模型数据预处理脚本")
    parser.add_argument('--plain_dirs', nargs='+', help='B+C数据目录（法律文本/课堂笔记）')
    parser.add_argument('--plain_out', type=str, default='../data/processed/plain_text.txt', help='输出纯文本文件')
    parser.add_argument('--instruction_dirs', nargs='+', help='A数据目录（知识蒸馏/指令微调）')
    parser.add_argument('--instruction_out', type=str, default='../data/processed/instruction.jsonl', help='输出指令微调jsonl文件')
    parser.add_argument('--personal_file', type=str, default=None, help='personal问答json文件')
    parser.add_argument('--personal_repeat', type=int, default=5, help='personal问答重复次数')
    parser.add_argument('--num_workers', type=int, default=8)
    args = parser.parse_args()

    # 处理plain文本（B+C）
    if args.plain_dirs:
        all_files = []
        for d in args.plain_dirs:
            for ext in ['**/*.txt', '**/*.csv', '**/*.docx', '**/*.parquet', '**/*.zip']:
                all_files.extend(glob.glob(os.path.join(d, ext), recursive=True))
        with mp.Pool(args.num_workers) as pool, open(args.plain_out, 'w', encoding='utf-8') as fout:
            for text in tqdm(pool.imap(process_plain_file, all_files), total=len(all_files), desc='B+C'):
                if text and text.strip():
                    fout.write(text.strip() + "\n")

    # 处理指令微调数据（A）
    if args.instruction_dirs:
        all_files = []
        for d in args.instruction_dirs:
            for ext in ['**/*.json', '**/*.jsonl', '**/*.zip']:
                all_files.extend(glob.glob(os.path.join(d, ext), recursive=True))
        with open(args.instruction_out, 'w', encoding='utf-8') as fout:
            for file_path in tqdm(all_files, desc='A'):
                results = process_instruction_file(file_path)
                for line in results:
                    fout.write(line.strip() + "\n")
        # personal injection
        if args.personal_file:
            with open(args.personal_file, 'r', encoding='utf-8') as pf:
                personal_data = json.load(pf)
                for _ in range(args.personal_repeat):
                    for item in personal_data:
                        if 'question' in item and 'answer' in item:
                            with open(args.instruction_out, 'a', encoding='utf-8') as fout:
                                fout.write(json.dumps({'question': item['question'], 'answer': item['answer']}, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()