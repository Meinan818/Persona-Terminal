# -*- coding: utf-8 -*-
"""纯蓝丝绒改造脚本：把 WelcomeModal.tsx 从「紫罗兰极光+渐变紫按钮+彩色emoji」
改为「墨蓝丝绒 + 冷白顶光 + 冷银蓝」的天鹅绒房间视觉。
一次性精确替换，避免正则破坏括号。
"""
import io

P = 'src/components/WelcomeModal.tsx'
s = io.open(P, encoding='utf-8').read()

# ── 1. 色板常量：把整个 VELVET 定义块替换（先定位原 AuroraBackground 之前无 VELVET，
#        而是散落的紫色。我们注入 VELVET 常量到 Constants 区） ──

# 在 "const ATTR_IDS" 之前注入 VELVET 常量与 SERIF
VELVET_BLOCK = '''/**
 * 天鹅绒房间视觉基线（PERSONA 二创改造 · 纯蓝丝绒版）：
 *   墨蓝丝绒 + 冷白顶光 + 玻璃门 —— Velvet Room 是「蓝」的，不是「金」。
 *   冷、沉、静谧；光从玻璃门缝漏下，只带极少量冷银点缀。
 */
const VELVET = {
  bg: '#040713',
  panel: 'rgba(8, 14, 34, 0.90)',
  line: 'rgba(120, 165, 235, 0.28)',
  lineStrong: 'rgba(140, 185, 250, 0.45)',
  silver: '#c8d6f0',
  ink: 'rgba(226, 236, 255, 0.92)',
  inkDim: 'rgba(170, 190, 228, 0.58)',
  inkFaint: 'rgba(150, 172, 214, 0.30)',
  accent: '#6f9fdb',
  accentBright: '#9cc2f2',
} as const;

/** 天鹅绒衬线：标题 / 仪式文案专用 */
const SERIF = "'Velvet Serif SC', 'Noto Serif SC', 'Songti SC', SimSun, serif";

'''
anchor = 'const ATTR_IDS: AttributeId[]'
assert anchor in s, '未找到 ATTR_IDS 锚点'
s = s.replace(anchor, VELVET_BLOCK + anchor, 1)

# ── 2. 属性图标：彩色 emoji → 花色符号（P 系通用语言，冷银单色由使用处控制） ──
s = s.replace("""const DEFAULT_ATTR_ICONS: Record<AttributeId, string> = {
  knowledge: '📖',
  guts: '💪',
  dexterity: '✨',
  kindness: '💝',
  charm: '👑',
};""", """const DEFAULT_ATTR_ICONS: Record<AttributeId, string> = {
  knowledge: '✦',
  guts: '♠',
  dexterity: '♦',
  kindness: '♥',
  charm: '♣',
};""")

# ── 3. 主按钮：渐变紫 → 冷蓝丝绒双线 ──
s = s.replace("""const PRIMARY_BTN_STYLE = {
  background: 'linear-gradient(135deg, #7c3aed, #6d28d9, #4f46e5)',
  boxShadow: '0 4px 22px rgba(124,58,237,0.38)',
};""", """const PRIMARY_BTN_STYLE: React.CSSProperties = {
  background: 'linear-gradient(165deg, #122248 0%, #0a1228 78%)',
  border: '1px solid rgba(140,185,250,0.45)',
  boxShadow: 'inset 0 0 0 3.5px #0a1226, inset 0 0 0 4.5px rgba(120,165,235,0.30), 0 4px 26px rgba(0,0,0,0.55), 0 0 22px rgba(120,170,245,0.12)',
  color: '#9cc2f2',
  fontFamily: SERIF,
  letterSpacing: '0.14em',
};""")

