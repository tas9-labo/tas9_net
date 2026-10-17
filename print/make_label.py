"""ガジェット裏の QR シール（34×34mm・300dpi）と、ロック画面用の大きい QR・型押し用 SVG を作る。
実行: py print/make_label.py（このフォルダ直下から）。必要: qrcode[pil]。
URL は名刺ページの正式アドレス（takahashi.tas9.net・2026-10-17 に www から変更）。
"""
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.image.svg import SvgPathImage

HERE = Path(__file__).resolve().parent
URL = "https://takahashi.tas9.net/"
DPI = 300
MM = DPI / 25.4


def make(box, border):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box, border=border)
    q.add_data(URL)
    q.make(fit=True)
    return q


def main() -> None:
    size = round(34 * MM)  # 402px
    # QR だけを枠いっぱいに置く（URL が長くなって QR の目が増えても、余白ごと 34mm に収まるようマス目の大きさを決める）
    modules = make(1, 3).modules_count
    q = make(size // (modules + 6), 3)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    label = Image.new("RGB", (size, size), "white")
    label.paste(img, ((size - img.width) // 2, (size - img.height) // 2))
    label.save(HERE / "label_34mm_300dpi.png", dpi=(DPI, DPI))
    print("label", label.size, "modules", q.modules_count)
    make(48, 4).make_image(fill_color="black", back_color="white").convert("RGB").save(HERE / "qr_1000.png")
    make(10, 4).make_image(image_factory=SvgPathImage).save(str(HERE / "qr.svg"))
    print("wrote label_34mm_300dpi.png / qr_1000.png / qr.svg")


if __name__ == "__main__":
    main()
