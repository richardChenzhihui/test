import os
import glob
import pandas as pd
from docx import Document
import zipfile
from tqdm import tqdm
import multiprocessing as mp
import json
import pyarrow.parquet as pq

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

def extract_text_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            if isinstance(data, list):
                return "\n".join([json.dumps(item, ensure_ascii=False) for item in data])
            else:
                return json.dumps(data, ensure_ascii=False)
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
        return "\n".join(lines)
    except Exception as e:
        return ""

def extract_text_from_parquet(file_path):
    try:
        table = pq.read_table(file_path)
        df = table.to_pandas()
        return "\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
    except Exception as e:
        return ""

def extract_text_from_zip(file_path):
    texts = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith('.txt'):
                    with zip_ref.open(name) as f:
                        texts.append(f.read().decode('utf-8', errors='ignore'))
                elif name.endswith('.csv'):
                    with zip_ref.open(name) as f:
                        df = pd.read_csv(f)
                        texts.append("\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1)))
                elif name.endswith('.docx'):
                    with zip_ref.open(name) as f:
                        # docx不能直接用文件对象，需要先写到临时文件
                        tmp_path = name.replace('/', '_')
                        with open(tmp_path, 'wb') as tmpf:
                            tmpf.write(f.read())
                        texts.append(extract_text_from_docx(tmp_path))
                        os.remove(tmp_path)
                elif name.endswith('.json'):
                    with zip_ref.open(name) as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            texts.append("\n".join([json.dumps(item, ensure_ascii=False) for item in data]))
                        else:
                            texts.append(json.dumps(data, ensure_ascii=False))
                elif name.endswith('.jsonl'):
                    with zip_ref.open(name) as f:
                        lines = [line.decode('utf-8', errors='ignore').strip() for line in f if line.strip()]
                        texts.append("\n".join(lines))
                elif name.endswith('.parquet'):
                    with zip_ref.open(name) as f:
                        tmp_path = name.replace('/', '_')
                        with open(tmp_path, 'wb') as tmpf:
                            tmpf.write(f.read())
                        texts.append(extract_text_from_parquet(tmp_path))
                        os.remove(tmp_path)
    except Exception as e:
        return ""
    return "\n".join(texts)

def process_file(file_path):
    if file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.csv'):
        return extract_text_from_csv(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    elif file_path.endswith('.json'):
        return extract_text_from_json(file_path)
    elif file_path.endswith('.jsonl'):
        return extract_text_from_jsonl(file_path)
    elif file_path.endswith('.parquet'):
        return extract_text_from_parquet(file_path)
    elif file_path.endswith('.zip'):
        return extract_text_from_zip(file_path)
    else:
        return ""

def worker(file_path):
    text = process_file(file_path)
    return text.strip() if text.strip() else None

def main(raw_dir, out_file, num_workers=8):
    all_files = []
    for ext in ['**/*.txt', '**/*.csv', '**/*.docx', '**/*.json', '**/*.jsonl', '**/*.parquet', '**/*.zip']:
        all_files.extend(glob.glob(os.path.join(raw_dir, ext), recursive=True))
    with mp.Pool(num_workers) as pool, open(out_file, 'w', encoding='utf-8') as fout:
        for text in tqdm(pool.imap(worker, all_files), total=len(all_files)):
            if text:
                fout.write(text + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_dir', type=str, default='../data/raw')
    parser.add_argument('--out_file', type=str, default='../data/processed/all_text.txt')
    parser.add_argument('--num_workers', type=int, default=8)
    args = parser.parse_args()
    main(args.raw_dir, args.out_file, args.num_workers)