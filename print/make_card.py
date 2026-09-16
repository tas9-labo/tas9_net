"""名刺（91×55mm）の印刷原稿を作る。+9 ロゴ・名前（和／英）・QR だけの構成（2026-09-17 本人指定）。

出力（すべてベクター。QR はここで生成）:
  print/card_91x55.pdf     … 1枚（名刺サイズの用紙・カードプリンタ向け）
  print/card_a4_10up.pdf   … A4 に 10 面付け（エーワン 51002＝マイクロミシン目・2列×5行・上 11mm／左 14mm・隙間なし）
  print/card_preview.png   … 目視確認用（300dpi）
実行: py print/make_card.py（このフォルダ直下から）。フォントは Windows 標準の游ゴシック。
必要: reportlab・svglib・pymupdf（プレビュー用）。
"""
from pathlib import Path

from reportlab.graphics import renderPDF
import qrcode
import qrcode.image.svg
from reportlab.graphics.shapes import Drawing, Group, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

HERE = Path(__file__).resolve().parent
URL = "https://www.tas9.net/"
INK = HexColor("#1d1d1f")
SUB = HexColor("#6e6e73")
CARD_W, CARD_H = 91 * mm, 55 * mm

pdfmetrics.registerFont(TTFont("YuGothB", "C:/Windows/Fonts/YuGothB.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YuGothM", "C:/Windows/Fonts/YuGothM.ttc", subfontIndex=0))


def build_card() -> Drawing:
    d = Drawing(CARD_W, CARD_H)
    d.add(Rect(0, 0, CARD_W, CARD_H, fillColor=white, strokeColor=None))

    # ロゴ（+9）: 左上。高さ 11mm
    logo = svg2rlg(str(HERE.parent / "logo.svg"))
    scale = (11 * mm) / logo.height
    logo.scale(scale, scale)
    logo.width, logo.height = logo.width * scale, logo.height * scale
    g = Group(logo)
    g.translate(7.5 * mm, CARD_H - 8 * mm - 11 * mm)
    d.add(g)

    # 名前（和）＋英名: 左下に寄せる（ロゴ＝左上・名前＝左下・QR＝右中央の三点で釣り合わせる）
    d.add(String(8 * mm, 15 * mm, "高橋 佐", fontName="YuGothB", fontSize=19, fillColor=INK))
    d.add(String(8 * mm, 9.5 * mm, "Tasuku Takahashi", fontName="YuGothM", fontSize=8, fillColor=SUB))

    # QR: 右側・26mm 角（静穏域 2 モジュール込み）・上下中央。
    # qrcode ライブラリの「1本のパス」SVG を使う（モジュール間に継ぎ目が出ない）。
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2, box_size=10)
    q.add_data(URL)
    q.make(fit=True)
    svg_path = HERE / "_qr_tmp.svg"
    q.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(str(svg_path))
    qr = svg2rlg(str(svg_path))
    svg_path.unlink()
    size = 26 * mm
    s = size / qr.width
    qr.scale(s, s)
    wrap = Group(qr)
    wrap.translate(CARD_W - 8 * mm - size, (CARD_H - size) / 2)
    d.add(wrap)
    return d


def main() -> None:
    card = build_card()
    renderPDF.drawToFile(card, str(HERE / "card_91x55.pdf"))

    # A4 10面付け（エーワン 51002 系: 上余白 11mm・左余白 14mm・2列×5行・隙間なし）
    a4_w, a4_h = 210 * mm, 297 * mm
    c = canvas.Canvas(str(HERE / "card_a4_10up.pdf"), pagesize=(a4_w, a4_h))
    left, top = 14 * mm, 11 * mm
    for row in range(5):
        for col in range(2):
            x = left + col * CARD_W
            y = a4_h - top - (row + 1) * CARD_H
            renderPDF.draw(card, c, x, y)
    # ガイド線は引かない（51002 はミシン目入り。線を刷るとわずかなズレが端に灰色の筋として残る）
    c.showPage()
    c.save()
    # 目視確認用 PNG（PDF をそのまま 300dpi でラスタライズ。印刷に使うのは PDF）
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(str(HERE / "card_91x55.pdf"))
        doc[0].get_pixmap(dpi=300).save(str(HERE / "card_preview.png"))
        doc.close()
    except ImportError:
        print("PyMuPDF が無いのでプレビュー PNG は省略（py -m pip install pymupdf）")
    print("wrote card_91x55.pdf / card_a4_10up.pdf / card_preview.png")


if __name__ == "__main__":
    main()
