import React, { useState, useEffect } from 'react';

export default function App() {
  // Authentication & Security Panel Routing
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // App System Core Parameters
  const [prompt, setPrompt] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('English');
  const [loading, setLoading] = useState(false);
  const [videoProject, setVideoProject] = useState(null);
  const [playingState, setPlayingState] = useState({});
  const [activeMasterVideo, setActiveMasterVideo] = useState(null);

  // Real-Time Rendering Processing Engine Metrics
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  // Authentication Gateway Handlers
  const handleLogin = (e) => {
    e.preventDefault();
    if (username.trim() === 'admin' && password === 'admin123') {
      setIsLoggedIn(true);
    } else {
      alert("Invalid Security Signature! (Demo Keys: admin / admin123)");
    }
  };

  // High-Resolution Counter Core Loop
  useEffect(() => {
    let interval = null;
    if (loading) {
      interval = setInterval(() => {
        setSecondsElapsed((prevSeconds) => prevSeconds + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const formatTime = (totalSeconds) => {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleGenerateVideo = async () => {
    if (!prompt.trim()) return alert("Please specify a baseline narrative prompt!");
    setLoading(true);
    setSecondsElapsed(0); 
    setVideoProject(null);
    setActiveMasterVideo(null);
    setPlayingState({});
    
    try {
      const cleanPrompt = encodeURIComponent(prompt.trim());
      
      // Multi-Lingual Automation Engine Localization Streams Configuration
      const translations = {
        English: {
          v1: `Opening structural cinematic feed rendering localized tracking data parameters for "${prompt}". Audio track decoupled.`,
          v2: "The narrative framework peaks as automated sequence structures adjust audio layouts smoothly."
        },
        Hindi: {
          v1: `"${prompt}" के लिए सिनेमाई दृश्य संरचना आरंभ की जा रही है। एआई ऑडियो डबिंग स्ट्रीम सक्रिय है।`,
          v2: "सिमुलेशन अपने चरम पर पहुंच गया है क्योंकि न्यूरल ऑडियो परतें मूल वीडियो संरचना के साथ सिंक्रनाइज़ हो रही हैं।"
        },
        Spanish: {
          v1: `Iniciando la secuencia de diseño visual cinematográfico para "${prompt}". Canal de doblaje de audio activado.`,
          v2: "El marco de simulación alcanza su punto máximo a medida que las capas de audio neuronal se fusionan."
        },
        Telugu: {
          v1: `"${prompt}" కోసం సినిమాటిక్ విజువల్ లేఅవుట్ సీక్వెన్స్ ప్రారంభించబడింది. ఏఐ ఆడియో డబ్బింగ్ స్ట్రీమ్ యాక్టివ్‌గా ఉంది.`,
          v2: "న్యూరల్ ఆడియో లేయర్‌లు ఒరిజినల్ వీడియో స్ట్రక్చర్‌తో పక్కాగా సింక్ అవ్వడంతో విజువల్స్ ముగుస్తాయి."
        }
      };

      const voiceoverText = translations[targetLanguage] || translations['English'];

      const newProject = {
        title: prompt,
        language: targetLanguage,
        scenes: [
          {
            id: 1,
            title: `🎬 Scene 1: Multi-Lingual Establishing Matrix [${targetLanguage}]`,
            voiceover: voiceoverText.v1,
            videoUrl: `https://pollinations.ai{cleanPrompt}%20cinematic%20hyperrealistic%20video%20sequence%204k%20motion%20neon%20gold%20lighting?width=1024&height=576&seed=88&enhance=true&nologo=true`
          },
          {
            id: 2,
            title: `⚡ Scene 2: Ultra-Dynamic Dubbed Output [${targetLanguage}]`,
            voiceover: voiceoverText.v2,
            videoUrl: `https://pollinations.ai{cleanPrompt}%20slow%20motion%20drone%20shot%20highly%20detailed%20epic%20movement%20cyberpunk%20luxury?width=1024&height=576&seed=77&enhance=true&nologo=true`
          }
        ]
      };

      // Artificial cloud compiler baseline timeout execution
      await new Promise(resolve => setTimeout(resolve, 4000));
      setVideoProject(newProject);
      
      if (newProject.scenes && newProject.scenes.length > 0) {
        setActiveMasterVideo(newProject.scenes[0].videoUrl);
      }
    } catch (error) {
      alert("Neural Compilation Timeout - Backend Matrix Disconnected.");
    } finally {
      setLoading(false);
    }
  };

  const togglePlay = (id) => {
    setPlayingState(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // 🌟 GATEWAY INTERFACE: PREMIUM BLACK & DEEP GOLD LOGIN HUB
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-[#070708] flex items-center justify-center p-4 relative overflow-hidden font-sans">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-amber-500/5 rounded-full blur-[140px] pointer-events-none"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-yellow-600/5 rounded-full blur-[140px] pointer-events-none"></div>

        <div className="w-full max-w-md bg-[#0d0d0f] border border-amber-500/20 rounded-3xl p-8 shadow-2xl relative backdrop-blur-xl ring-1 ring-amber-500/10">
          <div className="text-center space-y-3 mb-8">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-amber-600 via-yellow-500 to-amber-400 flex items-center justify-center shadow-xl shadow-amber-600/10 mx-auto">
              <span className="text-[#070708] font-black text-2xl">⚡</span>
            </div>
            <div className="space-y-1">
              <span className="text-[10px] font-bold tracking-[0.2em] text-amber-500/80 uppercase block font-mono">Premium Terminal Access</span>
              <h1 className="text-2xl font-black tracking-tight text-slate-100">
                NEXUS <span className="bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-500 bg-clip-text text-transparent">GOLD</span>
              </h1>
            </div>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-amber-400/70 tracking-wider uppercase block font-mono">Operator ID</label>
              <input 
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g., admin"
                className="w-full bg-[#121215] border border-slate-800 focus:border-amber-500/60 rounded-xl p-3.5 text-slate-100 text-sm focus:outline-none transition font-mono placeholder:text-slate-700"
                required
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-amber-400/70 tracking-wider uppercase block font-mono">Access Signature Key</label>
              <input 
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#121215] border border-slate-800 focus:border-amber-500/60 rounded-xl p-3.5 text-slate-100 text-sm focus:outline-none transition font-mono placeholder:text-slate-700"
                required
              />
            </div>

            <button 
              type="submit"
              className="w-full mt-2 bg-gradient-to-r from-amber-600 via-yellow-500 to-amber-500 hover:opacity-90 text-[#070708] font-bold py-3.5 px-4 rounded-xl transition-all duration-300 shadow-lg shadow-amber-500/10 text-sm tracking-wide uppercase font-mono"
            >
              Verify Core Credentials
            </button>
          </form>

          <div className="text-center mt-6">
            <p className="text-[10px] text-slate-600 font-mono">Terminal Defaults: <span className="text-amber-500/50">admin</span> / <span className="text-amber-500/50">admin123</span></p>
          </div>
        </div>
      </div>
    );
  }

  // 🌟 APP CORE MONITOR PANEL: GOLD AUTOMATION LAB WORKSPACE
  return (
    <div className="min-h-screen bg-[#030712] text-slate-100 font-sans p-4 sm:p-8 relative overflow-hidden">
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-amber-500/5 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="max-w-7xl mx-auto space-y-10">
        
        {/* Navigation & Status Header Block */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-yellow-500 to-amber-600 flex items-center justify-center shadow-lg">
              <span className="text-[#030712] font-bold text-xl">▶</span>
            </div>
            <div>
              <span className="text-xs font-bold font-mono tracking-widest text-amber-500 block uppercase">AUTOMATED SYNC MODULE</span>
              <h1 className="text-xl font-black tracking-tight text-white">NEXUS STUDIO <span className="text-amber-400 text-xs font-mono px-1.5 py-0.5 rounded border border-amber-500/20 bg-amber-950/20">PRO</span></h1>
            </div>
          </div>
          <button 
            onClick={() => setIsLoggedIn(false)}
            className="px-4 py-2 border border-amber-500/30 rounded-xl text-xs font-mono text-amber-400 hover:bg-amber-500/10 transition backdrop-blur-md"
          >
            Lock System Console
          </button>
        </div>

        {/* Operating Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Console Configuration Input Panel (4 Units Wide) */}
