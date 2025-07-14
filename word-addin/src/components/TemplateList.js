import React from 'react';

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

function TemplateList({ templates }) {
  const handleInsert = async (id, name) => {
    const res = await fetch(`http://localhost:3001/api/templates/${id}`);
    const blob = await res.blob();
    const text = await blob.text();
    insertToWord(text);
  };

  return (
    <div>
      <h3>模板库</h3>
      <ul>
        {templates.map(t => (
          <li key={t.id} style={{ marginBottom: 8 }}>
            {t.originalname} ({t.mimetype})
            <button style={{ marginLeft: 8 }} onClick={() => handleInsert(t.id, t.originalname)}>插入</button>
            <a style={{ marginLeft: 8 }} href={`http://localhost:3001/api/templates/${t.id}`} download={t.originalname}>下载</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TemplateList;