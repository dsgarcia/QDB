from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def text_size(draw, text, fnt, spacing=2):
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align="center")
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font(draw, text, box, max_size, min_size=7, bold=False, spacing=2):
    w = box[2] - box[0] - 8
    h = box[3] - box[1] - 6
    for size in range(max_size, min_size - 1, -1):
        fnt = font(size, bold)
        tw, th = text_size(draw, text, fnt, spacing)
        if tw <= w and th <= h:
            return fnt
    return font(min_size, bold)


def box_text(draw, box, text, size=18, fill="black", bg="white", bold=False, spacing=2):
    draw.rectangle(box, fill=bg)
    fnt = fit_font(draw, text, box, size, bold=bold, spacing=spacing)
    tw, th = text_size(draw, text, fnt, spacing)
    x = box[0] + (box[2] - box[0] - tw) / 2
    y = box[1] + (box[3] - box[1] - th) / 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, spacing=spacing, align="center")


def rotated_text(img, center, text, size=18, angle=0, fill="black", bg="white", bold=False):
    fnt = font(size, bold)
    tmp = Image.new("RGBA", (260, 90), (255, 255, 255, 0))
    td = ImageDraw.Draw(tmp)
    bbox = td.textbbox((0, 0), text, font=fnt)
    pad = 8
    layer = Image.new("RGBA", (bbox[2] - bbox[0] + 2 * pad, bbox[3] - bbox[1] + 2 * pad), bg)
    ld = ImageDraw.Draw(layer)
    ld.text((pad, pad), text, font=fnt, fill=fill)
    rotated = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x = int(center[0] - rotated.width / 2)
    y = int(center[1] - rotated.height / 2)
    img.alpha_composite(rotated, (x, y))


def arrow_line(draw, start, end, fill, width=3, head=12):
    draw.line([start, end], fill=fill, width=width)
    import math

    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (
        end[0] - head * math.cos(angle - math.pi / 6),
        end[1] - head * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - head * math.cos(angle + math.pi / 6),
        end[1] - head * math.sin(angle + math.pi / 6),
    )
    draw.polygon([end, left, right], fill=fill)


