import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Sparkles, Smartphone, RefreshCw, Download, BookOpen, Trash2, Copy, Moon, Sun } from 'lucide-react';

const BACKEND = "http://localhost:8000";

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [terminal, setTerminal] = useState("System ready...");
  const [loading, setLoading] = useState(null);
  const [darkMode, setDarkMode] = useState(true);
  const [explanation, setExplanation] = useState("");
  const editorRef = useRef(null);

  const api = async (path, body) => {
    try {
      const res = await fetch(`${BACKEND}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      return await res.json();
    } catch (e) {
      setTerminal(`Error: ${e.message}`);
      return null;
    }
  };

  const withLoading = (key, fn) => async () => {
    setLoading(key);
    setExplanation("");
    await fn();
    setLoading(null);
  };

  const handleRun = withLoading("run", async () => {
    setTerminal("Running...");
    const data = await api("/api/execute", { code, language });
    if (data) setTerminal(data.result || data.error || "No output.");
  });

  const handleCorrect = withLoading("correct", async () => {
    setTerminal("AI analyzing...");
    const data = await api("/api/ai/correct", { code, language });
    if (data?.corrected_code) { setCode(data.corrected_code); setTerminal("Correction applied."); }
  });

  const handleConvert = withLoading("convert", async () => {
    setTerminal("Converting...");
    const data = await api("/api/ai/convert", { code, language });
    if (data?.converted_code) {
      setCode(data.converted_code);
      setLanguage(data.new_language);
      setTerminal(`Converted to ${data.new_language}.`);
    }
  });

  const handleExplain = withLoading("explain", async () => {
    setTerminal("Generating explanation...");
    const data = await api("/api/ai/explain", { code, language });
    if (data?.explanation) {
      setExplanation(data.explanation);
      setTerminal("Explanation ready.");
    }
  });

  const handleExportAPK = withLoading("apk", async () => {
    setTerminal("Building APK — this may take a few minutes...");
    const data = await api("/api/build/apk", { code });
    if (data?.download_url) {
      setTerminal(`APK ready: ${data.download_url}`);
      window.open(`${BACKEND}${data.download_url}`, "_blank");
    } else {
      setTerminal(`Build failed: ${data?.error || "Unknown error"}\n${data?.log || ""}`);
    }
  });

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setTerminal("Code copied to clipboard.");
  };

  const handleClear = () => {
    setCode("");
    setTerminal("Editor cleared.");
    setExplanation("");
  };

  const btn = (key, onClick, color, icon, label) => (
    <button
      onClick={onClick}
      disabled={loading !== null}
      className={`flex items-center gap-1 ${color} px-3 py-1 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {loading === key ? <span className="animate-spin">⟳</span> : icon}
      {label}
    </button>
  );

  return (
    <div className={`h-screen flex flex-col ${darkMode ? "bg-[#0d1117] text-white" : "bg-gray-100 text-gray-900"}`}>

      {/* Navbar */}
      <nav className={`p-3 border-b flex justify-between items-center ${darkMode ? "bg-[#161b22] border-gray-800" : "bg-white border-gray-300"}`}>
        <h1 className="text-lg font-bold flex items-center gap-2 text-blue-400">
          <Smartphone size={20}/> ProblemCode
        </h1>
        <div className="flex gap-2 flex-wrap items-center">
          <select
            value={language}
            onChange={e => setLanguage(e.target.value)}
            className={`px-2 py-1 rounded text-sm ${darkMode ? "bg-gray-800 text-white" : "bg-gray-200 text-gray-900"}`}
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>
          {btn("correct", handleCorrect, "bg-purple-600 hover:bg-purple-700", <Sparkles size={14}/>, "Correct")}
          {btn("convert", handleConvert, "bg-green-600 hover:bg-green-700", <RefreshCw size={14}/>, "Convert")}
          {btn("explain", handleExplain, "bg-yellow-600 hover:bg-yellow-700", <BookOpen size={14}/>, "Explain")}
          {btn("run", handleRun, "bg-blue-600 hover:bg-blue-700", <Play size={14}/>, "Run")}
          <button onClick={handleCopy} className="p-1 rounded hover:bg-gray-700" title="Copy"><Copy size={16}/></button>
          <button onClick={handleClear} className="p-1 rounded hover:bg-gray-700" title="Clear"><Trash2 size={16}/></button>
          <button onClick={() => setDarkMode(!darkMode)} className="p-1 rounded hover:bg-gray-700">
            {darkMode ? <Sun size={16}/> : <Moon size={16}/>}
          </button>
        </div>
      </nav>

      {/* Main */}
      <div className="flex-1 flex overflow-hidden">

        {/* Editor */}
        <div className={`w-2/3 border-r ${darkMode ? "border-gray-800" : "border-gray-300"}`}>
          <Editor
            height="100%"
            theme={darkMode ? "vs-dark" : "light"}
            language={language}
            value={code}
            onChange={val => setCode(val || "")}
            onMount={e => editorRef.current = e}
            options={{ fontSize: 14, minimap: { enabled: false }, wordWrap: "on", scrollBeyondLastLine: false }}
          />
        </div>

        {/* Right Panel */}
        <div className={`w-1/3 flex flex-col ${darkMode ? "bg-black" : "bg-gray-50"}`}>
          <div className={`p-2 border-b text-xs font-mono uppercase ${darkMode ? "border-gray-800 text-gray-500" : "border-gray-300 text-gray-400"}`}>
            Terminal Output
          </div>
          <pre className="p-4 flex-1 font-mono text-sm overflow-auto text-green-400 whitespace-pre-wrap">
            {terminal}
          </pre>

          {explanation && (
            <div className={`p-3 border-t text-sm ${darkMode ? "border-gray-800 text-gray-300 bg-gray-900" : "border-gray-300 text-gray-700 bg-white"}`}>
              <div className="font-bold mb-1 text-yellow-400">Explanation</div>
              <div className="whitespace-pre-wrap">{explanation}</div>
            </div>
          )}

          <div className={`p-4 border-t ${darkMode ? "border-gray-800" : "border-gray-300"}`}>
            <button
              onClick={handleExportAPK}
              disabled={loading !== null}
              className="w-full bg-gray-800 hover:bg-gray-700 text-white py-2 rounded flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading === "apk" ? <span className="animate-spin">⟳</span> : <Download size={16}/>}
              Export APK
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