# ── 4. 背景：AuroraBackground → VelvetBackground（纯蓝丝绒） ──
start = s.index('// ── Aurora Background')
end = s.index('// ── Guide Step')
bg_block = '''// ── Velvet Background（天鹅绒房间 · 纯蓝丝绒）─────────────────────────
// 墨蓝丝绒幕布 + 幽冷顶光 + 玻璃门竖条反光。冷、沉、静谧。

const VelvetBackground = () => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
    <div
      className="absolute inset-0"
      style={{
        background:
          'radial-gradient(ellipse 130% 95% at 50% 0%, #0d1a3a 0%, #080f26 32%, #050916 66%, #03050d 100%)',
      }}
    />
    <motion.div
      animate={{ opacity: [0.5, 0.7, 0.5] }}
      transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      style={{
        position: 'absolute',
        top: '-16%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '72%',
        height: '48%',
        borderRadius: '50%',
        background: 'radial-gradient(ellipse, rgba(150,190,250,0.14) 0%, transparent 65%)',
        filter: 'blur(44px)',
      }}
    />
    <div
      style={{
        position: 'absolute', top: '14%', left: '-16%', width: '56%', height: '64%',
        borderRadius: '50%', background: 'radial-gradient(circle, rgba(20,38,88,0.34) 0%, transparent 70%)', filter: 'blur(84px)',
      }}
    />
    <div
      style={{
        position: 'absolute', bottom: '4%', right: '-14%', width: '52%', height: '58%',
        borderRadius: '50%', background: 'radial-gradient(circle, rgba(16,32,76,0.38) 0%, transparent 70%)', filter: 'blur(88px)',
      }}
    />
    {[
      { left: '18%', top: '6%', h: '34%', o: 0.05 },
      { left: '32%', top: '10%', h: '26%', o: 0.07 },
      { left: '66%', top: '8%', h: '30%', o: 0.05 },
      { left: '80%', top: '5%', h: '36%', o: 0.06 },
    ].map((g, i) => (
      <div
        key={i}
        aria-hidden
        style={{
          position: 'absolute', left: g.left, top: g.top, width: 2, height: g.h,
          background: `linear-gradient(180deg, rgba(160,195,250,${g.o * 3}) 0%, rgba(120,165,235,${g.o}) 60%, transparent 100%)`,
          filter: 'blur(0.5px)',
        }}
      />
    ))}

    {PARTICLES.map(p => (
      <motion.div
        key={p.id}
        style={{
          position: 'absolute',
          left: p.x,
          top: p.y,
          width: p.size,
          height: p.size,
          borderRadius: '50%',
          background: '#bcd4f5',
          opacity: p.opacity * 0.7,
          boxShadow: `0 0 ${p.size * 3}px rgba(150,190,250,0.4)`,
        }}
        animate={{
          y: [0, -22, 0],
          opacity: [p.opacity * 0.2, p.opacity * 0.7, p.opacity * 0.2],
        }}
        transition={{
          duration: p.duration,
          repeat: Infinity,
          delay: p.delay,
          ease: 'easeInOut',
        }}
      />
    ))}
  </div>
);

'''
s = s[:start] + bg_block + s[end:]

# ── 5. 引用：AuroraBackground 调用点 → VelvetBackground ──
s = s.replace('<AuroraBackground />', '<VelvetBackground />')

# ── 6. 外层容器背景与卡片 ──
s = s.replace("style={{ background: '#06061a' }}", "style={{ background: VELVET.bg }}")
s = s.replace("""        <div
          className="rounded-3xl p-8"
          style={{
            background: 'rgba(10, 6, 38, 0.80)',
            backdropFilter: 'blur(32px)',
            WebkitBackdropFilter: 'blur(32px)',
            border: '1px solid rgba(255,255,255,0.07)',
            boxShadow:
              '0 0 80px rgba(109,40,217,0.18), 0 25px 60px rgba(0,0,0,0.75)',
          }}
        >""", """        <div
          className="p-8"
          style={{
            background: VELVET.panel,
            backdropFilter: 'blur(24px)',
            WebkitBackdropFilter: 'blur(24px)',
            border: '1px solid rgba(120,165,235,0.28)',
            boxShadow:
              'inset 0 0 0 4px #0a1226, inset 0 0 0 5px rgba(120,165,235,0.20), 0 0 70px rgba(30,48,124,0.35), 0 25px 60px rgba(0,0,0,0.8)',
            borderRadius: '3px',
          }}
        >""")

# ── 7. 进度指示器：紫色横条 → 冷蓝菱形 ──
s = s.replace("""              {[1, 2, 3, 4, 5].map(s => (
                <div
                  key={s}
                  className="h-1 rounded-full transition-all duration-500"
                  style={{
                    width: s <= stepIndex ? 32 : 12,
                    background:
                      s <= stepIndex ? '#a78bfa' : 'rgba(255,255,255,0.1)',
                    boxShadow:
                      s <= stepIndex
                        ? '0 0 8px rgba(167,139,250,0.55)'
                        : 'none',
                  }}
                />
              ))}""", """              {[1, 2, 3, 4, 5].map(s => {
                const lit = s <= stepIndex;
                return (
                  <div
                    key={s}
                    className="h-2 w-2 transition-all duration-500"
                    style={{
                      transform: `rotate(45deg) scale(${s === stepIndex ? 1.35 : 1})`,
                      background: lit ? '#8fb0e0' : 'rgba(150,180,225,0.12)',
                      boxShadow: lit
                        ? '0 0 10px rgba(140,185,250,0.5)'
                        : 'inset 0 0 0 1px rgba(150,180,225,0.3)',
                    }}
                  />
                );
              })}""")

