import io

from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

original_image = None
edited_image = None


def import_image(file):
    global original_image, edited_image
    try:
        original_image = Image.open(file)
        edited_image = original_image.copy()
        return True
    except Exception as e:
        print(f"Error importing image: {e}")
        return False


def apply_sepia():
    global edited_image
    if edited_image:
        sepia_image = ImageOps.colorize(edited_image.convert("L"), "#704214", "#C0C090")
        edited_image = sepia_image


def apply_black_and_white():
    global edited_image
    if edited_image:
        edited_image = edited_image.convert("L")


def apply_vintage():
    global edited_image
    if edited_image:
        enhancer = ImageEnhance.Color(edited_image)
        edited_image = enhancer.enhance(0.2)


def apply_dramatic():
    global edited_image
    if edited_image:
        edited_image = edited_image.filter(ImageFilter.DETAIL)


def apply_teal_and_orange():
    global edited_image
    if edited_image:
        r, g, b = edited_image.split()
        r = r.point(lambda i: i * 1.2)
        b = b.point(lambda i: i * 1.5)
        edited_image = Image.merge("RGB", (r, g, b))


def apply_cross_process():
    global edited_image
    if edited_image:
        r, g, b = edited_image.split()
        r = r.point(lambda i: min(255, int(i * 1.2)))
        g = g.point(lambda i: min(255, int(i * 1.1)))
        b = b.point(lambda i: min(255, int(i * 0.9)))
        edited_image = Image.merge("RGB", (r, g, b))


def apply_contrast():
    global edited_image
    if edited_image:
        enhancer = ImageEnhance.Contrast(edited_image)
        edited_image = enhancer.enhance(2)


def reset_image():
    global edited_image
    if original_image:
        edited_image = original_image.copy()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if import_image(file):
        return render_template('edit.html')
    else:
        return "Error importing image", 400


@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    filter_type = request.form['filter']
    if filter_type == 'sepia':
        apply_sepia()
    elif filter_type == 'black_and_white':
        apply_black_and_white()
    elif filter_type == 'vintage':
        apply_vintage()
    elif filter_type == 'dramatic':
        apply_dramatic()
    elif filter_type == 'teal_and_orange':
        apply_teal_and_orange()
    elif filter_type == 'cross_process':
        apply_cross_process()
    elif filter_type == 'contrast':
        apply_contrast()
    return render_template('edit.html')


@app.route('/show_image')
def show_image():
    global edited_image
    if edited_image:
        img_io = io.BytesIO()
        edited_image.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return "No image to show", 400


@app.route('/reset')
def reset():
    reset_image()
    return render_template('edit.html')


if __name__ == '__main__':
    app.run(debug=True)
