"""SNS・共有サイト用のアバター（+9 ロゴ・1000px 正方形）を作る：avatar_1000.png。
実行: py print/make_avatar.py（このフォルダ直下から）。必要: reportlab・svglib・pymupdf（make_icons.py と同じ）。
丸く切り抜かれても欠けないよう、ロゴは幅の 62%・中央。色は名刺ページのライトと同じ（墨 #1d1d1f／地 #f5f5f7）。
使っている所：MakerWorld のプロフィール（2026-10-09〜）。ロゴ（logo.svg）を変えたら作り直して差し替える。
"""
from pathlib import Path

import pymupdf
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Group, Rect
from reportlab.lib.colors import HexColor
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "print" / "avatar_1000.png"
INK, BG = HexColor("#1d1d1f"), HexColor("#f5f5f7")
SIZE = 1000


def paint(node) -> None:
    for c in getattr(node, "contents", []):
        paint(c)
    if hasattr(node, "fillColor"):
        node.fillColor = INK


def main() -> None:
    d = Drawing(SIZE, SIZE)
    d.add(Rect(0, 0, SIZE, SIZE, fillColor=BG, strokeColor=None))
    lg = svg2rlg(str(ROOT / "logo.svg"))
    paint(lg)
    sc = (SIZE * 0.62) / lg.width
    lg.scale(sc, sc)
    g = Group(lg)
    g.translate((SIZE - lg.width * sc) / 2, (SIZE - lg.height * sc) / 2)
    d.add(g)
    tmp = OUT.with_suffix(".tmp.pdf")
    renderPDF.drawToFile(d, str(tmp))
    doc = pymupdf.open(str(tmp))
    doc[0].get_pixmap(matrix=pymupdf.Matrix(1, 1)).save(str(OUT))
    doc.close()
    tmp.unlink()
    print(OUT)


if __name__ == "__main__":
    main()
