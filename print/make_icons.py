"""favicon 以外の画像2枚を作る：apple-touch-icon.png（180px・iOS 用）と og-image.png（1200×630・リンク共有時のプレビュー）。
実行: py print/make_icons.py（このフォルダ直下から）。必要: reportlab・svglib・pymupdf。フォントは Windows 標準の游ゴシック。
キャラ（chara.svg）・ロゴ（logo.svg）・肩書の文言を変えたら作り直す。favicon は index.html 内の SVG（chara の path）で別管理。
"""
from pathlib import Path

import pymupdf
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Group, Rect, String
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent.parent
INK, SUB, BG = HexColor("#1d1d1f"), HexColor("#6e6e73"), HexColor("#e5e5ea")
pdfmetrics.registerFont(TTFont("YuGothB", "C:/Windows/Fonts/YuGothB.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YuGothM", "C:/Windows/Fonts/YuGothM.ttc", subfontIndex=0))


def to_png(drawing: Drawing, out: Path) -> None:
    tmp = out.with_suffix(".tmp.pdf")
    renderPDF.drawToFile(drawing, str(tmp))
    doc = pymupdf.open(str(tmp))
    doc[0].get_pixmap(matrix=pymupdf.Matrix(1, 1)).save(str(out))
    doc.close()
    tmp.unlink()


def touch_icon() -> None:
    size = 180
    d = Drawing(size, size)
    d.add(Rect(0, 0, size, size, fillColor=BG, strokeColor=None))
    ic = svg2rlg(str(ROOT / "chara.svg"))
    sc = (size * 0.72) / max(ic.width, ic.height)
    ic.scale(sc, sc)
    g = Group(ic)
    g.translate((size - ic.width * sc) / 2, (size - ic.height * sc) / 2)
    d.add(g)
    to_png(d, ROOT / "apple-touch-icon.png")


def og_image() -> None:
    w, h = 1200, 630
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=BG, strokeColor=None))
    ch = svg2rlg(str(ROOT / "chara.svg"))
    sc = 220 / max(ch.width, ch.height)
    ch.scale(sc, sc)
    g = Group(ch)
    g.translate(110, (h - ch.height * sc) / 2)
    d.add(g)
    x = 390
    d.add(String(x, 372, "高橋 佐", fontName="YuGothB", fontSize=72, fillColor=INK))
    d.add(String(x, 322, "たかはし たすく / Tasuku Takahashi", fontName="YuGothM", fontSize=26, fillColor=SUB))
    d.add(String(x, 250, "モーションデザイナー / AIナレッジデザイナー / 専門学校講師", fontName="YuGothM", fontSize=28, fillColor=INK))
    d.add(String(x, 205, "www.tas9.net", fontName="YuGothM", fontSize=24, fillColor=SUB))
    lg = svg2rlg(str(ROOT / "logo.svg"))
    s2 = 120 / lg.height
    lg.scale(s2, s2)
    g2 = Group(lg)
    g2.translate(w - 110 - lg.width * s2, h - 80 - lg.height * s2)
    d.add(g2)
    to_png(d, ROOT / "og-image.png")


if __name__ == "__main__":
    touch_icon()
    og_image()
    print("wrote apple-touch-icon.png / og-image.png")
