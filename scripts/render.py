import json
import os

# --- 色彩与设定圣经 ---
COLORS = {
    "bg": "#04060D", "panel": "#0A0F1A", "stroke": "#1B2740",
    "cyan": "#22E1FF", "magenta": "#FF2FA8", "purple": "#8B5CFF",
    "green": "#A8FF5E", "yellow": "#FFC247", "dim": "#6F84A6"
}
WIDTH = 1200
ASSETS_DIR = "assets"

def load_data():
    with open("profile.json", "r", encoding="utf-8") as f: return json.load(f)

# --- SVG 基础骨架构建器 ---
def svg_base(height, content, watermark="00"):
    defs = f"""
    <defs>
        <!-- 泛光滤镜 -->
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="glow-yellow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="glow-magenta" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <!-- 沉浸式渐变遮罩 (用于平滑折线图) -->
        <linearGradient id="grad-cyan" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{COLORS['cyan']}" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="{COLORS['cyan']}" stop-opacity="0.0"/>
        </linearGradient>
        <linearGradient id="grad-magenta" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{COLORS['magenta']}" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="{COLORS['magenta']}" stop-opacity="0.0"/>
        </linearGradient>
        <linearGradient id="grad-green" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{COLORS['green']}" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="{COLORS['green']}" stop-opacity="0.0"/>
        </linearGradient>
        <linearGradient id="grad-yellow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{COLORS['yellow']}" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="{COLORS['yellow']}" stop-opacity="0.0"/>
        </linearGradient>
        <linearGradient id="grad-purple" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{COLORS['purple']}" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="{COLORS['purple']}" stop-opacity="0.0"/>
        </linearGradient>
        
        <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="4" y2="0" stroke="#FFFFFF" stroke-opacity="0.03" stroke-width="1"/>
        </pattern>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <rect width="40" height="40" fill="none" stroke="{COLORS['cyan']}" stroke-opacity="0.03" stroke-width="1"/>
        </pattern>
        <!-- 十六进制内存流底纹 (双副本保证 300px 无缝滚动) -->
        <pattern id="hex-rain" width="300" height="300" patternUnits="userSpaceOnUse">
            <g fill="{COLORS['cyan']}" opacity="0.04" font-size="9" font-family="'JetBrains Mono', Consolas" letter-spacing="2">
                <text x="20" y="20">0x0800 0x1A2B 0x3C4D 0x5E6F</text>
                <text x="80" y="80">0x2000 0xDEAD 0xBEEF 0x0000</text>
                <text x="150" y="140">0x4002 0x8899 0xAABB 0xCCDD</text>
                <text x="40" y="220">0x8000 0x1122 0x3344 0x5566</text>
                <text x="200" y="280">0x0000 0xFFFF 0x0000 0xFFFF</text>
                <text x="20" y="-280">0x0800 0x1A2B 0x3C4D 0x5E6F</text>
                <text x="80" y="-220">0x2000 0xDEAD 0xBEEF 0x0000</text>
                <text x="150" y="-160">0x4002 0x8899 0xAABB 0xCCDD</text>
                <text x="40" y="-80">0x8000 0x1122 0x3344 0x5566</text>
                <text x="200" y="-20">0x0000 0xFFFF 0x0000 0xFFFF</text>
                <animateTransform attributeName="transform" type="translate" from="0,0" to="0,300" dur="20s" repeatCount="indefinite"/>
            </g>
        </pattern>
    </defs>
    """

    # 动态边框 (HUD Viewport) 与 REC 录制指示灯
    hud_frame = f"""
    <!-- 全局微距网格与内存流 -->
    <rect width="{WIDTH}" height="{height}" fill="url(#hex-rain)" />
    <rect width="{WIDTH}" height="{height}" fill="url(#grid)" />
    
    <!-- 取景器物理边框 -->
    <rect x="8" y="8" width="{WIDTH-16}" height="{height-16}" fill="none" stroke="{COLORS['stroke']}" stroke-width="1.5"/>
    <!-- 四角重装甲锁定框 -->
    <path d="M 8,40 L 8,8 L 40,8 M {WIDTH-40},8 L {WIDTH-8},8 L {WIDTH-8},40 M 8,{height-40} L 8,{height-8} L 40,{height-8} M {WIDTH-40},{height-8} L {WIDTH-8},{height-8} L {WIDTH-8},{height-40}" fill="none" stroke="{COLORS['cyan']}" stroke-width="2.5" opacity="0.7"/>
    
    <!-- 顶部状态栏元数据 -->
    <text x="18" y="22" fill="{COLORS['dim']}" font-size="9" letter-spacing="1">SYS.MNTR // LIVE FEED</text>
    <circle cx="{WIDTH-45}" cy="18" r="3.5" fill="{COLORS['magenta']}">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
    </circle>
    <text x="{WIDTH-35}" y="22" fill="{COLORS['magenta']}" font-size="9" font-weight="bold" letter-spacing="1">REC</text>
    <text x="{WIDTH-65}" y="22" fill="{COLORS['dim']}" font-size="9" text-anchor="end">UPLINK_ESTABLISHED</text>
    """

    # 强制覆盖底层属性，禁用 JS
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="100%" height="100%" style="background-color:{COLORS['bg']}; font-family: 'JetBrains Mono', Consolas, 'Microsoft YaHei', sans-serif;">
    {defs}
    <rect width="{WIDTH}" height="{height}" fill="{COLORS['bg']}" />
    <!-- 巨型工业背景水印 -->
    <text x="{WIDTH/2}" y="{height/2 + 100}" fill="#FFFFFF" font-size="{height * 0.8}" font-weight="900" font-family="Arial, Helvetica, sans-serif" opacity="0.02" text-anchor="middle" letter-spacing="-10">{watermark}</text>
    {hud_frame}
    {content}
    <rect width="{WIDTH}" height="{height}" fill="url(#scanlines)" pointer-events="none" />
    </svg>"""

# --- 区块 01: HERO ---
def render_hero(data):
    h = 560
    
    # 顶部状态栏
    top_bar = f"""
    <text x="32" y="40" fill="{COLORS['cyan']}" font-size="12" font-weight="bold" letter-spacing="2">● JASMINE//OS · PROFILE {data['version']}</text>
    <text x="{WIDTH-32}" y="40" fill="{COLORS['dim']}" font-size="12" letter-spacing="1" text-anchor="end">CH1 500mV/div CH2 1V/div RUN &#9656;</text>
    <line x1="24" y1="60" x2="{WIDTH-24}" y2="60" stroke="{COLORS['stroke']}" stroke-width="1" />
    """

    # 巨型文字与故障切片动画 (SMIL)
    glitch_text = f"""
    <g transform="translate(48, 220)">
        <text x="0" y="0" fill="{COLORS['magenta']}" font-size="96" font-weight="700" letter-spacing="-2">
            {data['callsign']}
            <animateTransform attributeName="transform" type="translate" values="4,0; 4,4; -2,-2; 4,0" keyTimes="0; 0.1; 0.2; 1" dur="3.7s" calcMode="discrete" repeatCount="indefinite"/>
        </text>
        <text x="0" y="0" fill="{COLORS['cyan']}" font-size="96" font-weight="700" letter-spacing="-2">
            {data['callsign']}
            <animateTransform attributeName="transform" type="translate" values="-4,0; -4,-4; 2,2; -4,0" keyTimes="0; 0.1; 0.2; 1" dur="5.2s" calcMode="discrete" repeatCount="indefinite"/>
        </text>
        <text x="0" y="0" fill="#FFFFFF" font-size="96" font-weight="700" letter-spacing="-2">{data['callsign']}</text>
    </g>
    """

    # 打字机副标
    typewriter = f"""
    <g transform="translate(52, 280)">
        <clipPath id="type-clip">
            <rect x="0" y="-20" width="0" height="40">
                <animate attributeName="width" from="0" to="600" dur="2.6s" fill="freeze" />
            </rect>
        </clipPath>
        <text x="0" y="0" fill="{COLORS['dim']}" font-size="16" clip-path="url(#type-clip)">&gt; 让电机转准，让代码跑稳，让画面剪好。</text>
        <!-- 闪烁光标 -->
        <rect x="340" y="-14" width="8" height="18" fill="{COLORS['yellow']}">
            <animate attributeName="opacity" values="1;0;1" dur="1.05s" calcMode="discrete" repeatCount="indefinite"/>
        </rect>
    </g>
    """

    # 高级动效：全息三维线框球体 (Holographic Core)
    core = f"""
    <g transform="translate({WIDTH/2}, 420)">
        <text x="0" y="-100" fill="{COLORS['cyan']}" font-size="10" font-weight="bold" letter-spacing="4" text-anchor="middle">QUANTUM CORE // SPATIAL PERCEPTION</text>
        <line x1="-120" y1="-96" x2="120" y2="-96" stroke="{COLORS['stroke']}" stroke-width="1"/>
        
        <!-- 外围光晕脉冲 -->
        <circle cx="0" cy="0" r="75" fill="none" stroke="{COLORS['cyan']}" stroke-width="1" opacity="0.2">
            <animate attributeName="r" values="75; 85; 75" dur="4s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.2; 0; 0.2" dur="4s" repeatCount="indefinite"/>
        </circle>
        
        <!-- 3D 铁线框球体视错觉 -->
        <g stroke="{COLORS['cyan']}" stroke-width="1.5" fill="none" filter="url(#glow-cyan)">
            <ellipse cx="0" cy="0" rx="70" ry="20" opacity="0.6">
                <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>
            </ellipse>
            <ellipse cx="0" cy="0" rx="70" ry="20" opacity="0.8">
                <animateTransform attributeName="transform" type="rotate" from="60" to="420" dur="8s" repeatCount="indefinite"/>
            </ellipse>
            <ellipse cx="0" cy="0" rx="70" ry="20" opacity="0.4">
                <animateTransform attributeName="transform" type="rotate" from="120" to="480" dur="8s" repeatCount="indefinite"/>
            </ellipse>
        </g>
        
        <!-- 核心计算内核 (品红色转子) -->
        <path d="M 0,-30 L 26,15 L -26,15 Z" fill="none" stroke="{COLORS['magenta']}" stroke-width="2" filter="url(#glow-magenta)">
             <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="4s" repeatCount="indefinite"/>
        </path>
        <circle cx="0" cy="0" r="5" fill="{COLORS['yellow']}" filter="url(#glow-cyan)">
            <animate attributeName="opacity" values="1;0.5;1" dur="1s" repeatCount="indefinite"/>
        </circle>
    </g>
    """

    # 左右两侧的微型频谱仪 (Spectrum Visualizer)
    def make_spectrum(x, y, is_left):
        bars = ""
        for i in range(16):
            height = 10 + (i * 7 % 30) if is_left else 10 + ((15-i) * 11 % 30)
            bars += f"""
            <rect x="{i*12}" y="{-height}" width="6" height="{height}" fill="{COLORS['dim']}">
                <animate attributeName="height" values="{height}; {height*0.2}; {height}" dur="{0.5 + (i%3)*0.2}s" repeatCount="indefinite"/>
                <animate attributeName="y" values="{-height}; {-height*0.2}; {-height}" dur="{0.5 + (i%3)*0.2}s" repeatCount="indefinite"/>
            </rect>
            """
        title = "SYS.MEM" if is_left else "NET.TX/RX"
        return f'<g transform="translate({x}, {y})"><text x="0" y="20" fill="{COLORS["dim"]}" font-size="9" letter-spacing="1">{title}</text>{bars}</g>'

    waveforms = core + make_spectrum(100, 460, True) + make_spectrum(WIDTH - 300, 460, False)
    
    return svg_base(h, top_bar + glitch_text + typewriter + waveforms, "01")

# --- 区块 03: WHOAMI ---
def render_whoami(data):
    h = 344
    content = f"""
    <!-- 左侧终端面板 -->
    <rect x="24" y="24" width="680" height="{h-48}" rx="12" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
    <circle cx="44" cy="44" r="5" fill="{COLORS['magenta']}"/>
    <circle cx="60" cy="44" r="5" fill="{COLORS['yellow']}"/>
    <circle cx="76" cy="44" r="5" fill="{COLORS['green']}"/>
    <text x="364" y="48" fill="{COLORS['dim']}" font-size="12" text-anchor="middle">jasmine@os: ~</text>
    <line x1="24" y1="64" x2="704" y2="64" stroke="{COLORS['stroke']}" stroke-width="1"/>
    
    <g font-size="14" transform="translate(44, 96)">
        <text y="0" fill="{COLORS['green']}">$ <tspan fill="#FFF">whoami</tspan></text>
        <text y="24" fill="{COLORS['dim']}">{data['callsign']}  ·  {data['roles'][0]} / {data['roles'][1]}</text>
        
        <text y="64" fill="{COLORS['green']}">$ <tspan fill="#FFF">cat focus.txt</tspan></text>
        <text y="88" fill="{COLORS['dim']}">{data['focus']}</text>
        
        <text y="128" fill="{COLORS['green']}">$ <tspan fill="#FFF">ls ~/lab</tspan></text>
        <text y="152" fill="{COLORS['cyan']}">{ '   '.join(data['dirs']) }</text>
        
        <text y="192" fill="{COLORS['green']}">$ <tspan fill="#FFF">git log -1 --oneline</tspan></text>
        <text y="216" fill="{COLORS['dim']}"><tspan fill="{COLORS['yellow']}">9c1f2ab</tspan> polish: PWM jitter 12us -&gt; 2us</text>
    </g>
    """

    log_panel = f'<rect x="728" y="24" width="228" height="{h-48}" rx="12" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>'

    logs = [
        "[ 0.00] jasmine_os boot", 
        "[ 0.04] mcu_core: OK", 
        "[ 0.08] bus_init: OK", 
        "[ 0.12] ros2_node: ONLINE",
        "[ 0.16] qwen2.5: STANDBY",
        "[ 0.24] fs_mount: /lab OK",
        "[ 0.28] -------------",
        "[ 0.32] init: haloflux.js",
        "[ 0.36] ready for input_"
    ]
    log_text = f'<g font-size="12" transform="translate(740, 60)" fill="{COLORS["dim"]}">'
    for i, log in enumerate(logs):
        color = COLORS['green'] if "ONLINE" in log or "ready" in log else (COLORS['yellow'] if "STANDBY" in log else COLORS['dim'])
        log_text += f'<text y="{i*24}" fill="{color}" opacity="0">{log}<animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{i*0.15}s" fill="freeze" /></text>'
    log_text += "</g>"

    log_meta = f"""
    <text x="740" y="48" fill="{COLORS['dim']}" font-size="8" letter-spacing="1">BOOT.LOG // KERNEL</text>
    <line x1="740" y1="288" x2="944" y2="288" stroke="{COLORS['stroke']}" stroke-width="1"/>
    <text x="740" y="302" fill="{COLORS['dim']}" font-size="8" letter-spacing="1">BUFFER 09/256 // ERR 0</text>
    """

    # --- HALOFLUX AI 代理监控拓扑 ---
    haloflux = f"""
    <g transform="translate(972, 24)">
        <rect x="0" y="0" width="204" height="{h-48}" rx="12" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
        <text x="12" y="24" fill="{COLORS['cyan']}" font-size="10" font-weight="bold">AGENT // HALOFLUX</text>
        <line x1="12" y1="32" x2="192" y2="32" stroke="{COLORS['stroke']}" stroke-width="1"/>
        
        <!-- GLM-5.3 WS/SSE 流式节点模型 -->
        <circle cx="102" cy="110" r="30" fill="none" stroke="{COLORS['magenta']}" stroke-width="1" stroke-dasharray="2 4">
             <animateTransform attributeName="transform" type="rotate" from="0 102 110" to="360 102 110" dur="10s" repeatCount="indefinite"/>
        </circle>
        <circle cx="102" cy="110" r="15" fill="{COLORS['bg']}" stroke="{COLORS['magenta']}" stroke-width="2" filter="url(#glow-magenta)"/>
        <text x="102" y="113" fill="#FFFFFF" font-size="9" font-weight="bold" text-anchor="middle">GLM</text>
        
        <!-- DOM-Canvas 混合渲染数据流 -->
        <path d="M 102,140 L 102,190" fill="none" stroke="{COLORS['cyan']}" stroke-width="1.5" stroke-dasharray="4 4">
            <animate attributeName="stroke-dashoffset" from="16" to="0" dur="1s" repeatCount="indefinite"/>
        </path>
        <rect x="52" y="190" width="100" height="30" rx="4" fill="none" stroke="{COLORS['cyan']}" stroke-width="1"/>
        <text x="102" y="209" fill="{COLORS['cyan']}" font-size="9" text-anchor="middle">DOM/CANVAS SYNC</text>
        <text x="102" y="245" fill="{COLORS['dim']}" font-size="8" letter-spacing="1" text-anchor="middle">60FPS // HYBRID</text>
        
        <circle cx="16" cy="270" r="3" fill="{COLORS['green']}"><animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>
        <text x="26" y="273" fill="{COLORS['dim']}" font-size="9">WS/SSE: CONNECTED</text>
    </g>
    """

    return svg_base(h, content + log_panel + log_meta + log_text + haloflux, "03")

# --- 区块 08: FOOTER ---
def render_footer(data):
    h = 210
    content = f"""
    <!-- 中心花朵与旋转光环 -->
    <g transform="translate(600, 80)">
        <circle cx="0" cy="0" r="40" fill="none" stroke="{COLORS['stroke']}" stroke-width="2" stroke-dasharray="8 8">
            <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="20s" repeatCount="indefinite"/>
        </circle>
        <circle cx="0" cy="0" r="3" fill="{COLORS['yellow']}" filter="url(#glow-cyan)">
            <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>
        </circle>
        <!-- 极简花瓣 -->
        <path d="M0,-5 Q15,-20 0,-30 Q-15,-20 0,-5 M4,-2 Q18,-5 25,5 Q15,15 4,-2 M-4,-2 Q-18,-5 -25,5 Q-15,15 -4,-2 M3,4 Q10,18 0,25 Q-10,18 -3,4" fill="none" stroke="{COLORS['cyan']}" stroke-width="1.5" />
    </g>
    
    <line x1="24" y1="80" x2="520" y2="80" stroke="{COLORS['stroke']}" stroke-width="1" />
    <line x1="680" y1="80" x2="{WIDTH-24}" y2="80" stroke="{COLORS['stroke']}" stroke-width="1" />
    
    <text x="600" y="160" fill="{COLORS['dim']}" font-size="14" letter-spacing="2" text-anchor="middle">{data['motto'].upper()}</text>
    <text x="600" y="180" fill="{COLORS['stroke']}" font-size="12" letter-spacing="1" text-anchor="middle">&lt; EOF /&gt;</text>
    """
    return svg_base(h, content, "08")

# --- 区块 02: TELEMETRY ---
def render_telemetry(data):
    import math
    h = 240

    # 尝试加载真实抓取的 GitHub 遥测数据
    real_data = {}
    try:
        import json, os
        if os.path.exists("data/github.json"):
            with open("data/github.json", "r", encoding="utf-8") as f:
                gh_raw = json.load(f)
                real_data = {
                    "followers": gh_raw.get("followers"),
                    "repos": gh_raw.get("public_repos"),
                    "following": gh_raw.get("following"),
                    "stars": gh_raw.get("total_stars"),
                    "commits": gh_raw.get("commits_ytd"),
                }
    except Exception as e:
        print(f"[-] Telemetry sensor offline, showing placeholders. ({e})")

    def present(value):
        return value if isinstance(value, (int, float)) else "--"

    has_live_data = any(
        isinstance(real_data.get(key), (int, float))
        for key in ("followers", "repos", "following", "stars", "commits")
    )
    status = "LIVE" if has_live_data else "OFFLINE"

    # 顶部微型坐标系刻度 (Micro Rulers)
    ruler = ""
    for i in range(24, WIDTH-24, 20):
        tick = 16 if i % 100 == 24 else 14
        ruler += f'<line x1="{i}" y1="12" x2="{i}" y2="{tick}" stroke="{COLORS["dim"]}" stroke-width="1"/>'

    header = f"""
    <text x="24" y="38" fill="{COLORS['dim']}" font-size="8" letter-spacing="1">SYS.TELEMETRY // 30D_WINDOW</text>
    <text x="{WIDTH-24}" y="38" fill="{COLORS['dim']}" font-size="8" letter-spacing="1" text-anchor="end">SRC: GITHUB_REST // {status}</text>
    """

    # Grafana 风格水平数据条生成器
    def make_bar(x, y, w, title, value, max_val, color):
        numeric = isinstance(value, (int, float))
        percent = min(1.0, value / max_val) if numeric and max_val > 0 else 0
        fill_w = w * percent
        display = value if numeric else "--"
        
        return f"""
        <g transform="translate({x}, {y})">
            <!-- 标题与数据值 -->
            <text x="0" y="0" fill="{COLORS['dim']}" font-size="12" font-weight="bold" letter-spacing="1">{title}</text>
            <text x="{w}" y="0" fill="#FFFFFF" font-size="12" font-family="'JetBrains Mono', Consolas" font-weight="bold" text-anchor="end">{display}</text>
            <!-- 底槽 -->
            <rect x="0" y="8" width="{w}" height="4" fill="{COLORS['stroke']}" rx="2"/>
            <!-- 动态数据条 -->
            <rect x="0" y="8" width="0" height="4" fill="{color}" rx="2">
                <animate attributeName="width" from="0" to="{fill_w}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
            </rect>
            <!-- 尾部跟随发光点 -->
            <circle cx="0" cy="10" r="2" fill="#FFF" filter="url(#glow-cyan)">
                <animate attributeName="cx" from="0" to="{fill_w}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
            </circle>
        </g>
        """

    # 底部微型波形图 (平滑贝塞尔曲线 + 渐变光影)
    def make_sparkline(x, y, color, grad_id, smooth_path):
        return f"""
        <g transform="translate({x}, {y})">
            <!-- 曲线主体 -->
            <path d="{smooth_path}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <!-- 底部渐变光影遮罩 -->
            <path d="{smooth_path} L 120,25 L 0,25 Z" fill="url(#{grad_id})"/>
            <!-- 扫描光栅 (跑马灯动效) -->
            <line x1="0" y1="0" x2="0" y2="25" stroke="#FFFFFF" stroke-width="1" opacity="0.5">
                <animate attributeName="x1" values="0; 120; 0" dur="3s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
                <animate attributeName="x2" values="0; 120; 0" dur="3s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
            </line>
        </g>
        """

    # --- 六维能力雷达图 ---
    def make_radar(cx, cy, radius, scores):
        labels = ["FIRMWARE", "ROBOTICS", "AI_VISION", "WEB_DEV", "OPEN_SRC", "ACTIVITY"]
        angles = [i * (math.pi / 3) - (math.pi / 2) for i in range(6)]

        grid = ""
        for r in [radius*0.33, radius*0.66, radius]:
            pts = " ".join([f"{cx + r * math.cos(a)},{cy + r * math.sin(a)}" for a in angles])
            grid += f'<polygon points="{pts}" fill="none" stroke="{COLORS["stroke"]}" stroke-width="1"/>'
        for a in angles:
            grid += f'<line x1="{cx}" y1="{cy}" x2="{cx + radius * math.cos(a)}" y2="{cy + radius * math.sin(a)}" stroke="{COLORS["stroke"]}" stroke-width="1"/>'

        data_pts = " ".join([f"{cx + (radius * s) * math.cos(a)},{cy + (radius * s) * math.sin(a)}" for s, a in zip(scores, angles)])
        data_poly = f"""
        <polygon points="{data_pts}" fill="{COLORS['cyan']}" fill-opacity="0.2" stroke="{COLORS['cyan']}" stroke-width="2" filter="url(#glow-cyan)">
            <animate attributeName="fill-opacity" values="0.1;0.3;0.1" dur="4s" repeatCount="indefinite"/>
        </polygon>
        """

        nodes = ""
        for i, (s, a) in enumerate(zip(scores, angles)):
            px, py = cx + (radius * s) * math.cos(a), cy + (radius * s) * math.sin(a)
            lx, ly = cx + (radius + 25) * math.cos(a), cy + (radius + 15) * math.sin(a)
            nodes += f'<circle cx="{px}" cy="{py}" r="3" fill="#FFF"/>'
            anchor = "middle" if i == 0 or i == 3 else ("start" if i == 1 or i == 2 else "end")
            nodes += f'<text x="{lx}" y="{ly+4}" fill="{COLORS["dim"]}" font-size="10" text-anchor="{anchor}">{labels[i]}</text>'

        return grid + data_poly + nodes

    # 左侧数据条 + 中部雷达图
    bars = [
        make_bar(40, 50, 220, "NET.FOLLOWERS", present(real_data.get("followers")), 20, COLORS['cyan']),
        make_bar(40, 90, 220, "REPO.PUBLIC", present(real_data.get("repos")), 20, COLORS['magenta']),
        make_bar(40, 130, 220, "NET.FOLLOWING", present(real_data.get("following")), 20, COLORS['green']),
        make_bar(320, 50, 220, "RUNTIME.STARS", present(real_data.get("stars")), 50, COLORS['yellow']),
        make_bar(320, 90, 220, "COMMITS.YTD", present(real_data.get("commits")), 100, COLORS['purple'])
    ]

    smooth_paths = [
        "M 0,15 Q 10,5 20,12 T 40,8 T 60,18 T 80,5 T 100,12 T 120,8",
        "M 0,12 Q 10,18 20,10 T 40,16 T 60,6 T 80,14 T 100,4 T 120,10",
        "M 0,17 Q 10,8 20,14 T 40,5 T 60,16 T 80,7 T 100,18 T 120,6",
        "M 0,10 Q 10,16 20,7 T 40,14 T 60,3 T 80,11 T 100,6 T 120,13",
        "M 0,14 Q 10,6 20,16 T 40,9 T 60,4 T 80,18 T 100,7 T 120,12",
    ]
    spark_x = [40, 170, 300, 430, 560]
    spark_colors = [COLORS['cyan'], COLORS['magenta'], COLORS['green'], COLORS['yellow'], COLORS['purple']]
    spark_grads = ["grad-cyan", "grad-magenta", "grad-green", "grad-yellow", "grad-purple"]
    sparklines = [
        make_sparkline(x, 170, color, grad, path)
        for x, color, grad, path in zip(spark_x, spark_colors, spark_grads, smooth_paths)
    ]

    spark_label = f"""
    <text x="40" y="158" fill="{COLORS['dim']}" font-size="8" letter-spacing="1">ACTIVITY.SPARK // 30D</text>
    <text x="680" y="158" fill="{COLORS['dim']}" font-size="8" letter-spacing="1" text-anchor="end">CH1..CH5</text>
    """
    spark_baseline = f'<line x1="40" y1="195" x2="680" y2="195" stroke="{COLORS["stroke"]}" stroke-width="1"/>'
    bus_note = f'<text x="320" y="138" fill="{COLORS["dim"]}" font-size="8" letter-spacing="1">BUS.0x02 // SAMPLE 1Hz</text>'

    radar_scores = [0.95, 0.85, 0.70, 0.90, 0.60, 0.80]
    radar = make_radar(880, 120, 75, radar_scores)

    return svg_base(h, ruler + header + "".join(bars) + bus_note + spark_label + "".join(sparklines) + spark_baseline + radar, "02")

# --- 区块 04: TOOLCHAIN ---
def render_toolchain(data):
    h = 340

    # 工业图纸风格底纹 (十字对齐线 + 极小字号工程批号)
    bg = f"""
    <path d="M 24,20 L 34,20 M 24,20 L 24,30 M {WIDTH-24},20 L {WIDTH-34},20 M {WIDTH-24},20 L {WIDTH-24},30" fill="none" stroke="{COLORS['dim']}" stroke-width="1"/>
    <text x="64" y="40" fill="{COLORS['dim']}" font-size="10" font-weight="bold" letter-spacing="2">SYS.ARCH // ORTHOGONAL PCB ROUTING</text>
    <text x="{WIDTH-32}" y="40" fill="{COLORS['dim']}" font-size="8" text-anchor="end">JASMINE_SOC_REV_2.6</text>
    <line x1="24" y1="48" x2="{WIDTH-24}" y2="48" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="4 2"/>
    """

    # 正交 45 度 PCB 走线 + 流动数据包
    def make_trace(path_d, color, duration):
        glow = "glow-cyan"
        if color == COLORS['yellow']:
            glow = "glow-yellow"
        elif color == COLORS['magenta']:
            glow = "glow-magenta"
        return f"""
        <g>
            <path d="{path_d}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <circle r="2" fill="#FFFFFF" filter="url(#{glow})">
                <animateMotion dur="{duration}s" repeatCount="indefinite" path="{path_d}"/>
            </circle>
        </g>
        """

    # 精准对齐方块边缘 (300/900) 与芯片边缘 (570/630)
    bus_lines = f"""
    {make_trace('M 570,145 L 530,145 L 475,90 L 300,90', COLORS['cyan'], 1.2)}
    {make_trace('M 570,160 L 530,160 L 500,190 L 300,190', COLORS['yellow'], 1.5)}
    {make_trace('M 570,175 L 540,175 L 540,270 L 520,290 L 300,290', COLORS['yellow'], 1.8)}
    {make_trace('M 630,145 L 670,145 L 707.5,107.5 L 900,107.5', COLORS['magenta'], 1.3)}
    {make_trace('M 630,175 L 670,175 L 727.5,232.5 L 900,232.5', COLORS['green'], 1.6)}
    """

    # 中央主控 IC 芯片图示
    pins = ""
    for i in range(10):
        pins += f'<line x1="{575+i*5}" y1="135" x2="{575+i*5}" y2="140" stroke="{COLORS["dim"]}" stroke-width="1.5"/>'
        pins += f'<line x1="{575+i*5}" y1="180" x2="{575+i*5}" y2="185" stroke="{COLORS["dim"]}" stroke-width="1.5"/>'
        pins += f'<line x1="565" y1="{145+i*3.5}" x2="570" y2="{145+i*3.5}" stroke="{COLORS["dim"]}" stroke-width="1.5"/>'
        pins += f'<line x1="630" y1="{145+i*3.5}" x2="635" y2="{145+i*3.5}" stroke="{COLORS["dim"]}" stroke-width="1.5"/>'

    central_chip = f"""
    <g>
        {pins}
        <rect x="570" y="140" width="60" height="40" fill="{COLORS['bg']}" stroke="{COLORS['cyan']}" stroke-width="2"/>
        <circle cx="578" cy="148" r="2" fill="{COLORS['yellow']}"/>
        <text x="600" y="158" fill="{COLORS['cyan']}" font-size="8" font-weight="bold" text-anchor="middle">JASMINE</text>
        <text x="600" y="170" fill="{COLORS['dim']}" font-size="7" font-weight="bold" text-anchor="middle">SOC V2.6</text>
    </g>
    """

    # 工业内存块生成器
    def make_block(x, y, w, h, label, sub_labels, color, hex_addr):
        subs = "".join([
            f'<text x="{x+10}" y="{y+42+(idx*16)}" fill="{COLORS["dim"]}" font-size="11">- {sub}</text>'
            for idx, sub in enumerate(sub_labels)
        ])

        return f"""
        <g>
            <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{COLORS['panel']}" stroke="{color}" stroke-width="1"/>
            <rect x="{x}" y="{y}" width="{w}" height="22" fill="{color}" fill-opacity="0.15"/>
            <text x="{x+10}" y="{y+15}" fill="{color}" font-size="12" font-weight="bold">{label}</text>
            <text x="{x+w-10}" y="{y+15}" fill="{color}" font-size="10" font-family="'JetBrains Mono', Consolas" text-anchor="end">{hex_addr}</text>
            <circle cx="{x+w if x < 600 else x}" cy="{y+h/2}" r="3" fill="{COLORS['bg']}" stroke="{color}" stroke-width="1.5"/>
            {subs}
            <line x1="{x+10}" y1="{y+h-10}" x2="{x+w-10}" y2="{y+h-10}" stroke="{color}" stroke-opacity="0.4" stroke-width="2"/>
        </g>
        """

    blocks = [
        make_block(80, 55, 220, 70, "MCU_CORE", ["STM32 / ESP32 / FreeRTOS"], COLORS['cyan'], "0x0800"),
        make_block(80, 155, 220, 70, "PERIPHERALS", ["I2C/SPI / UART / RS485 / PWM"], COLORS['yellow'], "0x4000"),
        make_block(80, 255, 220, 70, "MOTION_CTRL", ["ROS2 Humble / Nav2 / SLAM"], COLORS['yellow'], "0x4002"),
        make_block(900, 55, 220, 105, "AI_VISION", ["YOLOv8 / YOLOv11", "Qwen2.5-VL / Ollama", "OpenCV / RealSense D435"], COLORS['magenta'], "0x6000"),
        make_block(900, 180, 220, 105, "WEB_PORTAL", ["Vue3 + Element Plus", "Django REST Framework", "Next.js / 3D Canvas"], COLORS['green'], "0x8000")
    ]

    return svg_base(h, bg + bus_lines + central_chip + "".join(blocks), "04")

# --- 区块 05: BUILDS ---
def render_builds(data):
    h = 240
    content = f'<text x="64" y="40" fill="{COLORS["dim"]}" font-size="12" font-weight="bold" letter-spacing="2">ACCESSING_RECORDS // BUILDS</text>'

    def make_card(x, y, build):
        w = 360
        card_h = 160

        # 全息激光扫描线动效 (Holo-Scanner)
        scanner = f"""
        <g opacity="0.7">
            <rect x="0" y="0" width="{w}" height="40" fill="{COLORS['cyan']}" fill-opacity="0.12" filter="url(#glow-cyan)">
                <animate attributeName="y" values="0; {card_h-40}; 0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
            </rect>
            <line x1="0" y1="0" x2="{w}" y2="0" stroke="{COLORS['cyan']}" stroke-width="2" filter="url(#glow-cyan)">
                <animate attributeName="y1" values="0; {card_h}; 0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
                <animate attributeName="y2" values="0; {card_h}; 0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>
            </line>
        </g>
        """

        return f"""
        <g transform="translate({x}, {y})">
            <rect x="0" y="0" width="{w}" height="{card_h}" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>

            <path d="M -5,-5 L 10,-5 M -5,-5 L -5,10" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M {w+5},-5 L {w-10},-5 M {w+5},-5 L {w+5},10" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M -5,{card_h+5} L 10,{card_h+5} M -5,{card_h+5} L -5,{card_h-10}" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M {w+5},{card_h+5} L {w-10},{card_h+5} M {w+5},{card_h+5} L {w+5},{card_h-10}" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>

            <clipPath id="clip-{build['id']}">
                <rect x="0" y="0" width="{w}" height="{card_h}" />
            </clipPath>
            <g clip-path="url(#clip-{build['id']})">
                {scanner}
            </g>

            <rect x="0" y="0" width="{w}" height="4" fill="{COLORS['purple']}"/>
            <text x="16" y="35" fill="{COLORS['yellow']}" font-size="20" font-family="'JetBrains Mono', Consolas" font-weight="900">[{build['id']}]</text>
            <text x="70" y="32" fill="{COLORS['dim']}" font-size="10" font-weight="bold">{build['lang'].upper()}</text>
            <circle cx="{w-20}" cy="24" r="4" fill="{COLORS['green']}">
                <animate attributeName="opacity" values="1;0.2;1" dur="{2 + int(build['id'])*0.5}s" repeatCount="indefinite"/>
            </circle>

            <text x="16" y="75" fill="#FFFFFF" font-size="22" font-weight="900" letter-spacing="1">{build['codename']}</text>
            <text x="16" y="105" fill="{COLORS['cyan']}" font-size="13">{build['desc'][0]}</text>
            <text x="16" y="130" fill="{COLORS['cyan']}" font-size="13">{build['desc'][1]}</text>
            <line x1="16" y1="145" x2="{w-16}" y2="145" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="2 2"/>
        </g>
        """

    start_x = (WIDTH - (360 * 3 + 40 * 2)) / 2
    for i, build in enumerate(data['builds']):
        content += make_card(start_x + i * 400, 50, build)
        
    return svg_base(h, content, "05")

if __name__ == "__main__":
    os.makedirs(ASSETS_DIR, exist_ok=True)
    data = load_data()
    
    with open(f"{ASSETS_DIR}/01_hero.svg", "w", encoding="utf-8") as f: f.write(render_hero(data))
    
    # 替换这三行，调用新写的高级函数
    with open(f"{ASSETS_DIR}/02_telemetry.svg", "w", encoding="utf-8") as f: f.write(render_telemetry(data))
    with open(f"{ASSETS_DIR}/03_whoami.svg", "w", encoding="utf-8") as f: f.write(render_whoami(data))
    with open(f"{ASSETS_DIR}/04_toolchain.svg", "w", encoding="utf-8") as f: f.write(render_toolchain(data))
    with open(f"{ASSETS_DIR}/05_builds.svg", "w", encoding="utf-8") as f: f.write(render_builds(data))
    
    with open(f"{ASSETS_DIR}/08_footer.svg", "w", encoding="utf-8") as f: f.write(render_footer(data))
    
    print("Advanced SVG assets successfully rendered.")
