<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Developer Telemetry & Profile | AI x IoT x Embedded</title>
  
  <!-- External Resources -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&family=Orbitron:wght@400;600;800;900&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Fira Code', 'monospace'],
            orbitron: ['Orbitron', 'sans-serif'],
            mono: ['Fira Code', 'monospace'],
          },
          colors: {
            cyber: {
              bg: '#06080e',
              card: 'rgba(12, 17, 29, 0.75)',
              border: 'rgba(0, 243, 255, 0.25)',
              cyan: '#00f3ff',
              green: '#00ff66',
              purple: '#b026ff',
              amber: '#ffb700',
              pink: '#ff0055',
            }
          },
          animation: {
            'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            'glow-cyan': 'glowCyan 2s ease-in-out infinite alternate',
            'scanline': 'scanline 8s linear infinite',
            'float': 'float 4s ease-in-out infinite',
          },
          keyframes: {
            glowCyan: {
              '0%': { boxShadow: '0 0 5px rgba(0, 243, 255, 0.2), inset 0 0 5px rgba(0, 243, 255, 0.1)' },
              '100%': { boxShadow: '0 0 20px rgba(0, 243, 255, 0.6), inset 0 0 15px rgba(0, 243, 255, 0.3)' }
            },
            scanline: {
              '0%': { transform: 'translateY(-100%)' },
              '100%': { transform: 'translateY(1000%)' }
            },
            float: {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-6px)' }
            }
          }
        }
      }
    }
  </script>

  <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #06080e;
    }
    ::-webkit-scrollbar-thumb {
      background: #00f3ff55;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #00f3ff;
    }

    /* Cyber Glassmorphism & Corner Reticles */
    .cyber-hud-card {
      position: relative;
      background: rgba(10, 15, 26, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(0, 243, 255, 0.2);
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.7), inset 0 0 15px rgba(0, 243, 255, 0.03);
      transition: all 0.3s ease;
    }

    .cyber-hud-card:hover {
      border-color: rgba(0, 243, 255, 0.6);
      box-shadow: 0 0 25px rgba(0, 243, 255, 0.25), inset 0 0 20px rgba(0, 243, 255, 0.08);
    }

    /* Corner Bracket Accents */
    .corner-brackets::before, .corner-brackets::after {
      content: '';
      position: absolute;
      width: 8px;
      height: 8px;
      pointer-events: none;
      transition: all 0.3s ease;
    }
    .corner-brackets::before {
      top: -1px; left: -1px;
      border-top: 2px solid #00f3ff;
      border-left: 2px solid #00f3ff;
    }
    .corner-brackets::after {
      bottom: -1px; right: -1px;
      border-bottom: 2px solid #00f3ff;
      border-right: 2px solid #00f3ff;
    }

    /* Scanlines Overlay */
    .crt-overlay {
      background: linear-gradient(
        rgba(18, 16, 16, 0) 50%, 
        rgba(0, 0, 0, 0.25) 50%
      ), linear-gradient(
        90deg,
        rgba(255, 0, 0, 0.03),
        rgba(0, 255, 0, 0.01),
        rgba(0, 0, 255, 0.03)
      );
      background-size: 100% 4px, 6px 100%;
      pointer-events: none;
    }

    /* Glowing Text Effect */
    .glow-text-cyan {
      text-shadow: 0 0 10px rgba(0, 243, 255, 0.7), 0 0 20px rgba(0, 243, 255, 0.4);
    }
    .glow-text-green {
      text-shadow: 0 0 10px rgba(0, 255, 102, 0.7), 0 0 20px rgba(0, 255, 102, 0.4);
    }
    .glow-text-purple {
      text-shadow: 0 0 10px rgba(176, 38, 255, 0.7), 0 0 20px rgba(176, 38, 255, 0.4);
    }

    /* SVG Diagram Connection Beams */
    .path-pulse {
      stroke-dasharray: 8, 8;
      animation: dash 1.5s linear infinite;
    }
    @keyframes dash {
      to {
        stroke-dashoffset: -16;
      }
    }
  </style>
</head>