# ── 8. Welcome 页：眉标 + 标题 + 文案（冷蓝衬线） ──
s = s.replace("JRPG Growth Tracker", "Persona Terminal")
s = s.replace("""                <p
                  className="text-[10px] font-semibold tracking-[0.28em] uppercase mb-2"
                  style={{ color: '#a78bfa' }}
                >""", """                <p
                  className="text-[10px] font-semibold tracking-[0.34em] uppercase mb-3"
                  style={{ color: '#9cc2f2' }}
                >""")
s = s.replace("""                <h1
                  className="text-4xl font-black mb-2 text-white"
                  style={{ textShadow: '0 0 48px rgba(167,139,250,0.45)' }}
                >
                  面具终端
                </h1>""", """                <h1
                  className="text-4xl font-black mb-3"
                  style={{
                    fontFamily: SERIF,
                    color: '#cfe0f8',
                    textShadow: '0 0 42px rgba(150,190,250,0.35), 0 2px 12px rgba(0,0,0,0.8)',
                  }}
                >
                  面具终端
                </h1>""")
s = s.replace("""                <div
                  className="w-20 h-px mx-auto mb-5 rounded-full"
                  style={{
                    background:
                      'linear-gradient(90deg, transparent, rgba(167,139,250,0.7), transparent)',
                  }}
                />""", """                <div
                  className="w-24 h-px mx-auto mb-5"
                  style={{
                    background:
                      'linear-gradient(90deg, transparent, rgba(150,190,250,0.75), transparent)',
                  }}
                />""")
s = s.replace("""                <p className="text-base mb-2" style={{ color: 'rgba(255,255,255,0.5)' }}>
                  欢迎来到你的成长空间
                </p>""", """                <p
                  className="text-base mb-2"
                  style={{ fontFamily: SERIF, color: VELVET.inkDim, letterSpacing: '0.06em' }}
                >
                  欢迎来到你的成长空间
                </p>""")
s = s.replace("""                <p
                  className="text-sm mb-10 leading-relaxed"
                  style={{ color: 'rgba(255,255,255,0.28)' }}
                >""", """                <p
                  className="text-sm mb-10 leading-relaxed"
                  style={{ color: VELVET.inkFaint }}
                >""")
# 欢迎 CTA hover
s = s.replace("""                  whileHover={{
                    scale: 1.02,
                    boxShadow: '0 8px 32px rgba(124,58,237,0.55)',
                  }}""", """                  whileHover={{
                    scale: 1.02,
                    boxShadow: 'inset 0 0 0 3.5px #0a1226, inset 0 0 0 4.5px rgba(120,165,235,0.30), 0 4px 26px rgba(0,0,0,0.55), 0 0 34px rgba(120,170,245,0.28)',
                  }}""")
s = s.replace("""                  className="text-xs transition-colors"
                  style={{ color: 'rgba(255,255,255,0.22)' }}
                  onMouseEnter={e =>
                    ((e.target as HTMLElement).style.color = 'rgba(255,255,255,0.5)')
                  }
                  onMouseLeave={e =>
                    ((e.target as HTMLElement).style.color = 'rgba(255,255,255,0.22)')
                  }""", """                  className="text-xs transition-colors"
                  style={{ color: 'rgba(150,180,225,0.4)' }}
                  onMouseEnter={e =>
                    ((e.target as HTMLElement).style.color = 'rgba(150,180,225,0.85)')
                  }
                  onMouseLeave={e =>
                    ((e.target as HTMLElement).style.color = 'rgba(150,180,225,0.4)')
                  }""")

