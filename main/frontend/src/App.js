import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Sparkles, Smartphone, RefreshCw, Download } from 'lucide-react';

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [terminal, setTerminal] = useState("System ready...");
  const backendUrl = "http://localhost:8000";

  const apiRequest = async (path, body) => {
    try {
      const res = await fetch(`${backendUrl}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      return await res.json();
    } catch (e) {
      setTerminal("Error: Connection to backend failed.");
    }
  };

  const handleExecute = async () => {
    setTerminal("Running...");
    const data = await apiRequest("/api/execute", { code, language });
    setTerminal(data.result || data.error);
  };

  const handleAICorrect = async () => {
    setTerminal("AI Analyzing...");
    const data = await apiRequest("/api/ai/correct", { code, language });
    if (data.corrected_code) setCode(data.corrected_code);
    setTerminal("AI Correction Applied.");
  };

  const handleConvert = async () => {
    setTerminal("Converting...");
    const data = await apiRequest("/api/ai/convert", { code, language });
    if (data.converted_code) {
      setLanguage(data.new_language);
      setCode(data.converted_code);
      setTerminal(`Converted to ${data.new_language}`);
    }
  };

  const handleExportAPK = async () => {
    setTerminal("Building APK...");
    const data = await apiRequest("/api/build/apk", { code });
    if (data.download_url) {
      setTerminal(`APK ready: ${data.download_url}`);
      window.open(`${backendUrl}${data.download_url}`, '_blank');
    } else {
      setTerminal(`Build failed: ${data.error}\n${data.log || ''}`);
    }
  };

  return (
    <div className="h-screen bg-[#0d1117] text-white flex flex-col">
      <nav className="p-4 border-b border-gray-800 flex justify-between bg-[#161b22]">
        <h1 className="text-xl font-bold flex items-center gap-2 text-blue-400">
          <Smartphone size={24}/> ProblemCode
        </h1>
        <div className="flex gap-2">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-gray-800 text-white px-2 py-1 rounded text-sm"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>
          <button onClick={handleAICorrect} className="flex items-center gap-1 bg-purple-600 px-3 py-1 rounded hover:bg-purple-700">
            <Sparkles size={16}/> Correct
          </button>
          <button onClick={handleConvert} className="flex items-center gap-1 bg-green-600 px-3 py-1 rounded hover:bg-green-700">
            <RefreshCw size={16}/> Convert
          </button>
          <button onClick={handleExecute} className="flex items-center gap-1 bg-blue-600 px-3 py-1 rounded hover:bg-blue-700">
            <Play size={16}/> Run
          </button>
        </div>
      </nav>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-2/3 border-r border-gray-800">
          <Editor
            height="100%"
            theme="vs-dark"
            language={language}
            value={code}
            onChange={(val) => setCode(val)}
            options={{ fontSize: 14, minimap: { enabled: false } }}
          />
        </div>
        <div className="w-1/3 flex flex-col bg-black">
          <div className="p-2 border-b border-gray-800 text-xs font-mono text-gray-500 uppercase">Terminal Output</div>
          <pre className="p-4 flex-1 font-mono text-sm overflow-auto text-green-400">
            {terminal}
          </pre>
          <div className="p-4 border-t border-gray-800">
            <button
              onClick={handleExportAPK}
              className="w-full bg-gray-800 py-2 rounded flex items-center justify-center gap-2 hover:bg-gray-700"
            >
              <Download size={18}/> Export APK
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
