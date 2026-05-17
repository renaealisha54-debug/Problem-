import { useState, useEffect } from 'react';

const getInitialDark = () => {
  if (typeof window === 'undefined') return false;
  try {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  } catch {
    return false;
  }
};

export default function useTheme() {
  const [dark, setDark] = useState(getInitialDark);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = e => setDark(e.matches);
      mq.addEventListener('change', handler);
      return () => mq.removeEventListener('change', handler);
    } catch {
      // matchMedia not supported
    }
  }, []);

  return { dark, toggle: () => setDark(d => !d) };
}
