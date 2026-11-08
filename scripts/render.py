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

# --- 区块 02: TELEMETRY ---
def render_telemetry(data):
    h = 130
    
    # 尝试加载真实抓取的 GitHub 遥测数据
    real_data = {}
    try:
        import json, os
        if os.path.exists("data/github.json"):
            with open("data/github.json", "r", encoding="utf-8") as f:
                gh_raw = json.load(f)
                real_data = {
                    "followers": gh_raw.get("followers", 0),
                    "repos": gh_raw.get("public_repos", 0),
                    "following": gh_raw.get("following", 0)
                    # 注: Stars 和 Commits 需要更复杂的 GraphQL API，这里用现有 REST 字段做示范
                }
    except Exception as e:
        print(f"[-] Telemetry sensor offline, using fallback data. ({e})")

    # 顶部滑动的数据包轨迹 (SMIL 动效)
    track = f"""
    <path id="data-track" d="M 24,10 L {WIDTH-24},10" fill="none" stroke="{COLORS['cyan']}" stroke-opacity="0.2" stroke-width="1" stroke-dasharray="2 4"/>
    <circle r="3" fill="{COLORS['yellow']}" filter="url(#glow-cyan)">
        <animateMotion dur="8s" repeatCount="indefinite">
            <mpath href="#data-track"/>
        </animateMotion>
    </circle>
    """
    
    # 数据表盘生成器 (支持动态输入真实数值)
    def make_dial(x, title, value, max_val, color):
        percent = min(1.0, value / max_val)
        dash_full = 188.5 # 2 * pi * r (r=30)
        dash_val = dash_full * percent
        
        return f"""
        <g transform="translate({x}, 70)">
            <text x="0" y="-45" fill="{COLORS['dim']}" font-size="10" font-weight="bold" letter-spacing="1" text-anchor="middle">{title}</text>
            <!-- 环形底圈 -->
            <circle cx="0" cy="0" r="30" fill="none" stroke="{COLORS['stroke']}" stroke-width="4"/>
            <!-- 动态注入的数据进度圈 -->
            <circle cx="0" cy="0" r="30" fill="none" stroke="{color}" stroke-width="4" stroke-dasharray="{dash_full}" stroke-dashoffset="{dash_full}" transform="rotate(-90)" stroke-linecap="round">
                <animate attributeName="stroke-dashoffset" from="{dash_full}" to="{dash_full - dash_val}" dur="2.5s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
            </circle>
            <!-- 中心跳动的真实数据 -->
            <text x="0" y="5" fill="#FFFFFF" font-size="16" font-family="'JetBrains Mono', Consolas" font-weight="bold" text-anchor="middle">
                {value}
                <!-- 数字加载闪烁错觉 -->
                <animate attributeName="opacity" values="0;1;0.5;1" dur="1s" repeatCount="1" fill="freeze"/>
            </text>
        </g>
        """

    # 如果有真实数据就用真实数据，否则用视觉效果极佳的 Mock 数据填充监控矩阵
    sys_followers = real_data.get("followers", 42)
    sys_repos = real_data.get("repos", 18)
    sys_following = real_data.get("following", 12)

    dials = [
        make_dial(150, "SYS.FOLLOWERS", sys_followers, max(100, sys_followers*2), COLORS['cyan']),
        make_dial(375, "REPO.PUBLIC", sys_repos, max(50, sys_repos*2), COLORS['magenta']),
        make_dial(600, "SYS.FOLLOWING", sys_following, max(50, sys_following*2), COLORS['green']),
        # 预留给未来通过 GraphQL 抓取的复杂数据
        make_dial(825, "RUNTIME.STARS", 128, 500, COLORS['yellow']), 
        make_dial(1050, "COMMITS.YTD", 1024, 2048, COLORS['purple'])
    ]
    
    return svg_base(h, track + "".join(dials))

# --- 区块 04: TOOLCHAIN ---
def render_toolchain(data):
    h = 240
    
    # 工业图纸风格底纹 (十字对齐线 + 极小字号工程批号)
    bg = f"""
    <path d="M 24,20 L 34,20 M 24,20 L 24,30 M {WIDTH-24},20 L {WIDTH-34},20 M {WIDTH-24},20 L {WIDTH-24},30" fill="none" stroke="{COLORS['dim']}" stroke-width="1"/>
    <text x="32" y="32" fill="{COLORS['dim']}" font-size="10" font-weight="bold" letter-spacing="2">SYS.ARCH // HARDWARE &amp; FIRMWARE TOPOLOGY</text>
    <text x="{WIDTH-32}" y="32" fill="{COLORS['dim']}" font-size="8" text-anchor="end">REV. 2.6.1_PROD</text>
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
            subs += f'<text x="{x+10}" y="{y+42+(idx*16)}" fill="{COLORS["dim"]}" font-size="11">- {sub}</text>'
            
        return f"""
        <g>
            <!-- 实体方块与背景 -->
            <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{COLORS['panel']}" stroke="{color}" stroke-width="1"/>
            <rect x="{x}" y="{y}" width="{w}" height="22" fill="{color}" fill-opacity="0.15"/>
            <!-- 标题与十六进制地址 -->
            <text x="{x+10}" y="{y+15}" fill="{color}" font-size="12" font-weight="bold">{label}</text>
            <text x="{x+w-10}" y="{y+15}" fill="{color}" font-size="10" font-family="'JetBrains Mono', Consolas" text-anchor="end">{hex_addr}</text>
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

    return svg_base(h, bg + barcode + bus_lines + "".join(blocks))

# --- 区块 05: BUILDS ---
def render_builds(data):
    h = 420
    content = ""
    
    title = f"<text x=\"24\" y=\"30\" fill=\"{COLORS['dim']}\" font-size=\"12\" font-weight=\"bold\" letter-spacing=\"2\">ACCESSING_RECORDS // BUILDS</text>"
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
            <text x="16" y="30" fill="{COLORS['yellow']}" font-size="18" font-family="'JetBrains Mono', Consolas" font-weight="900">[{build['id']}]</text>
            <text x="60" y="28" fill="{COLORS['dim']}" font-size="10" font-weight="bold">{build['lang'].upper()}</text>
            
            <!-- 呼吸状态点 -->
            <circle cx="{w-20}" cy="24" r="4" fill="{COLORS['green']}">
                <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
            </circle>

            <!-- 项目代号 -->
            <text x="16" y="65" fill="#FFFFFF" font-size="20" font-weight="900" letter-spacing="1">{build['codename']}</text>
            
            <!-- 中文描述 (分两行) -->
            <text x="16" y="95" fill="{COLORS['cyan']}" font-size="13">{build['desc'][0]}</text>
            <text x="16" y="115" fill="{COLORS['cyan']}" font-size="13">{build['desc'][1]}</text>
            
            <!-- 底部装饰线索 -->
            <line x1="16" y1="135" x2="{w-16}" y2="135" stroke="{COLORS['stroke']}" stroke-width="1" stroke-dasharray="2 2"/>
        </g>
        """

    # 横向排列三个卡片
    start_x = (WIDTH - (360 * 3 + 40 * 2)) / 2 # 居中计算
    for i, build in enumerate(data['builds']):
        content += make_card(start_x + i * 400, 70, build)
        
    return svg_base(h, content)

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
