import os
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def download_image(url, save_path):
    if not url or not isinstance(url, str) or not url.startswith('http'):
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        return save_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def create_ppt(slides_data, output_path="presentation.pptx", topic="AI Presentation"):
    prs = Presentation()
    
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = topic
    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = ""

    for i, slide_info in enumerate(slides_data):
        title_text = slide_info.get("title", "Slide Title")
        bullets = slide_info.get("content", [])
        image_url = slide_info.get("image_url", None)

        blank_layout = prs.slide_layouts[6] 
        slide = prs.slides.add_slide(blank_layout)

        MARGIN = Inches(1.0)
        TOP_MARGIN = Inches(0.5)
        TITLE_HEIGHT = Inches(1.0)
        CONTENT_TOP = Inches(1.8)
        
        TEXT_WIDTH = Inches(6.5)
        IMG_WIDTH = Inches(4.5)
        GAP = Inches(0.5)

        title_box = slide.shapes.add_textbox(
            MARGIN, TOP_MARGIN, prs.slide_width - (MARGIN * 2), TITLE_HEIGHT
        )
        title_tf = title_box.text_frame
        title_tf.text = title_text
        title_tf.paragraphs[0].font.size = Pt(40)
        title_tf.paragraphs[0].font.bold = True
        title_tf.paragraphs[0].alignment = PP_ALIGN.LEFT 

        text_box = slide.shapes.add_textbox(
            MARGIN, CONTENT_TOP, TEXT_WIDTH, Inches(5.0)
        )
        tf = text_box.text_frame
        tf.word_wrap = True
        
        for point in bullets:
            p = tf.add_paragraph()
            p.text = f"• {point}"
            p.font.size = Pt(20)
            p.space_before = Pt(14) 
            p.space_after = Pt(4)
            p.level = 0

        if image_url:
            img_filename = f"temp_img_{i}.jpg"
            img_path = download_image(image_url, img_filename)
            
            if img_path:
                try:
                    img_left = MARGIN + TEXT_WIDTH + GAP
                    
                    pic = slide.shapes.add_picture(
                        img_path,
                        left=img_left,
                        top=CONTENT_TOP,
                        width=IMG_WIDTH
                    )
        
                    if pic.height < Inches(4.5):
                        pic.top = CONTENT_TOP + Inches(0.5)

                except Exception as e:
                    print(f"Error adding image to slide: {e}")
            
                try:
                    os.remove(img_path)
                except:
                    pass

    prs.save(output_path)
    

