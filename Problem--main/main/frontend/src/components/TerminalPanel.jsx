import React, { useEffect, useRef } from 'react';
import { Download } from 'lucide-react';

export default function TerminalPanel({ terminal, explanation, loading, onExportAPK, dark }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [terminal]);

  return (
    <div className={`w-1/3 flex flex-col ${dark ? "bg-[#0d1117]" : "bg-gray-50"}`}>
      <div className={`p-2 border-b text-xs font-mono uppercase tracking-widest ${dark ? "border-gray-800 text-gray-500" : "border-gray-300 text-gray-400"}`}>
        Terminal Output
      </div>
      <pre className={`p-4 flex-1 font-mono text-sm overflow-auto whitespace-pre-wrap leading-relaxed ${dark ? "text-green-400" : "text-gray-800"}`}>
        {terminal}
        <div ref={bottomRef}/>
      </pre>

      {explanation && (
        <div className={`p-3 border-t text-sm ${dark ? "border-gray-800 text-gray-300 bg-gray-900" : "border-gray-300 text-gray-700 bg-white"}`}>
          <div className="font-bold mb-1 text-yellow-500">Explanation</div>
          <div className="whitespace-pre-wrap">{explanation}</div>
        </div>
      )}

      <div className={`p-4 border-t ${dark ? "border-gray-800" : "border-gray-300"}`}>
        <button
          onClick={onExportAPK}
          disabled={loading !== null}
          className="w-full bg-gray-800 hover:bg-gray-700 text-white py-2 rounded flex items-center justify-center gap-2 disabled:opacity-50 transition-colors"
        >
          {loading === "apk" ? <span className="animate-spin">⟳</span> : <Download size={16}/>}
          Export APK
        </button>
      </div>
    </div>
  );
}
