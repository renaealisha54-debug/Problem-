import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import Navbar from './components/Navbar';
import TerminalPanel from './components/TerminalPanel';
import useTheme from './hooks/useTheme';

const BACKEND = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API_KEY = process.env.REACT_APP_API_KEY || "";

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [terminal, setTerminal] = useState("System ready...");
  const [loading, setLoading] = useState(null);
  const [explanation, setExplanation] = useState("");
  const [appName, setAppName] = useState("ProblemCode App");
  const [packageName, setPackageName] = useState("com.problemcode.app");
  const editorRef = useRef(null);
  const { dark, toggle: toggleDark } = useTheme();

  const api = async (path, body) => {
    try {
      const headers = { "Content-Type": "application/json" };
      if (API_KEY) headers["X-API-Key"] = API_KEY;
      const res = await fetch(`${BACKEND}${path}`, {
        method: "POST",
        headers,
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || err.error || `Server error: ${res.status}`);
      }
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
    if (!code.trim()) { setTerminal("Nothing to run."); return; }
    setTerminal("Running...");
    const data = await api("/api/execute", { code, language });
    if (data) {
      const out = data.result || data.error || "No output.";
      const err = data.error && data.result ? `\nStderr: ${data.error}` : "";
      setTerminal(out + err);
    }
  });

  const handleCorrect = withLoading("correct", async () => {
    if (!code.trim()) { setTerminal("Nothing to correct."); return; }
    setTerminal("AI analyzing...");
    const data = await api("/api/ai/correct", { code, language });
    if (data?.corrected_code) {
      setCode(data.corrected_code);
      setTerminal("Correction applied.");
    }
  });

  const handleConvert = withLoading("convert", async () => {
    if (!code.trim()) { setTerminal("Nothing to convert."); return; }
    setTerminal("Converting...");
    const data = await api("/api/ai/convert", { code, language });
    if (data?.converted_code) {
      setCode(data.converted_code);
      setLanguage(data.new_language);
      setTerminal(`Converted to ${data.new_language}.`);
    }
  });

  const handleExplain = withLoading("explain", async () => {
    if (!code.trim()) { setTerminal("Nothing to explain."); return; }
    setTerminal("Generating explanation...");
    const data = await api("/api/ai/explain", { code, language });
    if (data?.explanation) {
      setExplanation(data.explanation);
      setTerminal("Explanation ready.");
    }
  });

  const handleExportAPK = withLoading("apk", async () => {
    if (!code.trim()) { setTerminal("Write some code first."); return; }
    setTerminal("Building APK — this may take a few minutes...");
    const data = await api("/api/build/apk", {
      code,
      app_name: appName,
      package_name: packageName
    });
    if (data?.download_url) {
      setTerminal(`APK ready! Downloading...`);
      window.open(`${BACKEND}${data.download_url}`, "_blank");
    } else if (data) {
      setTerminal(`Build failed: ${data.error || "Unknown error"}\n${data.log || ""}`);
    }
  });

  const handleCopy = () => {
    if (!code) { setTerminal("Nothing to copy."); return; }
    navigator.clipboard.writeText(code).then(
      () => setTerminal("Code copied to clipboard."),
      () => setTerminal("Clipboard access denied.")
    );
  };

  const handleClear = () => {
    setCode("");
    setTerminal("Editor cleared.");
    setExplanation("");
  };

  return (
    <div className={`h-screen flex flex-col ${dark ? "bg-[#0d1117] text-white" : "bg-gray-100 text-gray-900"}`}>
      <Navbar
        language={language}
        setLanguage={setLanguage}
        loading={loading}
        dark={dark}
        toggleDark={toggleDark}
        onRun={handleRun}
        onCorrect={handleCorrect}
        onConvert={handleConvert}
        onExplain={handleExplain}
        onCopy={handleCopy}
        onClear={handleClear}
        appName={appName}
        setAppName={setAppName}
        packageName={packageName}
        setPackageName={setPackageName}
      />
      <div className="flex-1 flex overflow-hidden">
        <div className={`w-2/3 border-r ${dark ? "border-gray-800" : "border-gray-300"}`}>
          <Editor
            height="100%"
            theme={dark ? "vs-dark" : "light"}
            language={language}
            value={code}
            onChange={val => setCode(val || "")}
            onMount={e => { editorRef.current = e; }}
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              wordWrap: "on",
              scrollBeyondLastLine: false,
            }}
          />
        </div>
        <TerminalPanel
          terminal={terminal}
          explanation={explanation}
          loading={loading}
          onExportAPK={handleExportAPK}
          dark={dark}
        />
      </div>
    </div>
  );
  }
