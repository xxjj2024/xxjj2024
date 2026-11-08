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
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="glow-magenta" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="4" y2="0" stroke="#FFFFFF" stroke-opacity="0.04" stroke-width="1"/>
        </pattern>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <rect width="40" height="40" fill="none" stroke="{COLORS['cyan']}" stroke-opacity="0.04" stroke-width="1"/>
        </pattern>
    </defs>
    """
    # 强制覆盖底层属性，禁用 JS
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="100%" height="100%" style="background-color:{COLORS['bg']}; font-family: 'JetBrains Mono', Consolas, 'Microsoft YaHei', sans-serif;">
    {defs}
    <rect width="{WIDTH}" height="{height}" fill="{COLORS['bg']}" />
    <!-- 巨型工业背景水印 -->
    <text x="{WIDTH/2}" y="{height/2 + 100}" fill="#FFFFFF" font-size="{height * 0.8}" font-weight="900" font-family="Arial, Helvetica, sans-serif" opacity="0.02" text-anchor="middle" letter-spacing="-10">{watermark}</text>
    <rect width="{WIDTH}" height="{height}" fill="url(#grid)" />
    {content}
    <rect width="{WIDTH}" height="{height}" fill="url(#scanlines)" pointer-events="none" />
    
    <!-- HUD Corners -->
    <path d="M 14,0 L 0,0 L 0,14 M {WIDTH-14},0 L {WIDTH},0 L {WIDTH},14 M {WIDTH-14},{height} L {WIDTH},{height} L {WIDTH},{height-14} M 14,{height} L 0,{height} L 0,{height-14}" fill="none" stroke="{COLORS['stroke']}" stroke-width="2" />
    <!-- Calibration Crosshairs -->
    <path d="M 40,24 L 48,24 M 44,20 L 44,28" fill="none" stroke="{COLORS['dim']}" stroke-width="1.5"/>
    <path d="M {WIDTH-48},24 L {WIDTH-40},24 M {WIDTH-44},20 L {WIDTH-44},28" fill="none" stroke="{COLORS['dim']}" stroke-width="1.5"/>
    <path d="M 40,{height-12} L 48,{height-12} M 44,{height-16} L 44,{height-8}" fill="none" stroke="{COLORS['dim']}" stroke-width="1.5"/>
    <path d="M {WIDTH-48},{height-12} L {WIDTH-40},{height-12} M {WIDTH-44},{height-16} L {WIDTH-44},{height-8}" fill="none" stroke="{COLORS['dim']}" stroke-width="1.5"/>
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

    # 高级动效：干涉波阵列 (Interference Waves)
    waveforms = f"""
    <g transform="translate(0, 420)">
        <line x1="24" y1="0" x2="{WIDTH-400}" y2="0" stroke="{COLORS['yellow']}" stroke-width="1" stroke-dasharray="2 4" />
        <text x="32" y="-8" fill="{COLORS['yellow']}" font-size="10" letter-spacing="1">PHASE.SYNC // LISSAJOUS RESONANCE</text>
        
        <!-- 主载波 (Cyan) -->
        <g stroke="{COLORS['cyan']}" stroke-width="1.5" fill="none" filter="url(#glow-cyan)">
            <path d="M0,0 Q50,-50 100,0 T200,0 T300,0 T400,0 T500,0 T600,0 T700,0 T800,0 T900,0 T1000,0">
                <animateTransform attributeName="transform" type="translate" from="0,0" to="-200,0" dur="4s" repeatCount="indefinite" />
            </path>
        </g>
        <!-- 副频波 (Magenta, 逆向) -->
        <g stroke="{COLORS['magenta']}" stroke-width="1" fill="none" opacity="0.6">
            <path d="M-200,0 Q-150,30 -100,0 T0,0 T100,0 T200,0 T300,0 T400,0 T500,0 T600,0 T700,0 T800,0 T900,0 T1000,0">
                <animateTransform attributeName="transform" type="translate" from="0,0" to="200,0" dur="6s" repeatCount="indefinite" />
            </path>
        </g>
        <!-- 扫频扫描线 -->
        <line x1="200" y1="-60" x2="200" y2="60" stroke="#FFFFFF" stroke-width="1" opacity="0.5">
            <animate attributeName="x1" values="50; 800; 50" dur="8s" repeatCount="indefinite"/>
            <animate attributeName="x2" values="50; 800; 50" dur="8s" repeatCount="indefinite"/>
        </line>
    </g>
    """

    # 高级动效：右下角三维轨道陀螺仪 (Orbital Gyroscope)
    gyro = f"""
    <g transform="translate({WIDTH - 200}, 420)">
        <text x="0" y="-85" fill="{COLORS['dim']}" font-size="10" font-weight="bold" text-anchor="middle">TARGET_LOCK</text>
        <!-- 外层刻度慢速顺时针 -->
        <circle cx="0" cy="0" r="70" fill="none" stroke="{COLORS['stroke']}" stroke-width="6" stroke-dasharray="2 8">
            <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/>
        </circle>
        <!-- 中层瞄准环快速逆时针 -->
        <circle cx="0" cy="0" r="55" fill="none" stroke="{COLORS['cyan']}" stroke-width="2" stroke-dasharray="10 20 40 10 5 15" filter="url(#glow-cyan)">
            <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="12s" repeatCount="indefinite"/>
        </circle>
        <!-- 内层能量环脉冲 -->
        <circle cx="0" cy="0" r="40" fill="none" stroke="{COLORS['magenta']}" stroke-width="1.5" stroke-dasharray="40 80" filter="url(#glow-magenta)">
            <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>
        </circle>
        <!-- 核心十字准心 -->
        <path d="M -15,0 L 15,0 M 0,-15 L 0,15" fill="none" stroke="{COLORS['yellow']}" stroke-width="1"/>
        <circle cx="0" cy="0" r="3" fill="{COLORS['yellow']}" filter="url(#glow-cyan)">
             <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>
        </circle>
    </g>
    """
    
    return svg_base(h, top_bar + glitch_text + typewriter + waveforms + gyro, "01")

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

    <!-- 右侧 Boot Log 面板 (逐渐亮起) -->
    <rect x="728" y="24" width="448" height="{h-48}" rx="12" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
    <g font-size="14" transform="translate(748, 64)" fill="{COLORS['dim']}">
    """
    logs = [
        "[ 0.000] system boot: JASMINE//OS v2.6.1_PROD", 
        "[ 0.041] mcu_core: cortex-m4 @ 168MHz ... [OK]", 
        "[ 0.082] bus_init: i2c1, spi2, uart4    ... [OK]", 
        "[ 0.123] motion_sys: ros2_humble node  ... [ONLINE]",
        "[ 0.164] vision_ai: qwen2.5-vl loaded   ... [STANDBY]",
        "[ 0.205] fs_mount: /dev/sda1 -> /lab   ... [OK]",
        "[ 0.246] ---------------------------------------",
        "[ 0.287] proc_spawn: haloflux_agent_monitor.js", 
        "[ 0.328] ws_stream: connected to model [glm-5.3]",
        "[ 0.369] dom_canvas: hybrid render sync ... [ACTIVE]",
        "[ 0.410] ready for command input_"
    ]
    for i, log in enumerate(logs):
        if "ready" in log or any(tag in log for tag in ("[OK]", "[ONLINE]", "[ACTIVE]")):
            color = COLORS['green']
        elif "[STANDBY]" in log:
            color = COLORS['yellow']
        elif "haloflux" in log or "glm-5.3" in log:
            color = COLORS['cyan']
        else:
            color = COLORS['dim']
        content += f"""
        <text y="{i*24}" fill="{color}" opacity="0">
            {log}
            <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{i*0.13}s" fill="freeze" />
        </text>
        """
    content += "</g>"
    return svg_base(h, content, "03")

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

    # 底部微型波形图 (30 天活动频率示意)
    def make_sparkline(x, y, color, pts):
        return f"""
        <g transform="translate({x}, {y})">
            <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <polygon points="{pts} 100,25 0,25" fill="{color}" fill-opacity="0.1"/>
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

    spark_shapes = [
        "0,18 10,12 20,16 30,6 40,10 50,3 60,11 70,17 80,7 90,13 100,2",
        "0,10 10,15 20,7 30,12 40,4 50,13 60,8 70,16 80,5 90,11 100,1",
        "0,16 10,9 20,13 30,4 40,11 50,6 60,14 70,3 80,10 90,15 100,5",
        "0,12 10,18 20,5 30,9 40,14 50,2 60,7 70,12 80,4 90,10 100,0",
        "0,8 10,13 20,6 30,15 40,3 50,10 60,5 70,14 80,2 90,9 100,4",
    ]
    spark_x = [40, 150, 260, 370, 480]
    spark_colors = [COLORS['cyan'], COLORS['magenta'], COLORS['green'], COLORS['yellow'], COLORS['purple']]
    sparklines = [
        make_sparkline(x, 170, color, pts)
        for x, color, pts in zip(spark_x, spark_colors, spark_shapes)
    ]

    spark_label = f"""
    <text x="40" y="158" fill="{COLORS['dim']}" font-size="8" letter-spacing="1">ACTIVITY.SPARK // 30D</text>
    <text x="580" y="158" fill="{COLORS['dim']}" font-size="8" letter-spacing="1" text-anchor="end">CH1..CH5</text>
    """
    spark_baseline = f'<line x1="40" y1="195" x2="580" y2="195" stroke="{COLORS["stroke"]}" stroke-width="1"/>'
    bus_note = f'<text x="320" y="138" fill="{COLORS["dim"]}" font-size="8" letter-spacing="1">BUS.0x02 // SAMPLE 1Hz</text>'

    radar_scores = [0.95, 0.85, 0.70, 0.90, 0.60, 0.80]
    radar = make_radar(880, 120, 75, radar_scores)

    return svg_base(h, ruler + header + "".join(bars) + bus_note + spark_label + "".join(sparklines) + spark_baseline + radar, "02")

# --- 区块 04: TOOLCHAIN ---
def render_toolchain(data):
    h = 240
    
    # 工业图纸风格底纹 (十字对齐线 + 极小字号工程批号)
    bg = f"""
    <path d="M 24,20 L 34,20 M 24,20 L 24,30 M {WIDTH-24},20 L {WIDTH-34},20 M {WIDTH-24},20 L {WIDTH-24},30" fill="none" stroke="{COLORS['dim']}" stroke-width="1"/>
    <text x="64" y="32" fill="{COLORS['dim']}" font-size="12" font-weight="bold" letter-spacing="2">SYS.ARCH // HARDWARE &amp; FIRMWARE TOPOLOGY</text>
    <text x="{WIDTH-32}" y="40" fill="{COLORS['dim']}" font-size="8" text-anchor="end">REV. 2.6.1_PROD</text>
    <line x1="24" y1="44" x2="{WIDTH-24}" y2="44" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="4 2"/>
    """
    
    # 渲染右上角的装饰性条形码
    barcode = ""
    for i in [0, 4, 6, 12, 16, 20, 24, 30, 32, 38]:
        barcode += f'<line x1="{WIDTH - 120 + i}" y1="18" x2="{WIDTH - 120 + i}" y2="34" stroke="{COLORS["dim"]}" stroke-width="{1 if i%3==0 else 2}"/>'

    # 非对称工业内存块生成器
    def make_block(x, y, w, h, label, sub_labels, color, hex_addr):
        subs = ""
        for idx, sub in enumerate(sub_labels):
            subs += f'<text x="{x+10}" y="{y+42+(idx*16)}" fill="{COLORS["dim"]}" font-size="12">- {sub}</text>'
            
        return f"""
        <g>
            <!-- 实体方块与背景 -->
            <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{COLORS['panel']}" stroke="{color}" stroke-width="1"/>
            <rect x="{x}" y="{y}" width="{w}" height="22" fill="{color}" fill-opacity="0.15"/>
            <!-- 标题与十六进制地址 -->
            <text x="{x+10}" y="{y+15}" fill="{color}" font-size="12" font-weight="bold">{label}</text>
            <text x="{x+w-10}" y="{y+15}" fill="{color}" font-size="12" font-family="'JetBrains Mono', Consolas" text-anchor="end">{hex_addr}</text>
            <!-- 接口焊点节点 -->
            <circle cx="{x+w}" cy="{y+h/2}" r="3" fill="{COLORS['bg']}" stroke="{color}" stroke-width="1.5"/>
            {subs}
            <!-- 底部高亮装饰线 -->
            <line x1="{x+10}" y1="{y+h-10}" x2="{x+w-10}" y2="{y+h-10}" stroke="{color}" stroke-opacity="0.4" stroke-width="2"/>
        </g>
        """

    # 绘制数据总线走线 (直角拐角，模拟 PCB 走线)
    bus_lines = f"""
    <path d="M 280,125 L 320,125" fill="none" stroke="{COLORS['cyan']}" stroke-width="2" stroke-dasharray="4 2"/>
    <path d="M 520,95 L 560,95" fill="none" stroke="{COLORS['yellow']}" stroke-width="2"/>
    <path d="M 520,175 L 540,175 L 540,155 L 560,155" fill="none" stroke="{COLORS['yellow']}" stroke-width="2"/>
    <path d="M 760,140 L 800,140" fill="none" stroke="{COLORS['magenta']}" stroke-width="2"/>
    <path d="M 1000,140 L 1040,140" fill="none" stroke="{COLORS['green']}" stroke-width="2"/>
    """

    # 基于真实开发栈构建拓扑矩阵，避免假大空的名词
    blocks = [
        make_block(80, 70, 200, 110, "MCU_CORE", ["STM32F103C8T6", "ESP32-S3", "FreeRTOS / ESP-IDF"], COLORS['cyan'], "0x0800"),
        make_block(320, 60, 200, 70, "PERIPHERALS", ["I2C / SPI / UART", "RS485 / PWM"], COLORS['yellow'], "0x4000"),
        make_block(320, 140, 200, 70, "MOTION_CTRL", ["ROS2 Humble", "Nav2 / SLAM"], COLORS['yellow'], "0x4002"),
        make_block(560, 70, 200, 140, "AI_VISION", ["YOLOv8 / YOLOv11", "Qwen2.5-VL / Ollama", "OpenCV / ONNX", "Intel RealSense D435"], COLORS['magenta'], "0x6000"),
        make_block(800, 70, 200, 140, "WEB_PORTAL", ["Vue 3 + Element Plus", "Django REST Framework", "Next.js / Tailwind", "Three.js / WebGL"], COLORS['green'], "0x8000")
    ]

    return svg_base(h, bg + barcode + bus_lines + "".join(blocks), "04")

# --- 区块 05: BUILDS ---
def render_builds(data):
    h = 240
    content = ""
    
    title = f"<text x=\"64\" y=\"30\" fill=\"{COLORS['dim']}\" font-size=\"12\" font-weight=\"bold\" letter-spacing=\"2\">ACCESSING_RECORDS // BUILDS</text>"
    content += title

    def make_card(x, y, build):
        w = 360
        card_h = 150
        return f"""
        <g transform="translate({x}, {y})">
            <!-- 卡片底板 -->
            <rect x="0" y="0" width="{w}" height="{card_h}" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
            
            <!-- 瞄准器边角 (HUD) -->
            <path d="M -5,-5 L 10,-5 M -5,-5 L -5,10" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M {w+5},-5 L {w-10},-5 M {w+5},-5 L {w+5},10" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M -5,{card_h+5} L 10,{card_h+5} M -5,{card_h+5} L -5,{card_h-10}" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>
            <path d="M {w+5},{card_h+5} L {w-10},{card_h+5} M {w+5},{card_h+5} L {w+5},{card_h-10}" fill="none" stroke="{COLORS['cyan']}" stroke-width="2"/>

            <!-- 顶部装饰带 -->
            <rect x="0" y="0" width="{w}" height="4" fill="{COLORS['purple']}"/>
            
            <!-- 编号与语言标签 -->
            <text x="16" y="30" fill="{COLORS['yellow']}" font-size="18" font-family="'JetBrains Mono', Consolas" font-weight="700">[{build['id']}]</text>
            <text x="60" y="28" fill="{COLORS['dim']}" font-size="12" font-weight="bold">{build['lang'].upper()}</text>
            
            <!-- 呼吸状态点 -->
            <circle cx="{w-20}" cy="24" r="4" fill="{COLORS['green']}">
                <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
            </circle>

            <!-- 项目代号 -->
            <text x="16" y="65" fill="#FFFFFF" font-size="20" font-weight="700" letter-spacing="1">{build['codename']}</text>
            
            <!-- 中文描述 (分两行) -->
            <text x="16" y="95" fill="{COLORS['cyan']}" font-size="14">{build['desc'][0]}</text>
            <text x="16" y="115" fill="{COLORS['cyan']}" font-size="14">{build['desc'][1]}</text>
            
            <!-- 底部装饰线索 -->
            <line x1="16" y1="135" x2="{w-16}" y2="135" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="2 2"/>
        </g>
        """

    # 横向排列三个卡片
    start_x = (WIDTH - (360 * 3 + 40 * 2)) / 2 # 居中计算
    for i, build in enumerate(data['builds']):
        content += make_card(start_x + i * 400, 70, build)
        
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
