import io
import fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = 2300000000
# 拼接
IMAGES_FORMAT = ['.png']  # 图片格式
IMAGE_SIZE = 500  # 每张小图片的大小
IMAGE_COLUMN = 1  # 图片间隔，也就是合并成一张图后，一共有几列


def pyMuPDF_fitz(pdfPath, imagePath):
    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    pages = []
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 2.66666666
        zoom_y = 2.66666666
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pages.append(pix)
    IMAGE_ROW = len(pages)
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))
    for y in range(1, IMAGE_ROW + 1):
        image_bytes = pages[y - 1].tobytes()
        image = Image.open(io.BytesIO(image_bytes))
        from_image = image.resize(
            (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
        to_image.paste(from_image, (0, (y - 1) * IMAGE_SIZE))
    return to_image.save(imagePath)  # 保存新图


if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = 'C:\\Users\\dell\\Desktop\\xxxxxx.pdf'
    # 2、需要储存图片的目录
    imagePath = 'C:\\Users\\dell\\Desktop\\img.png'
    pyMuPDF_fitz(pdfPath, imagePath)