<body class="bg-[#06080e] text-slate-200 font-mono antialiased min-h-screen relative overflow-x-hidden selection:bg-cyber-cyan selection:text-black">

  <!-- Ambient Particle Canvas Background -->
  <canvas id="bgCanvas" class="fixed inset-0 pointer-events-none z-0 opacity-40"></canvas>
  
  <!-- CRT Grid Overlay -->
  <div id="crtScreen" class="fixed inset-0 crt-overlay z-50 opacity-60 pointer-events-none"></div>

  <!-- Foreground Interface Wrap -->
  <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">

    <!-- Top HUD Navigation / Cyber Bar -->
    <header class="cyber-hud-card rounded-lg p-4 corner-brackets flex flex-wrap items-center justify-between gap-4 border-l-4 border-l-cyber-cyan">
      <div class="flex items-center space-x-3">
        <div class="relative">
          <div class="w-3 h-3 rounded-full bg-cyber-green animate-ping absolute"></div>
          <div class="w-3 h-3 rounded-full bg-cyber-green relative"></div>
        </div>
        <div>
          <span class="font-orbitron tracking-widest text-xs text-cyber-cyan block font-semibold">CORE TELEMETRY OS</span>
          <span class="text-xs text-slate-400">DEV.NODE // LATENCY: <span id="pingCounter" class="text-cyber-green">14ms</span></span>
        </div>
      </div>

      <!-- Quick Metrics Telemetry HUD -->
      <div class="flex items-center space-x-6 text-xs text-slate-300">
        <div class="hidden sm:block">
          <span class="text-slate-500">FPS:</span> <span id="fpsCounter" class="text-cyber-cyan font-bold">60</span>
        </div>
        <div class="hidden md:block">
          <span class="text-slate-500">SYSTEM CLOCK:</span> <span id="sysClock" class="text-cyber-amber font-mono">00:00:00 UTC</span>
        </div>
        <!-- Audio Synth Toggle Button -->
        <button id="soundToggleBtn" onclick="toggleAudio()" class="px-3 py-1.5 rounded border border-cyber-cyan/40 hover:bg-cyber-cyan/10 text-cyber-cyan text-xs flex items-center space-x-2 transition">
          <i id="soundIcon" class="fa-solid fa-volume-xmark"></i>
          <span id="soundText">SFX: OFF</span>
        </button>
      </div>
    </header>

    <!-- SECTION 1: SYSTEM INITIALIZATION -->
    <section class="space-y-3">
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-terminal text-cyber-cyan"></i>
        <h2 class="font-orbitron text-sm font-bold tracking-wider text-cyber-cyan uppercase">
          SYSTEM INITIALIZATION
        </h2>
        <div class="h-[1px] flex-grow bg-gradient-to-r from-cyber-cyan/50 to-transparent"></div>
      </div>

      <div class="cyber-hud-card rounded-xl p-6 corner-brackets border-t-2 border-t-cyber-cyan relative overflow-hidden">
        
        <!-- Header status text -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4 mb-4">
          <div class="font-mono text-sm text-cyber-cyan flex items-center space-x-2">
            <span class="animate-pulse">></span>
            <span class="glow-text-cyan font-bold">booting developer.profile...</span>
          </div>
          <div class="text-xs px-3 py-1 rounded bg-cyber-green/10 border border-cyber-green/30 text-cyber-green font-bold flex items-center space-x-2 w-fit">
            <span class="w-2 h-2 rounded-full bg-cyber-green animate-pulse"></span>
            <span>SYSTEM STATUS: OPERATIONAL</span>
          </div>
        </div>

        <!-- Animated Progress Bar -->
        <div class="space-y-2 mb-6">
          <div class="flex justify-between text-xs text-slate-400">
            <span>INITIALIZING KERNEL MODULES</span>
            <span class="text-cyber-cyan font-bold">[████████████████████████████████████████] 100%</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-3 p-0.5 border border-cyber-cyan/30">
            <div class="bg-gradient-to-r from-cyber-purple via-cyber-cyan to-cyber-green h-full rounded-full transition-all duration-1000 shadow-[0_0_12px_rgba(0,243,255,0.8)]" style="width: 100%;"></div>
          </div>
        </div>

        <!-- Module Diagnostics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs sm:text-sm">
          
          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ AI MODULE</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ COMPUTER VISION</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ IoT NETWORK</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ EMBEDDED SYSTEM</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ CLOUD SERVICES</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

          <div class="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800 hover:border-cyber-cyan/40 transition group">
            <span class="text-slate-300 font-medium group-hover:text-cyber-cyan transition">✓ SOFTWARE ENGINEERING</span>
            <span class="dots text-slate-600 flex-grow mx-2 hidden sm:inline">....................</span>
            <span class="px-2 py-0.5 rounded text-xs bg-cyber-green/20 text-cyber-green border border-cyber-green/40 font-bold glow-text-green">ONLINE</span>
          </div>

        </div>

      </div>
    </section>

    <!-- SECTION 2: TECHNOLOGY MATRIX -->
    <section class="space-y-3">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-microchip text-cyber-purple"></i>
          <h2 class="font-orbitron text-sm font-bold tracking-wider text-cyber-purple uppercase">
            TECHNOLOGY MATRIX
          </h2>
          <div class="h-[1px] w-24 bg-gradient-to-r from-cyber-purple/50 to-transparent"></div>
        </div>
        <span class="font-orbitron text-xs font-semibold px-3 py-1 rounded bg-cyber-purple/10 border border-cyber-purple/30 text-cyber-purple glow-text-purple">
          AI × IoT × EMBEDDED
        </span>
      </div>

      <div class="cyber-hud-card rounded-xl p-6 corner-brackets border-t-2 border-t-cyber-purple relative overflow-hidden min-h-[460px] flex flex-col justify-center">
        
        <!-- Interactive Technology Node Flowchart (HTML/SVG Grid) -->
        <div class="relative w-full max-w-4xl mx-auto py-4">
          
          <!-- Top Level: ARTIFICIAL INTELLIGENCE -->
          <div class="flex justify-center mb-6">
            <div class="node-box p-3 sm:p-4 rounded-xl bg-slate-900/90 border-2 border-cyber-purple shadow-[0_0_15px_rgba(176,38,255,0.3)] text-center w-64 hover:scale-105 transition duration-300 cursor-pointer group">
              <i class="fa-solid fa-brain text-cyber-purple text-xl mb-1 group-hover:animate-bounce"></i>
              <div class="font-orbitron font-bold text-slate-100 text-sm">ARTIFICIAL</div>
              <div class="font-orbitron font-bold text-cyber-purple text-sm glow-text-purple">INTELLIGENCE</div>
            </div>
          </div>

          <!-- Down Arrow Signal to Data/Model -->
          <div class="flex justify-center mb-6">
            <div class="flex flex-col items-center">
              <div class="w-0.5 h-8 bg-gradient-to-b from-cyber-purple to-cyber-cyan"></div>
              <i class="fa-solid fa-chevron-down text-cyber-cyan text-xs animate-bounce"></i>
            </div>
          </div>

          <!-- Level 2: DATA / MODEL -->
          <div class="flex justify-center mb-8">
            <div class="node-box p-2.5 sm:p-3 rounded-lg bg-slate-900/90 border border-cyber-cyan shadow-[0_0_12px_rgba(0,243,255,0.2)] text-center w-56 hover:border-cyber-cyan transition cursor-pointer">
              <i class="fa-solid fa-database text-cyber-cyan text-sm mr-2"></i>
              <span class="font-orbitron font-bold text-slate-200 text-xs sm:text-sm tracking-wider">DATA / MODEL</span>
            </div>
          </div>

          <!-- Connector Lines for AI - IoT - EMBEDDED -->
          <div class="relative mb-8">
            <!-- Tri-Node Horizontal Flow -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 relative z-10">
              
              <!-- Left: AI -->
              <div class="node-box p-3 rounded-lg bg-slate-900/90 border border-cyber-cyan text-center hover:border-cyber-cyan hover:shadow-[0_0_15px_rgba(0,243,255,0.3)] transition">
                <i class="fa-solid fa-robot text-cyber-cyan mb-1"></i>
                <div class="font-orbitron font-bold text-sm text-slate-200">AI</div>
              </div>

              <!-- Center Hub: IoT -->
              <div class="node-box p-3 rounded-lg bg-slate-900/90 border-2 border-cyber-green shadow-[0_0_20px_rgba(0,255,102,0.3)] text-center hover:scale-105 transition">
                <i class="fa-solid fa-network-wired text-cyber-green mb-1 text-lg animate-pulse"></i>
                <div class="font-orbitron font-bold text-sm text-cyber-green glow-text-green">IoT</div>
              </div>

              <!-- Right: EMBEDDED -->
              <div class="node-box p-3 rounded-lg bg-slate-900/90 border border-cyber-amber text-center hover:border-cyber-amber hover:shadow-[0_0_15px_rgba(255,183,0,0.3)] transition">
                <i class="fa-solid fa-microchip text-cyber-amber mb-1"></i>
                <div class="font-orbitron font-bold text-sm text-slate-200">EMBEDDED</div>
              </div>

            </div>
          </div>

          <!-- Connection Down to Microcontrollers -->
          <div class="flex justify-center mb-6">
            <div class="flex flex-col items-center">
              <div class="w-0.5 h-8 bg-gradient-to-b from-cyber-green to-cyber-amber"></div>
              <i class="fa-solid fa-chevron-down text-cyber-amber text-xs animate-bounce"></i>
            </div>
          </div>

          <!-- Microcontroller Node: ESP32 / ARDUINO / STM32 -->
          <div class="flex justify-center mb-8">
            <div class="node-box p-4 rounded-xl bg-slate-900/95 border border-cyber-amber shadow-[0_0_15px_rgba(255,183,0,0.2)] text-center w-80">
              <div class="text-xs text-slate-400 mb-1 font-mono">MICROCONTROLLER UNITS</div>
              <div class="font-orbitron font-bold text-sm sm:text-base text-cyber-amber tracking-widest flex items-center justify-center space-x-2">
                <span>ESP32</span>
                <span class="text-slate-600">•</span>
                <span>ARDUINO</span>
                <span class="text-slate-600">•</span>
                <span>STM32</span>
              </div>
            </div>
          </div>

          <!-- Split Bus to Bottom Peripherals -->
          <div class="grid grid-cols-3 gap-2 sm:gap-4 max-w-2xl mx-auto relative pt-4 border-t border-dashed border-slate-700">
            
            <div class="text-center p-2.5 rounded bg-slate-900/70 border border-slate-800 hover:border-cyber-green transition">
              <i class="fa-solid fa-temperature-high text-cyber-green text-sm mb-1 block"></i>
              <span class="font-orbitron text-xs font-bold text-slate-300">SENSORS</span>
            </div>

            <div class="text-center p-2.5 rounded bg-slate-900/70 border border-slate-800 hover:border-cyber-pink transition">
              <i class="fa-solid fa-bolt text-cyber-pink text-sm mb-1 block"></i>
              <span class="font-orbitron text-xs font-bold text-slate-300">ACTUATORS</span>
            </div>

            <div class="text-center p-2.5 rounded bg-slate-900/70 border border-slate-800 hover:border-cyber-cyan transition">
              <i class="fa-solid fa-wifi text-cyber-cyan text-sm mb-1 block"></i>
              <span class="font-orbitron text-xs font-bold text-slate-300">NETWORK</span>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- SECTION 3: GITHUB TELEMETRY -->
    <section class="space-y-3">
      <div class="flex items-center space-x-2">
        <i class="fa-brands fa-github text-cyber-green"></i>
        <h2 class="font-orbitron text-sm font-bold tracking-wider text-cyber-green uppercase">
          GITHUB TELEMETRY
        </h2>
        <div class="h-[1px] flex-grow bg-gradient-to-r from-cyber-green/50 to-transparent"></div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- CONTRIBUTION MATRIX Grid -->
        <div class="lg:col-span-2 cyber-hud-card rounded-xl p-5 corner-brackets border-t-2 border-t-cyber-green space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div class="flex items-center space-x-2">
              <i class="fa-solid fa-chart-simple text-cyber-green text-xs"></i>
              <span class="font-orbitron text-xs font-bold text-slate-200">CONTRIBUTION MATRIX</span>
            </div>
            <span class="text-xs text-slate-400">52 WEEKS • LIVE TELEMETRY</span>
          </div>

          <!-- Heatmap Canvas Visualization -->
          <div class="overflow-x-auto pb-2">
            <div id="contribGrid" class="grid grid-flow-col grid-rows-7 gap-1 min-w-[620px]">
              <!-- Grid cells populated dynamically via JavaScript -->
            </div>
          </div>

          <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/60">
            <span>Less Contributions</span>
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-2.5 rounded-sm bg-slate-800 border border-slate-700"></span>
              <span class="w-2.5 h-2.5 rounded-sm bg-emerald-950 border border-emerald-800"></span>
              <span class="w-2.5 h-2.5 rounded-sm bg-emerald-700 border border-emerald-600"></span>
              <span class="w-2.5 h-2.5 rounded-sm bg-emerald-500 border border-emerald-400"></span>
              <span class="w-2.5 h-2.5 rounded-sm bg-cyber-green shadow-[0_0_6px_#00ff66]"></span>
            </div>
            <span>More Contributions</span>
          </div>
        </div>

        <!-- CONTRIBUTION SNAKE Visualizer Box -->
        <div class="cyber-hud-card rounded-xl p-5 corner-brackets border-t-2 border-t-cyber-cyan flex flex-col justify-between space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div class="flex items-center space-x-2">
              <i class="fa-solid fa-staff-snake text-cyber-cyan text-xs"></i>
              <span class="font-orbitron text-xs font-bold text-slate-200">CONTRIBUTION SNAKE</span>
            </div>
            <span class="text-[10px] px-2 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30">AUTONOMOUS</span>
          </div>

          <!-- Interactive Animated Canvas Snake Game / Telemetry Bot -->
          <div class="relative bg-slate-950/80 rounded-lg p-3 border border-slate-800 flex items-center justify-center min-h-[160px]">
            <canvas id="snakeCanvas" width="280" height="120" class="w-full h-auto block rounded"></canvas>
            <div class="absolute bottom-2 right-2 text-[10px] text-slate-500 font-mono">
              BYTES EATEN: <span id="snakeScore" class="text-cyber-green font-bold">0</span>
            </div>
          </div>

          <p class="text-xs text-slate-400 leading-relaxed">
            Neural Snake agent parsing telemetry feeds and harvesting green matrix commits in real-time.
          </p>
        </div>

      </div>
    </section>

    <!-- SECTION 4: DEVELOPER TERMINAL -->
    <section class="space-y-3">
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-square-terminal text-cyber-amber"></i>
        <h2 class="font-orbitron text-sm font-bold tracking-wider text-cyber-amber uppercase">
          DEVELOPER TERMINAL
        </h2>
        <div class="h-[1px] flex-grow bg-gradient-to-r from-cyber-amber/50 to-transparent"></div>
      </div>

      <div class="cyber-hud-card rounded-xl corner-brackets border-t-2 border-t-cyber-amber overflow-hidden">
        
        <!-- Terminal Top Header Bar -->
        <div class="bg-slate-900/90 px-4 py-2.5 border-b border-slate-800 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-red-500/80 inline-block"></span>
            <span class="w-3 h-3 rounded-full bg-yellow-500/80 inline-block"></span>
            <span class="w-3 h-3 rounded-full bg-green-500/80 inline-block"></span>
            <span class="text-xs text-slate-400 ml-2 font-mono">fatih@github:~ (zsh)</span>
          </div>
          <div class="text-xs text-slate-500 font-mono">
            TTY: /dev/pts/0
          </div>
        </div>

        <!-- Terminal Interactive Body -->
        <div id="terminalBody" class="p-6 font-mono text-sm space-y-4 max-h-[480px] overflow-y-auto bg-slate-950/90 text-slate-200">
          
          <!-- Command 1: prompt -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ whoami</span>
            </div>
            <div class="text-cyber-amber pl-4 font-semibold glow-text-amber">> fatih</div>
          </div>

          <!-- Command 2: role -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ role</span>
            </div>
            <div class="text-cyber-green pl-4 font-medium">> AI / IoT / Embedded Systems Developer</div>
          </div>

          <!-- Command 3: hardware -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ hardware</span>
            </div>
            <div class="text-slate-300 pl-4">> ESP32 / ESP8266 / Arduino / STM32 / Raspberry Pi</div>
          </div>

          <!-- Command 4: communication -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ communication</span>
            </div>
            <div class="text-slate-300 pl-4">> MQTT / WiFi / ESP-NOW / HTTP / Serial / I2C / SPI</div>
          </div>

          <!-- Command 5: intelligence -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ intelligence</span>
            </div>
            <div class="text-cyber-purple pl-4 font-medium">> Python / OpenCV / Machine Learning / Computer Vision</div>
          </div>

          <!-- Command 6: software -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ software</span>
            </div>
            <div class="text-cyber-cyan pl-4 font-medium">> React / Vite / Node.js / Laravel / Supabase</div>
          </div>

          <!-- Command 7: status -->
          <div class="space-y-1">
            <div class="text-cyber-cyan flex items-center space-x-2">
              <span class="text-cyber-green font-bold">fatih@github:~$</span>
              <span class="text-slate-100">$ status</span>
            </div>
            <div class="text-cyber-amber pl-4 font-bold animate-pulse">> BUILDING...</div>
          </div>

          <!-- Dynamic Active Line Input -->
          <div id="cliLine" class="flex items-center space-x-2 text-cyber-cyan pt-2">
            <span class="text-cyber-green font-bold">fatih@github:~$</span>
            <span class="text-slate-400">$</span>
            <input type="text" id="cliInput" class="bg-transparent border-none outline-none text-slate-100 flex-grow font-mono focus:ring-0" placeholder="Type 'help' or commands..." autofocus />
            <span class="w-2.5 h-5 bg-cyber-cyan animate-pulse inline-block"></span>
          </div>

        </div>

      </div>
    </section>

    <!-- SECTION 5: ACTIVITY STATUS & NETWORK -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- ACTIVITY STATUS Card -->
      <div class="cyber-hud-card rounded-xl p-6 corner-brackets border-t-2 border-t-cyber-pink flex flex-col justify-between space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-wave-square text-cyber-pink"></i>
            <h2 class="font-orbitron text-xs font-bold tracking-wider text-cyber-pink uppercase">
              ACTIVITY STATUS
            </h2>
          </div>
          <span class="text-xs text-cyber-green flex items-center space-x-1">
            <span class="w-2 h-2 rounded-full bg-cyber-green animate-ping"></span>
            <span>PROCESSING TRANSMISSION</span>
          </span>
        </div>

        <div class="space-y-3 py-2">
          <div class="flex justify-between items-center text-xs">
            <span class="text-slate-400">FIRMWARE COMPILATION</span>
            <span class="text-cyber-cyan">ESP32-S3 Core v2.4</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
            <div class="bg-cyber-cyan h-full rounded-full animate-pulse" style="width: 82%;"></div>
          </div>

          <div class="flex justify-between items-center text-xs">
            <span class="text-slate-400">NEURAL INFERENCE</span>
            <span class="text-cyber-purple">YOLOv8-Nano TensorRT</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
            <div class="bg-cyber-purple h-full rounded-full animate-pulse" style="width: 94%;"></div>
          </div>
        </div>
      </div>

      <!-- NETWORK Card / Banner Box -->
      <div class="cyber-hud-card rounded-xl p-6 corner-brackets border-t-2 border-t-cyber-cyan flex flex-col justify-center text-center space-y-4 relative overflow-hidden group">
        
        <div class="text-xs text-slate-500 font-orbitron tracking-widest uppercase">
          NETWORK // CORE MOTTO
        </div>

        <div class="p-4 rounded-lg bg-slate-950/80 border border-cyber-cyan/30 shadow-[0_0_20px_rgba(0,243,255,0.15)] space-y-3 group-hover:border-cyber-cyan transition duration-500">
          <div class="font-orbitron font-extrabold text-sm sm:text-base text-transparent bg-clip-text bg-gradient-to-r from-cyber-cyan via-cyber-green to-cyber-purple tracking-widest glow-text-cyan">
            BUILD • BREAK • LEARN • REBUILD
          </div>

          <div class="h-[1px] w-1/2 mx-auto bg-gradient-to-r from-transparent via-slate-700 to-transparent"></div>

          <div class="font-orbitron font-bold text-xs sm:text-sm text-slate-300 tracking-wider">
            HARDWARE &nbsp;×&nbsp; SOFTWARE &nbsp;×&nbsp; AI
          </div>
        </div>

      </div>

    </section>

    <!-- Footer -->
    <footer class="text-center py-4 text-xs text-slate-600 border-t border-slate-900">
      <p>© DEVELOPER PROFILE TELEMETRY SYSTEM // ALL MODULES OPERATIONAL</p>
    </footer>

  </div>

  <script>
    /* ==========================================================================
       1. AMBIENT PARTICLE BACKGROUND CANVAS
       ========================================================================== */
    const canvas = document.getElementById('bgCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const particles = [];
    const particleCount = 45;

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        size: Math.random() * 2 + 1,
        color: Math.random() > 0.5 ? '#00f3ff' : '#00ff66'
      });
    }

    function animateParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.fillStyle = p.color;
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        // Connect near particles
        for (let j = i + 1; j < particles.length; j++) {
          let p2 = particles[j];
          let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (dist < 120) {
            ctx.strokeStyle = `rgba(0, 243, 255, ${1 - dist / 120 * 0.8})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(animateParticles);
    }
    animateParticles();

    /* ==========================================================================
       2. WEB AUDIO SYNTH & SOUND EFFECTS
       ========================================================================== */
    let audioCtx = null;
    let soundEnabled = false;

    function toggleAudio() {
      soundEnabled = !soundEnabled;
      const soundIcon = document.getElementById('soundIcon');
      const soundText = document.getElementById('soundText');

      if (soundEnabled) {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        soundIcon.className = 'fa-solid fa-volume-high text-cyber-green';
        soundText.textContent = 'SFX: ON';
        playBeep(880, 0.08); // High cyber chime
      } else {
        soundIcon.className = 'fa-solid fa-volume-xmark';
        soundText.textContent = 'SFX: OFF';
      }
    }

    function playBeep(freq = 440, type = 'sine', duration = 0.05) {
      if (!soundEnabled || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    /* ==========================================================================
       3. INTERACTIVE DEVELOPER TERMINAL CLI
       ========================================================================== */
    const cliInput = document.getElementById('cliInput');
    const terminalBody = document.getElementById('terminalBody');
    const cliLine = document.getElementById('cliLine');

    const COMMAND_RESPONSES = {
      'whoami': '<div class="text-cyber-amber font-semibold font-mono">> fatih</div>',
      'role': '<div class="text-cyber-green font-mono">> AI / IoT / Embedded Systems Developer</div>',
      'hardware': '<div class="text-slate-300 font-mono">> ESP32 / ESP8266 / Arduino / STM32 / Raspberry Pi</div>',
      'communication': '<div class="text-slate-300 font-mono">> MQTT / WiFi / ESP-NOW / HTTP / Serial / I2C / SPI</div>',
      'intelligence': '<div class="text-cyber-purple font-mono">> Python / OpenCV / Machine Learning / Computer Vision</div>',
      'software': '<div class="text-cyber-cyan font-mono">> React / Vite / Node.js / Laravel / Supabase</div>',
      'status': '<div class="text-cyber-amber font-bold animate-pulse font-mono">> BUILDING...</div>',
      'help': '<div class="text-slate-400 font-mono">Available commands: whoami, role, hardware, communication, intelligence, software, status, clear, ping</div>'
    };

    cliInput.addEventListener('keydown', function(e) {
      playBeep(600 + Math.random() * 200, 'triangle', 0.03);

      if (e.key === 'Enter') {
        const cmd = this.value.trim().toLowerCase();
        
        // Echo user command
        const userEcho = document.createElement('div');
        userEcho.className = 'space-y-1';
        userEcho.innerHTML = `
          <div class="text-cyber-cyan flex items-center space-x-2">
            <span class="text-cyber-green font-bold">fatih@github:~$</span>
            <span class="text-slate-100">$ ${this.value}</span>
          </div>
        `;

        if (cmd === 'clear') {
          // Clear custom entries
          terminalBody.querySelectorAll('.custom-entry').forEach(el => el.remove());
          this.value = '';
          return;
        }

        const responseEl = document.createElement('div');
        responseEl.className = 'pl-4 custom-entry';

        if (COMMAND_RESPONSES[cmd]) {
          responseEl.innerHTML = COMMAND_RESPONSES[cmd];
        } else if (cmd === 'ping') {
          responseEl.innerHTML = `<div class="text-cyber-green font-mono">> PONG! Telemetry signal response 12ms. All nodes nominal.</div>`;
        } else if (cmd !== '') {
          responseEl.innerHTML = `<div class="text-red-400 font-mono">> Command not recognized: '${cmd}'. Type 'help' for options.</div>`;
        }

        userEcho.appendChild(responseEl);
        terminalBody.insertBefore(userEcho, cliLine);

        this.value = '';
        terminalBody.scrollTop = terminalBody.scrollHeight;
      }
    });

    /* ==========================================================================
       4. GITHUB CONTRIBUTION MATRIX & AUTONOMOUS SNAKE CANVAS
       ========================================================================== */
    const contribGrid = document.getElementById('contribGrid');
    const cols = 45;
    const rows = 7;
    const cells = [];

    // Colors mapping
    const intensityClasses = [
      'bg-slate-900 border-slate-800',
      'bg-emerald-950 border-emerald-800',
      'bg-emerald-800 border-emerald-700',
      'bg-emerald-600 border-emerald-500',
      'bg-cyber-green border-cyber-green shadow-[0_0_8px_#00ff66]'
    ];

    for (let c = 0; c < cols; c++) {
      for (let r = 0; r < rows; r++) {
        const cell = document.createElement('div');
        const randIntensity = Math.floor(Math.random() * 5);
        cell.className = `w-2.5 h-2.5 rounded-sm border transition-all duration-300 ${intensityClasses[randIntensity]}`;
        contribGrid.appendChild(cell);
        cells.push({ el: cell, level: randIntensity });
      }
    }

    // Snake Canvas Mini Game Bot
    const sCanvas = document.getElementById('snakeCanvas');
    const sCtx = sCanvas.getContext('2d');
    const gridSize = 10;
    let snakeScore = 0;

    let snake = [
      { x: 5, y: 5 },
      { x: 4, y: 5 },
      { x: 3, y: 5 }
    ];
    let food = { x: 15, y: 6 };
    let dx = 1, dy = 0;

    function drawSnakeGame() {
      sCtx.fillStyle = '#0a0f1a';
      sCtx.fillRect(0, 0, sCanvas.width, sCanvas.height);

      // Draw Grid Background lines
      sCtx.strokeStyle = '#1e293b';
      sCtx.lineWidth = 0.5;
      for (let x = 0; x < sCanvas.width; x += gridSize) {
        sCtx.beginPath(); sCtx.moveTo(x, 0); sCtx.lineTo(x, sCanvas.height); sCtx.stroke();
      }
      for (let y = 0; y < sCanvas.height; y += gridSize) {
        sCtx.beginPath(); sCtx.moveTo(0, y); sCtx.lineTo(sCanvas.width, y); sCtx.stroke();
      }

      // Draw Food
      sCtx.fillStyle = '#00f3ff';
      sCtx.shadowBlur = 10;
      sCtx.shadowColor = '#00f3ff';
      sCtx.fillRect(food.x * gridSize + 1, food.y * gridSize + 1, gridSize - 2, gridSize - 2);

      // Draw Snake
      snake.forEach((part, index) => {
        sCtx.fillStyle = index === 0 ? '#00ff66' : '#059669';
        sCtx.shadowBlur = index === 0 ? 8 : 0;
        sCtx.shadowColor = '#00ff66';
        sCtx.fillRect(part.x * gridSize + 1, part.y * gridSize + 1, gridSize - 2, gridSize - 2);
      });

      // Simple AI logic to move towards food
      const head = { x: snake[0].x + dx, y: snake[0].y + dy };

      if (Math.random() < 0.3) {
        if (head.x < food.x) { dx = 1; dy = 0; }
        else if (head.x > food.x) { dx = -1; dy = 0; }
        else if (head.y < food.y) { dx = 0; dy = 1; }
        else if (head.y > food.y) { dx = 0; dy = -1; }
      }

      // Check boundary hit - wrap around
      let newX = snake[0].x + dx;
      let newY = snake[0].y + dy;

      if (newX >= sCanvas.width / gridSize) newX = 0;
      if (newX < 0) newX = Math.floor(sCanvas.width / gridSize) - 1;
      if (newY >= sCanvas.height / gridSize) newY = 0;
      if (newY < 0) newY = Math.floor(sCanvas.height / gridSize) - 1;

      const newHead = { x: newX, y: newY };
      snake.unshift(newHead);

      // Check if food eaten
      if (newX === food.x && newY === food.y) {
        snakeScore += 16;
        document.getElementById('snakeScore').textContent = snakeScore;
        playBeep(1200, 'sine', 0.04);
        food = {
          x: Math.floor(Math.random() * (sCanvas.width / gridSize)),
          y: Math.floor(Math.random() * (sCanvas.height / gridSize))
        };
      } else {
        snake.pop();
      }
    }

    setInterval(drawSnakeGame, 120);

    /* ==========================================================================
       5. REAL-TIME CLOCK & HUD METRICS UPDATE
       ========================================================================== */
    function updateClock() {
      const now = new Date();
      const hrs = String(now.getUTCHours()).padStart(2, '0');
      const mins = String(now.getUTCMinutes()).padStart(2, '0');
      const secs = String(now.getUTCSeconds()).padStart(2, '0');
      document.getElementById('sysClock').textContent = `${hrs}:${mins}:${secs} UTC`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Random Ping Fluctuation
    setInterval(() => {
      const p = Math.floor(10 + Math.random() * 8);
      document.getElementById('pingCounter').textContent = `${p}ms`;
    }, 3000);

  </script>
</body>
</html>