# ── 9. 全局：剩余的紫色/暖色统一到冷蓝 ──
repl = [
    ("'linear-gradient(135deg, #7c3aed, #6d28d9, #4f46e5)'", "'linear-gradient(165deg, #122248 0%, #0a1228 80%)'"),
    ("boxShadow: '0 6px 24px rgba(124,58,237,0.4)'", "boxShadow: '0 4px 24px rgba(0,0,0,0.5)'"),
    ("boxShadow: '0 10px 40px rgba(124,58,237,0.5)'", "boxShadow: '0 6px 30px rgba(150,180,225,0.2)'"),
    ("background: 'rgba(109,40,217,0.12)'", "background: 'rgba(150,180,225,0.10)'"),
    ("background: 'rgba(124,58,237,0.13)'", "background: 'rgba(150,180,225,0.12)'"),
    ("background: 'rgba(124,58,237,0.07)'", "background: 'rgba(150,180,225,0.06)'"),
    ("border: '2px solid rgba(109,40,217,0.45)'", "border: '1.5px solid rgba(140,185,250,0.5)'"),
    ("border: '2px solid rgba(124,58,237,0.5)'", "border: '1.5px solid rgba(140,185,250,0.55)'"),
    ("border: '1px solid rgba(124,58,237,0.22)'", "border: '1px solid rgba(120,165,235,0.28)'"),
    ("background: 'rgba(167,139,250,0.09)'", "background: 'rgba(150,180,225,0.08)'"),
    ("border: '1px solid rgba(167,139,250,0.18)'", "border: '1px solid rgba(120,165,235,0.24)'"),
    ("background: 'rgba(167,139,250,0.12)'", "background: 'rgba(150,180,225,0.10)'"),
    ("border: '2px solid rgba(167,139,250,0.45)'", "border: '1.5px solid rgba(140,185,250,0.5)'"),
    ("boxShadow: '0 0 16px rgba(167,139,250,0.18)'", "boxShadow: '0 0 20px rgba(150,180,225,0.16)'"),
    ("color: '#a78bfa'", "color: '#8fb0e0'"),
    ("color: '#c4b5fd'", "color: '#b8cdf0'"),
    ("style={{ color: '#a78bfa' }}", "style={{ color: '#8fb0e0' }}"),
    ("style={{ color: '#c4b5fd' }}", "style={{ color: '#b8cdf0' }}"),
    ("style={{ color: '#e6cfa0' }}", "style={{ color: '#b8cdf0' }}"),
    ("boxShadow: '0 0 8px rgba(167,139,250,0.55)'", "boxShadow: '0 0 10px rgba(140,185,250,0.5)'"),
    ("color: '#9cc2f2'", "color: '#9cc2f2'"),  # no-op 占位
    # 文本灰白 → 冷蓝
    ("'rgba(255,255,255,0.5)'", "VELVET.inkDim"),
    ("'rgba(255,255,255,0.35)'", "'rgba(170,190,228,0.58)'"),
    ("'rgba(255,255,255,0.28)'", "'rgba(150,172,214,0.30)'"),
    ("'rgba(255,255,255,0.22)'", "'rgba(150,180,225,0.4)'"),
    ("'rgba(255,255,255,0.25)'", "'rgba(170,190,228,0.45)'"),
    ("'rgba(255,255,255,0.15)'", "'rgba(150,172,214,0.24)'"),
    ("'rgba(255,255,255,0.2)'", "'rgba(150,172,214,0.24)'"),
    ("'rgba(255,255,255,0.18)'", "'rgba(150,172,214,0.22)'"),
    ("'rgba(255,255,255,0.8)'", "'rgba(226,236,255,0.82)'"),
    ("'rgba(255,255,255,0.45)'", "'rgba(150,180,225,0.6)'"),
    ("'rgba(255,255,255,0.38)'", "'rgba(150,180,225,0.5)'"),
    # 输入框
    ("focus:border-violet-400/50", "focus:border-[#8fb0e0]/50"),
    ("focus:ring-2 focus:ring-violet-400/25", "focus:ring-2 focus:ring-[#8fb0e0]/25"),
    ("focus:ring-violet-400/40", "focus:ring-[#8fb0e0]/40"),
    ("focus:ring-violet-400/20", "focus:ring-[#8fb0e0]/20"),
    ("focus:ring-1 focus:ring-violet-400/30", "focus:ring-1 focus:ring-[#8fb0e0]/30"),
    ("focus:border-violet-400/40", "focus:border-[#8fb0e0]/40"),
    ("bg-white/[0.05]", "bg-[#8fb0e0]/[0.06]"),
    ("bg-white/[0.04]", "bg-[#8fb0e0]/[0.05]"),
    ("border border-white/10", "border border-[#8fb0e0]/20"),
    ("text-white/80", "text-[#e2ecff]/80"),
    ("placeholder-white/20", "placeholder-[#8fb0e0]/30"),
    ("placeholder-white/25", "placeholder-[#8fb0e0]/30"),
    # emoji 清掉（🎊/🌟/🗝️/☁️ 等）
    ("🎊", "✦"),
    ("🌟", "✦"),
    ("🗝️", "✧"),
    ("☁️", "☁"),
    ("'开始旅程 🦋'", "'开始旅程'"),
    ("'接受赐福，开始旅程 🦋'", "'接受赐福，开始旅程'"),
    ("'再试一次 🦋'", "'再试一次'"),
]
for a, b in repl:
    s = s.replace(a, b)

# ── 10. 赐福页文案微调：暖金高亮 → 冷蓝 ──
s = s.replace("""                    <span className="font-bold" style={{ color: '#c4b5fd' }}>
                      赐予一项永久祝福
                    </span>""", """                    <span className="font-bold" style={{ color: '#b8cdf0' }}>
                      赐予一项永久祝福
                    </span>""")

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('velvetify 完成')
