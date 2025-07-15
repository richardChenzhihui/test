# LLM 全量微调工程（PEFT + DeepSpeed + 超大数据）

## 目录结构

- `data/raw/`：原始法律数据集（支持 txt/csv/docx/zip）
- `data/processed/`：预处理后纯文本
- `scripts/preprocess.py`：数据预处理脚本
- `scripts/train.py`：微调主脚本
- `configs/train_config.yaml`：训练参数配置
- `configs/ds_config.json`：DeepSpeed 配置
- `requirements.txt`：依赖包
- `output/`：训练输出

---

## 依赖安装

```bash
pip install -r requirements.txt
```

---

## 数据预处理

支持 txt、csv、docx、zip（压缩包内 txt），自动并行处理，异常文件自动跳过。

```bash
python scripts/preprocess.py --raw_dir data/raw --out_file data/processed/all_text.txt --num_workers 16
```

---

## 训练参数说明（configs/train_config.yaml）

| 参数名                      | 说明                                                         |
|-----------------------------|--------------------------------------------------------------|
| model_name_or_path          | 预训练模型路径或 HuggingFace 名称（如本地 38B 模型）         |
| output_dir                  | 训练输出目录                                                 |
| per_device_train_batch_size | 单卡 batch size（建议根据显存调整）                           |
| gradient_accumulation_steps | 梯度累积步数（总 batch size = batch_size × 卡数 × 累积步数）  |
| num_train_epochs            | 训练轮数                                                     |
| learning_rate               | 学习率                                                       |
| logging_steps               | 日志打印步数                                                 |
| save_steps                  | 模型保存步数                                                 |
| max_seq_length              | 最大序列长度（建议 2048 及以上）                             |
| deepspeed                   | DeepSpeed 配置文件路径                                       |
| fp16                        | 是否使用混合精度 fp16                                        |
| bf16                        | 是否使用 bf16（部分显卡支持）                                |
| gradient_checkpointing      | 是否开启梯度检查点，节省显存                                 |
| resume_from_checkpoint      | 断点续训路径（可选）                                         |
| eval_steps                  | 验证步数（可选）                                             |
| evaluation_strategy         | 验证策略（如 "steps"）                                       |
| save_total_limit            | 最多保存模型数                                               |
| logging_dir                 | 日志目录                                                     |

---

## 训练启动

**推荐使用 DeepSpeed 启动，自动分布式，适配 4×H200：**

```bash
deepspeed scripts/train.py --config configs/train_config.yaml
```

如需流式加载超大数据集（1TB+），可加 `--streaming` 参数：

```bash
deepspeed scripts/train.py --config configs/train_config.yaml --streaming
```

---

## 训练策略建议

1. **分布式训练**  
   - 推荐 DeepSpeed ZeRO Stage 3 或 FSDP，极大节省显存，适合 38B 级别大模型。
   - 4×H200 建议 batch size 适当调小，利用梯度累积。

2. **数据处理**  
   - 1TB 级别建议用 streaming 模式，避免内存溢出。
   - 预处理时可分块并行，提升效率。

3. **PEFT 微调**  
   - LoRA/QLoRA 可大幅降低显存和存储需求，适合大模型。
   - 若需全量微调（非 LoRA），可去掉 `get_peft_model` 相关代码。

4. **混合精度与梯度检查点**  
   - fp16/bf16 可大幅提升训练速度和显存利用率。
   - 梯度检查点进一步节省显存，适合超大模型。

5. **断点续训与监控**  
   - 建议定期保存模型，支持断点续训。
   - 日志建议用 TensorBoard 监控 loss、lr 等指标。

6. **评估与早停**  
   - 可设置 eval_steps，定期在验证集评估，防止过拟合。

---

## 各模块说明

### preprocess.py

- 支持 txt/csv/docx/zip 格式，自动并行处理，异常文件自动跳过。
- 输出纯文本，每行为一条样本，适合大规模训练。

### train.py

- 支持 HuggingFace Transformers + PEFT + DeepSpeed。
- 支持流式加载超大数据集。
- 支持 LoRA/QLoRA 微调，极大节省资源。
- 支持断点续训、混合精度、梯度检查点、分布式训练。

---

## 结语

本工程为大模型（如 38B）在超大法律语料上的全量微调提供了完整、可扩展、易维护的解决方案。  
如需进一步定制（如多机多卡、评测脚本、推理部署等），欢迎补充需求！
