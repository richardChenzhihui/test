import React, { useEffect, useState } from 'react';
import TemplateList from './components/TemplateList';
import UploadTemplate from './components/UploadTemplate';
import AICompose from './components/AICompose';

function App() {
  const [templates, setTemplates] = useState([]);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    fetch('http://localhost:3001/api/templates')
      .then(res => res.json())
      .then(setTemplates)
      .catch(() => setTemplates([]));
  }, [refresh]);

  return (
    <div style={{ padding: 16, fontFamily: 'Segoe UI' }}>
      <h2>Word Legal Assistant</h2>
      <UploadTemplate onUpload={() => setRefresh(r => !r)} />
      <TemplateList templates={templates} />
      <AICompose />
    </div>
  );
}

export default App;