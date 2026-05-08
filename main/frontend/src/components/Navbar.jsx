import React from 'react';
import { Play, Sparkles, Smartphone, RefreshCw, BookOpen, Trash2, Copy, Moon, Sun } from 'lucide-react';

export default function Navbar({ language, setLanguage, loading, dark, toggleDark, onRun, onCorrect, onConvert, onExplain, onCopy, onClear }) {

  const btn = (key, onClick, color, icon, label) => (
    <button
      key={key}
      onClick={onClick}
      disabled={loading !== null}
      className={`flex items-center gap-1 ${color} px-3 py-1 rounded text-sm disabled:opacity-50`}
    >
      {loading === key ? <span className="animate-spin">⟳</span> : icon}
      {label}
    </button>
  );

  return (
    <nav className={`p-3 border-b flex justify-between items-center flex-wrap gap-2 ${dark ? "bg-[#161b22] border-gray-800" : "bg-white border-gray-300"}`}>
      <h1 className="text-lg font-bold flex items-center gap-2 text-blue-400">
        <Smartphone size={20}/> ProblemCode
      </h1>
      <div className="flex gap-2 flex-wrap items-center">
        <select
          value={language}
          onChange={e => setLanguage(e.target.value)}
          className={`px-2 py-1 rounded text-sm ${dark ? "bg-gray-800 text-white" : "bg-gray-200"}`}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
        </select>
        {btn("correct", onCorrect, "bg-purple-600 hover:bg-purple-700", <Sparkles size={14}/>, "Correct")}
        {btn("convert", onConvert, "bg-green-600 hover:bg-green-700", <RefreshCw size={14}/>, "Convert")}
        {btn("explain", onExplain, "bg-yellow-600 hover:bg-yellow-700", <BookOpen size={14}/>, "Explain")}
        {btn("run", onRun, "bg-blue-600 hover:bg-blue-700", <Play size={14}/>, "Run")}
        <button onClick={onCopy} className="p-1 rounded hover:bg-gray-700" title="Copy"><Copy size={16}/></button>
        <button onClick={onClear} className="p-1 rounded hover:bg-gray-700" title="Clear"><Trash2 size={16}/></button>
        <button onClick={toggleDark} className="p-1 rounded hover:bg-gray-700">{dark ? <Sun size={16}/> : <Moon size={16}/>}</button>
      </div>
    </nav>
  );
}
