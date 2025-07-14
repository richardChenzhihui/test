import React, { useRef } from 'react';

function UploadTemplate({ onUpload }) {
  const fileRef = useRef();

  const handleUpload = async e => {
    e.preventDefault();
    const file = fileRef.current.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    await fetch('http://localhost:3001/api/templates', {
      method: 'POST',
      body: formData,
    });
    fileRef.current.value = '';
    onUpload && onUpload();
  };

  return (
    <form onSubmit={handleUpload} style={{ marginBottom: 16 }}>
      <input type="file" ref={fileRef} required />
      <button type="submit">上传模板</button>
    </form>
  );
}

export default UploadTemplate;