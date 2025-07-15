import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset, Dataset, IterableDataset
from peft import get_peft_model, LoraConfig, TaskType
import yaml

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_dataset(text_file, tokenizer, max_length, streaming=False):
    if streaming:
        ds = load_dataset('text', data_files=text_file, split='train', streaming=True)
    else:
        ds = load_dataset('text', data_files=text_file, split='train')
    def tokenize(example):
        return tokenizer(example["text"], truncation=True, max_length=max_length, padding="max_length")
    return ds.map(tokenize, batched=True, remove_columns=["text"])

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='../configs/train_config.yaml')
    parser.add_argument('--streaming', action='store_true', help='Use streaming mode for large datasets')
    args = parser.parse_args()
    config = load_config(args.config)

    tokenizer = AutoTokenizer.from_pretrained(config['model_name_or_path'], trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        config['model_name_or_path'],
        torch_dtype=torch.float16 if config.get('fp16', False) else (torch.bfloat16 if config.get('bf16', False) else torch.float32),
        trust_remote_code=True,
        device_map="auto"
    )

    # LoRA/PEFT 配置
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    model = get_peft_model(model, lora_config)

    dataset = get_dataset("../data/processed/all_text.txt", tokenizer, config['max_seq_length'], streaming=args.streaming)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=config['output_dir'],
        per_device_train_batch_size=config['per_device_train_batch_size'],
        gradient_accumulation_steps=config['gradient_accumulation_steps'],
        num_train_epochs=config['num_train_epochs'],
        learning_rate=config['learning_rate'],
        logging_steps=config['logging_steps'],
        save_steps=config['save_steps'],
        fp16=config.get('fp16', False),
        bf16=config.get('bf16', False),
        deepspeed=config.get('deepspeed', None),
        gradient_checkpointing=config.get('gradient_checkpointing', False),
        resume_from_checkpoint=config.get('resume_from_checkpoint', None),
        eval_steps=config.get('eval_steps', None),
        evaluation_strategy=config.get('evaluation_strategy', "no"),
        save_total_limit=config.get('save_total_limit', 3),
        logging_dir=config.get('logging_dir', None),
        report_to="tensorboard"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    trainer.train(resume_from_checkpoint=config.get('resume_from_checkpoint', None))

if __name__ == "__main__":
    main()