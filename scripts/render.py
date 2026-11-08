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
def svg_base(height, content):
    defs = f"""
    <defs>
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="4" y2="0" stroke="#FFFFFF" stroke-opacity="0.04" stroke-width="1"/>
        </pattern>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <rect width="40" height="40" fill="none" stroke="{COLORS['cyan']}" stroke-opacity="0.06" stroke-width="1"/>
        </pattern>
    </defs>
    """
    # 强制覆盖底层属性，禁用 JS
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="100%" height="100%" style="background-color:{COLORS['bg']}; font-family: 'JetBrains Mono', Consolas, 'Microsoft YaHei', sans-serif;">
    {defs}
    <rect width="{WIDTH}" height="{height}" fill="{COLORS['bg']}" />
    <rect width="{WIDTH}" height="{height}" fill="url(#grid)" />
    {content}
    <rect width="{WIDTH}" height="{height}" fill="url(#scanlines)" pointer-events="none" />
    <!-- HUD Corners -->
    <path d="M 14,0 L 0,0 L 0,14 M {WIDTH-14},0 L {WIDTH},0 L {WIDTH},14 M {WIDTH-14},{height} L {WIDTH},{height} L {WIDTH},{height-14} M 14,{height} L 0,{height} L 0,{height-14}" fill="none" stroke="{COLORS['stroke']}" stroke-width="2" />
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
        <text x="0" y="0" fill="{COLORS['magenta']}" font-size="110" font-weight="900" letter-spacing="-2">
            {data['callsign']}
            <animateTransform attributeName="transform" type="translate" values="4,0; 4,4; -2,-2; 4,0" keyTimes="0; 0.1; 0.2; 1" dur="3.7s" calcMode="discrete" repeatCount="indefinite"/>
        </text>
        <text x="0" y="0" fill="{COLORS['cyan']}" font-size="110" font-weight="900" letter-spacing="-2">
            {data['callsign']}
            <animateTransform attributeName="transform" type="translate" values="-4,0; -4,-4; 2,2; -4,0" keyTimes="0; 0.1; 0.2; 1" dur="5.2s" calcMode="discrete" repeatCount="indefinite"/>
        </text>
        <text x="0" y="0" fill="#FFFFFF" font-size="110" font-weight="900" letter-spacing="-2">{data['callsign']}</text>
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

    # 底部示波器波形动画
    waveforms = f"""
    <g transform="translate(0, 420)">
        <line x1="24" y1="0" x2="{WIDTH-24}" y2="0" stroke="{COLORS['yellow']}" stroke-width="1" stroke-dasharray="4 4" />
        <text x="32" y="-8" fill="{COLORS['yellow']}" font-size="10" letter-spacing="1">TRIG 50%</text>
        <!-- 滚动的 PWM 方波 -->
        <g stroke="{COLORS['cyan']}" stroke-width="2" fill="none" filter="url(#glow-cyan)">
            <path d="M0,40 L40,40 L40,-40 L80,-40 L80,40 L120,40 L120,-40 L160,-40 L160,40 L200,40 L200,-40 L240,-40 L240,40 L280,40 L280,-40 L320,-40 L320,40 L360,40 L360,-40 L400,-40 L400,40 L440,40 L440,-40 L480,-40 L480,40 L520,40 L520,-40 L560,-40 L560,40 L600,40 L600,-40 L640,-40 L640,40 L680,40 L680,-40 L720,-40 L720,40 L760,40 L760,-40 L800,-40 L800,40 L840,40 L840,-40 L880,-40 L880,40 L920,40 L920,-40 L960,-40 L960,40 L1000,40 L1000,-40 L1040,-40 L1040,40 L1080,40 L1080,-40 L1120,-40 L1120,40 L1160,40 L1160,-40 L1200,-40 L1200,40 L1240,40 L1240,-40 L1280,-40">
                <animateTransform attributeName="transform" type="translate" from="0,0" to="-80,0" dur="1.2s" repeatCount="indefinite" />
            </path>
        </g>
    </g>
    """
    return svg_base(h, top_bar + glitch_text + typewriter + waveforms)

# --- 区块 03: WHOAMI ---
def render_whoami(data):
    h = 344
    content = f"""
    <!-- 左侧终端面板 -->
    <rect x="24" y="24" width="680" height="{h-48}" rx="14" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
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
    <rect x="728" y="24" width="448" height="{h-48}" rx="14" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1"/>
    <g font-size="13" transform="translate(748, 64)" fill="{COLORS['dim']}">
    """
    logs = [
        "[ 0.000] jasmine-os 2.6 boot", "[ 0.041] cpu: cortex-m4 @ 168MHz", 
        "[ 0.082] can0: 500 kbit/s online", "[ 0.123] i2c: oled 0x3c ack",
        "[ 0.164] pwm: tim3 ch1..ch4 armed", "[ 0.205] fs: mount /lab ok",
        "[ 0.246] net: ros2 agent up", "[ 0.287] theme: neon loaded", 
        "[ 0.328] ready for input_"
    ]
    for i, log in enumerate(logs):
        color = COLORS['green'] if "ready" in log else COLORS['dim']
        content += f"""
        <text y="{i*26}" fill="{color}" opacity="0">
            {log}
            <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{i*0.13}s" fill="freeze" />
        </text>
        """
    content += "</g>"
    return svg_base(h, content)

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
    return svg_base(h, content)

# --- 占位符：供其他模块直接使用简单的线框代替，符合极客约束 ---
def render_placeholder(name, height):
    return svg_base(height, f"""
    <rect x="24" y="24" width="{WIDTH-48}" height="{height-48}" fill="{COLORS['panel']}" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="4 4" rx="14"/>
    <text x="600" y="{height/2}" fill="{COLORS['dim']}" font-size="16" letter-spacing="4" text-anchor="middle" font-weight="bold">MODULE [{name}] : INITIALIZING...</text>
    <circle cx="{WIDTH-48}" cy="48" r="4" fill="{COLORS['yellow']}">
        <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    """)

if __name__ == "__main__":
    os.makedirs(ASSETS_DIR, exist_ok=True)
    data = load_data()
    
    with open(f"{ASSETS_DIR}/01_hero.svg", "w", encoding="utf-8") as f: f.write(render_hero(data))
    with open(f"{ASSETS_DIR}/02_telemetry.svg", "w", encoding="utf-8") as f: f.write(render_placeholder("TELEMETRY_DATA", 112))
    with open(f"{ASSETS_DIR}/03_whoami.svg", "w", encoding="utf-8") as f: f.write(render_whoami(data))
    with open(f"{ASSETS_DIR}/04_toolchain.svg", "w", encoding="utf-8") as f: f.write(render_placeholder("HARDWARE_TOOLCHAIN", 214))
    with open(f"{ASSETS_DIR}/05_builds.svg", "w", encoding="utf-8") as f: f.write(render_placeholder("RECENT_BUILDS", 392))
    with open(f"{ASSETS_DIR}/08_footer.svg", "w", encoding="utf-8") as f: f.write(render_footer(data))
    
    print("SVG assets successfully rendered.")
