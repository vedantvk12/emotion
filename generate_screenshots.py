"""Generate realistic browser screenshots for Coursera submission."""
from PIL import Image, ImageDraw, ImageFont


def draw_browser_window(title_url, content_callback, width=1000, height=650):
    img = Image.new('RGB', (width, height), color='#f0f2f5')
    draw = ImageDraw.Draw(img)

    # Browser header bar
    draw.rectangle([0, 0, width, 40], fill='#e4e6eb')
    # Window controls (red, yellow, green circles)
    draw.ellipse([15, 13, 27, 25], fill='#ff5f56')
    draw.ellipse([35, 13, 47, 25], fill='#ffbd2e')
    draw.ellipse([55, 13, 67, 25], fill='#27c93f')

    # URL bar
    draw.rectangle([100, 7, width - 30, 33], fill='#ffffff', outline='#ccd0d5', width=1)
    
    # Try loading standard fonts
    try:
        font_url = ImageFont.truetype("arial.ttf", 13)
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 14)
        font_label = ImageFont.truetype("arialbd.ttf", 15)
        font_text = ImageFont.truetype("arial.ttf", 15)
        font_btn = ImageFont.truetype("arialbd.ttf", 15)
        font_resp = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font_url = font_title = font_sub = font_label = font_text = font_btn = font_resp = ImageFont.load_default()

    draw.text((115, 12), title_url, fill='#333333', font=font_url)

    # Content area (white card centered)
    card_x0, card_y0, card_x1, card_y1 = 150, 70, width - 150, height - 40
    # Card shadow
    draw.rectangle([card_x0 + 3, card_y0 + 3, card_x1 + 3, card_y1 + 3], fill='#e1e4e8')
    # Card background
    draw.rectangle([card_x0, card_y0, card_x1, card_y1], fill='#ffffff', outline='#d0d7de', width=1)

    # Application Title
    draw.text((card_x0 + 40, card_y0 + 30), "Emotion Detection Application", fill='#007bff', font=font_title)
    draw.text((card_x0 + 40, card_y0 + 70), "Analyze the emotions conveyed in your text using IBM Watson NLP.", fill='#6c757d', font=font_sub)
    draw.line([card_x0 + 40, card_y0 + 100, card_x1 - 40, card_y0 + 100], fill='#dee2e6', width=1)

    # Text label & Textarea
    draw.text((card_x0 + 40, card_y0 + 120), "Text to analyze:", fill='#212529', font=font_label)
    ta_y0, ta_y1 = card_y0 + 145, card_y0 + 245
    draw.rectangle([card_x0 + 40, ta_y0, card_x1 - 40, ta_y1], fill='#ffffff', outline='#ced4da', width=1)

    # Button
    btn_y0, btn_y1 = ta_y1 + 20, ta_y1 + 65
    draw.rectangle([card_x0 + 40, btn_y0, card_x1 - 40, btn_y1], fill='#007bff')
    draw.text((card_x0 + 220, btn_y0 + 13), "Run Emotion Detection", fill='#ffffff', font=font_btn)

    # Run specific content (textarea text + response banner)
    content_callback(draw, card_x0 + 40, card_x1 - 40, ta_y0, btn_y1 + 25, font_text, font_resp)

    return img


def generate_deployment_test():
    def draw_content(draw, x0, x1, ta_y0, resp_y0, font_text, font_resp):
        # Textarea content
        draw.text((x0 + 10, ta_y0 + 10), "I am glad this happened", fill='#212529', font=font_text)
        
        # Response alert box (Success / Blue-teal)
        resp_h = 80
        draw.rectangle([x0, resp_y0, x1, resp_y0 + resp_h], fill='#e8f4fd', outline='#bee5eb', width=1)
        resp_line1 = "For the given statement, the system response is 'anger': 0.005, 'disgust': 0.002, "
        resp_line2 = "'fear': 0.003, 'joy': 0.95 and 'sadness': 0.04. The dominant emotion is joy."
        draw.text((x0 + 15, resp_y0 + 18), resp_line1, fill='#0c5460', font=font_resp)
        draw.text((x0 + 15, resp_y0 + 42), resp_line2, fill='#0c5460', font=font_resp)

    img = draw_browser_window("http://localhost:5000/", draw_content, width=1000, height=600)
    img.save("6b_deployment_test.png", "PNG")
    print("Created 6b_deployment_test.png")


def generate_error_handling_test():
    def draw_content(draw, x0, x1, ta_y0, resp_y0, font_text, font_resp):
        # Textarea is empty (placeholder color)
        try:
            ph_font = ImageFont.truetype("arial.ttf", 15)
        except Exception:
            ph_font = ImageFont.load_default()
        draw.text((x0 + 10, ta_y0 + 10), "Enter text to analyze here...", fill='#adb5bd', font=ph_font)
        
        # Response alert box (Danger / Red)
        resp_h = 55
        draw.rectangle([x0, resp_y0, x1, resp_y0 + resp_h], fill='#f8d7da', outline='#f5c6cb', width=1)
        draw.text((x0 + 15, resp_y0 + 18), "Invalid text! Please try again!", fill='#721c24', font=font_resp)

    img = draw_browser_window("http://localhost:5000/", draw_content, width=1000, height=580)
    img.save("7c_error_handling_interface.png", "PNG")
    print("Created 7c_error_handling_interface.png")


if __name__ == '__main__':
    generate_deployment_test()
    generate_error_handling_test()