def credibility_composition():
    img = Image.open(FIG / "credibility-dq-composition.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    blue = (45, 95, 128, 255)

    box_text(draw, (70, 195, 135, 330), "", bg=white)
    rotated_text(img, (105, 263), "Derived from", size=20, angle=90, bg=white, bold=True)
    box_text(draw, (394, 300, 515, 337), "Producer", size=21, bg=white)
    box_text(draw, (820, 300, 980, 337), "Consumer", size=21, bg=white)
    box_text(draw, (328, 486, 430, 517), "Contributes", size=20, bg=white)
    box_text(draw, (452, 625, 635, 682), "Presumed", size=26, bg=white)
    box_text(draw, (724, 625, 895, 682), "Reputed", size=26, bg=white)
    box_text(draw, (1012, 625, 1180, 682), "Surface", size=26, bg=white)
    box_text(draw, (1228, 694, 1295, 878), "", bg=white)
    rotated_text(img, (1260, 782), "Measured by", size=35, angle=-90, bg=white)

    draw.rectangle((472, 364, 585, 432), fill=white)
    draw.rectangle((780, 356, 860, 425), fill=white)
    arrow_line(draw, (455, 336), (667, 464), blue, width=3, head=12)
    arrow_line(draw, (866, 337), (694, 464), blue, width=3, head=12)
    rotated_text(img, (524, 402), "Builds", size=18, angle=-34, bg=white)
    rotated_text(img, (820, 392), "Perceives", size=18, angle=47, bg=white)

    img.convert("RGB").save(FIG / "credibility-dq-composition-en.png", quality=95)


def processing_flow():
    img = Image.open(FIG / "processing-flow-white.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    gray = (242, 242, 242, 255)
    green = (217, 238, 211, 255)
    yellow = (255, 242, 204, 255)

    labels = [
        ((17, 38, 68, 101), "Original\nClip", 13, green),
        ((2, 169, 82, 244), "Clip Format\nNormalization", 12, gray),
        ((132, 178, 177, 246), "Norm.\nClip", 13, green),
        ((227, 178, 304, 244), "Feature\nOrchestration\nModule", 11, gray),
        ((360, 0, 484, 45), "Feature\nGeneration\nModules", 12, white),
        ((391, 55, 456, 127), "User Feature\nGeneration", 11, gray),
        ((391, 136, 456, 205), "Entity Feature\nGeneration", 11, gray),
        ((391, 217, 456, 284), "Image Feature\nGeneration", 11, gray),
        ((390, 444, 454, 516), "Enriched\nClip", 13, green),
        ((498, 459, 545, 537), "Quality\nMetrics", 12, yellow),
        ((373, 585, 470, 677), "Quality\nOrchestration\nModule", 11, gray),
        ((565, 600, 661, 676), "Credibility\nModule", 11, gray),
        ((151, 770, 239, 856), "Provenance\nModule", 11, gray),
        ((255, 770, 347, 856), "Trustworthiness\nModule", 11, gray),
        ((361, 770, 452, 856), "Expertise\nModule", 11, gray),
        ((468, 770, 557, 856), "Reputation\nModule", 11, gray),
        ((578, 770, 666, 856), "Verifiability\nModule", 11, gray),
        ((727, 605, 786, 672), "Enriched\nClip", 13, green),
        ((735, 719, 786, 800), "Quality\nMetrics", 12, yellow),
    ]
    for box, text, size, bg in labels:
        box_text(draw, box, text, size=size, bg=bg)

    draw.rectangle((118, 750, 143, 870), fill=white)
    rotated_text(img, (130, 810), "Quality Modules", size=11, angle=90, bg=white)

    img.convert("RGB").save(FIG / "processing-flow-en.png", quality=95)


def provenance_framework():
    img = Image.open(FIG / "provenance-framework-white.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    gray = (242, 242, 242, 255)
    green = (217, 238, 211, 255)
    yellow = (255, 242, 204, 255)
    white = (255, 255, 255, 255)

    labels = [
        ((508, 174, 578, 241), "Provenance\nGeneration\nModule", 11, gray),
        ((2, 328, 50, 420), "Quality\nMetrics", 11, yellow),
        ((342, 342, 414, 413), "Equivalent\nClip Search\nModules", 11, gray),
        ((532, 318, 579, 399), "Equivalent\nClips", 10, green),
        ((310, 560, 459, 581), "Extraction Modules", 12, white),
    ]
    for box, text, size, bg in labels:
        box_text(draw, box, text, size=size, bg=bg)

    img.convert("RGB").save(FIG / "provenance-framework-en.png", quality=95)


def gcp_architecture():
    img = Image.open(FIG / "gcp-architecture.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    cloud_bg = (245, 245, 245, 255)
    gray_text = (145, 145, 145, 255)

    box_text(draw, (0, 156, 84, 180), "Social Media\nClip", size=12, bg=white)
    box_text(draw, (406, 142, 505, 170), "Clip Format\nNormalization", size=11, fill=gray_text, bg=cloud_bg, bold=True)
    box_text(draw, (395, 190, 504, 240), "Feature Modules", size=11, fill=gray_text, bg=cloud_bg, bold=True)
    box_text(draw, (392, 374, 505, 402), "Quality Modules", size=11, fill=gray_text, bg=cloud_bg, bold=True)
    box_text(draw, (392, 441, 514, 468), "Credibility Module", size=11, fill=gray_text, bg=cloud_bg, bold=True)
    box_text(draw, (620, 151, 721, 183), "Normalized Clip\nwith Metrics", size=12, bg=white)

    img.convert("RGB").save(FIG / "gcp-architecture-en.png", quality=95)


if __name__ == "__main__":
    credibility_composition()
    processing_flow()
    provenance_framework()
    gcp_architecture()
