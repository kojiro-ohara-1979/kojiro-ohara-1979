"""
GitHubプロフィール用 ターミナル風アニメーションSVG ジェネレータ

  python gen_terminal.py  →  terminal.svg を出力

LINES を編集するだけで内容を差し替えられます。
  ("cmd", "コマンド")           : プロンプト + 1文字ずつタイプ
  ("out", "出力テキスト", "色")  : 一瞬で表示(色は省略可)
  ("gap",)                       : 空行
"""
from xml.sax.saxutils import escape

PROMPT = "kojiro-ohara-1979@github:~$ "

LINES = [
    ("cmd", "whoami"),
    ("out", "Kojiro Ohara - Head of Service Development @ Fleekdrive Inc. / Solxyz Co., Ltd.", "#e6edf3"),
    ("gap",),
    ("cmd", "cat career.log"),
    ("out", "[2001]  B.A. in Russian Language & Literature", "#e6edf3"),
    ("out", "        Far Eastern Federal University, Hakodate Branch", "#8b949e"),
    ("out", "[2003]  Started my career as a systems engineer", "#e6edf3"),
    ("out", "[2012]  Joined Solxyz Co., Ltd.", "#e6edf3"),
    ("out", "          - Custom software development for enterprise clients", "#8b949e"),
    ("out", "          - Liaison between Japanese clients and Philippine offshore teams", "#8b949e"),
    ("out", "          - Supported the launch of a FinTech startup", "#8b949e"),
    ("gap",),
    ("cmd", "cat ongoing.txt"),
    ("out", "- Head of Service Development, Fleekdrive Inc. (since 2024, concurrent)", "#e6edf3"),
    ("out", "- Driving DX initiatives", "#e6edf3"),
    ("out", "- Defining development standards to raise quality", "#e6edf3"),
    ("out", "- Engineer education and training", "#e6edf3"),
    ("out", "- Research & development", "#e6edf3"),
    ("gap",),
]

# ---- 見た目・タイミング設定 ----
WIDTH = 820
FONT_SIZE = 14
CHAR_W = FONT_SIZE * 0.6      # 等幅フォントの半角1文字幅(概算)
LINE_H = 22
PAD_X = 20
TOP = 52                      # タイトルバー下の1行目ベースライン
TYPE_SPEED = 0.07             # 1文字あたり秒
AFTER_CMD = 0.35              # Enter後、出力が出るまで
OUT_STEP = 0.12               # 出力行の間隔
AFTER_BLOCK = 0.5             # 次のコマンドまでの間

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
BG, BAR = "#0d1117", "#161b22"
GREEN, FG = "#3fb950", "#e6edf3"


def build():
    els, defs = [], []
    t = 0.6
    y = TOP
    prompt_w = len(PROMPT) * CHAR_W

    for i, line in enumerate(LINES):
        kind = line[0]
        if kind == "gap":
            y += LINE_H
            continue

        if kind == "cmd":
            cmd = line[1]
            # プロンプト
            els.append(
                f'<text x="{PAD_X}" y="{y}" fill="{GREEN}" opacity="0">'
                f'{escape(PROMPT)}<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
            )
            t += 0.3
            # タイプ部分:クリップ幅を1文字ずつ広げる
            n = len(cmd)
            dur = max(n * TYPE_SPEED, 0.01)
            widths = ";".join(f"{k * CHAR_W:.1f}" for k in range(n + 1))
            widths = widths.rsplit(";", 1)[0] + f";{n * CHAR_W + 20:.1f}"
            keytimes = ";".join(f"{k / n:.4f}" for k in range(n + 1)) if n else "0;1"
            cid = f"c{i}"
            defs.append(
                f'<clipPath id="{cid}"><rect x="{PAD_X + prompt_w}" y="{y - LINE_H + 6}" '
                f'height="{LINE_H}" width="0"><animate attributeName="width" values="{widths}" '
                f'keyTimes="{keytimes}" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" '
                f'fill="freeze"/></rect></clipPath>'
            )
            els.append(
                f'<text x="{PAD_X + prompt_w}" y="{y}" fill="{FG}" opacity="0" clip-path="url(#{cid})">'
                f'{escape(cmd)}<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
            )
            t += dur + AFTER_CMD
            y += LINE_H
            continue

        if kind == "out":
            text = line[1]
            color = line[2] if len(line) > 2 else FG
            els.append(
                f'<text x="{PAD_X}" y="{y}" fill="{color}" opacity="0">{escape(text)}'
                f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
            )
            t += OUT_STEP
            y += LINE_H
            nxt = LINES[i + 1][0] if i + 1 < len(LINES) else None
            if nxt != "out":
                t += AFTER_BLOCK

    # 最後のプロンプト + 点滅カーソル
    els.append(
        f'<text x="{PAD_X}" y="{y}" fill="{GREEN}" opacity="0">{escape(PROMPT)}'
        f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
    )
    els.append(
        f'<rect x="{PAD_X + prompt_w + 2}" y="{y - FONT_SIZE + 2}" width="{CHAR_W:.1f}" '
        f'height="{FONT_SIZE + 2}" fill="{FG}" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
        f'dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>'
    )

    height = y + LINE_H
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Kojiro Ohara terminal profile">
<defs>{"".join(defs)}</defs>
<rect width="{WIDTH}" height="{height}" rx="10" fill="{BG}"/>
<rect width="{WIDTH}" height="30" rx="10" fill="{BAR}"/>
<rect y="20" width="{WIDTH}" height="10" fill="{BAR}"/>
<circle cx="20" cy="15" r="6" fill="#ff5f56"/><circle cx="40" cy="15" r="6" fill="#ffbd2e"/><circle cx="60" cy="15" r="6" fill="#27c93f"/>
<text x="{WIDTH / 2}" y="20" fill="#8b949e" font-family="{FONT}" font-size="12" text-anchor="middle">kojiro-ohara-1979 — zsh</text>
<g font-family="{FONT}" font-size="{FONT_SIZE}" xml:space="preserve">
{chr(10).join(els)}
</g>
</svg>
'''


if __name__ == "__main__":
    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote terminal.svg")
