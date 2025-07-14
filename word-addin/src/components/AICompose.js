import React, { useState } from 'react';

function insertToWord(text) {
  if (window.Office && window.Word) {
    window.Word.run(async context => {
      const range = context.document.getSelection();
      range.insertText(text, 'Replace');
      await context.sync();
    });
  } else {
    alert('请在Word中使用此功能');
  }
}

function AICompose() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAI = async e => {
    e.preventDefault();
    setLoading(true);
    setResult('');
    const res = await fetch('http://localhost:3001/api/ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: '你是专业的香港金融法律文书助手。' },
          { role: 'user', content: prompt },
        ],
        temperature: 0.2,
      }),
    });
    const data = await res.json();
    const text = data.choices?.[0]?.message?.content || '无结果';
    setResult(text);
    setLoading(false);
  };

  return (
    <div style={{ marginTop: 24 }}>
      <h3>AI起草/润色/审查</h3>
      <form onSubmit={handleAI}>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          rows={3}
          style={{ width: '100%' }}
          placeholder="请输入你的需求，如：请起草一份贷款合同模板..."
        />
        <button type="submit" disabled={loading || !prompt}>AI生成</button>
      </form>
      {loading && <div>AI处理中...</div>}
      {result && (
        <div style={{ marginTop: 8 }}>
          <b>AI结果：</b>
          <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: 8, marginTop: 4 }}>{result}</div>
          <button style={{ marginTop: 8 }} onClick={() => insertToWord(result)}>插入到Word</button>
        </div>
      )}
    </div>
  );
}

export default AICompose;