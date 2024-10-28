import streamlit as st
import pytesseract
from PIL import Image, ImageDraw
import io
import base64
import os

# Tesseract Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def verify_tesseract():
    try:
        version = pytesseract.get_tesseract_version()
        return True, f"Tesseract version: {version}"
    except Exception as e:
        return False, f"Tesseract error: {str(e)}"

def extract_text(image):
    """Extract text from image using Tesseract OCR."""
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"Error during text extraction: {str(e)}")
        return None

def extract_bboxes(image, bbox_type):
    """Extract bounding boxes from image using Tesseract OCR."""
    try:
        # Configure page segmentation mode based on bbox_type
        config = r'--oem 3'
        if bbox_type == 'word':
            config += r' --psm 3'
        elif bbox_type == 'line':
            config += r' --psm 6'
        elif bbox_type == 'paragraph':
            config += r' --psm 4'
        elif bbox_type in ['block', 'page']:
            config += r' --psm 3'

        # Get OCR data
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=config)
        
        # Define level mapping
        level_map = {
            'word': 5,
            'line': 4,
            'paragraph': 3,
            'block': 2,
            'page': 1
        }
        
        bboxes = []
        n_boxes = len(data['level'])
        target_level = level_map[bbox_type]
        
        # Special handling for different bbox types
        if bbox_type == 'word':
            # For words, we look at the confidence score
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Only include words with confidence > 0
                    bbox = {
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i],
                        'text': data['text'][i],
                        'conf': data['conf'][i]
                    }
                    if bbox['text'].strip():  # Only include non-empty text
                        bboxes.append(bbox)
        else:
            # For other levels, we use the level information
            current_bbox = None
            for i in range(n_boxes):
                if data['level'][i] == target_level:
                    if current_bbox is not None:
                        if current_bbox['text'].strip():
                            bboxes.append(current_bbox)
                    
                    current_bbox = {
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i],
                        'text': data['text'][i]
                    }
                elif current_bbox is not None and data['level'][i] > target_level:
                    # Accumulate text for higher levels
                    current_bbox['text'] += ' ' + data['text'][i]
                    # Update bbox boundaries
                    current_bbox['x_max'] = max(current_bbox['x_max'], 
                                              data['left'][i] + data['width'][i])
                    current_bbox['y_max'] = max(current_bbox['y_max'], 
                                              data['top'][i] + data['height'][i])
            
            # Add the last bbox if it exists
            if current_bbox is not None and current_bbox['text'].strip():
                bboxes.append(current_bbox)
        
        return bboxes
    except Exception as e:
        st.error(f"Error during bbox extraction: {str(e)}")
        return None

def draw_bboxes(image, bboxes, color="red"):
    """Draw bounding boxes on the image."""
    img_draw = image.copy()
    draw = ImageDraw.Draw(img_draw)
    
    # Use different colors for different confidence levels (for words)
    for bbox in bboxes:
        outline_color = color
        if 'conf' in bbox:
            # Color based on confidence for words
            if bbox['conf'] >= 80:
                outline_color = "green"
            elif bbox['conf'] >= 50:
                outline_color = "yellow"
            else:
                outline_color = "red"
                
        draw.rectangle(
            [
                bbox['x_min'], bbox['y_min'],
                bbox['x_max'], bbox['y_max']
            ],
            outline=outline_color,
            width=2
        )
    return img_draw

def get_image_download_link(img, filename):
    """Generate a download link for the image."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download Annotated Image</a>'

def main():
    st.set_page_config(
        page_title="OCR Text & BBox Extractor",
        page_icon="📝",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
            .stAlert {margin-top: 1rem;}
            .upload-prompt {font-size: 1.2rem; margin-bottom: 1rem;}
            .results-area {margin-top: 2rem;}
            .bbox-options {margin: 1rem 0;}
            .stButton>button {
                width: 100%;
                margin-top: 1rem;
            }
            .css-1d391kg {
                padding-top: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📝 OCR Text & Bounding Box Extractor")

    # Verify Tesseract installation
    tesseract_ok, tesseract_msg = verify_tesseract()
    if not tesseract_ok:
        st.error(tesseract_msg)
        st.stop()
    else:
        st.sidebar.success(tesseract_msg)

    st.markdown("""
    ### Instructions:
    1. Upload an image containing text
    2. Choose to either extract text or detect text regions
    3. Download the results or copy extracted text
    """)

    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg"],
        help="Upload an image containing text"
    )

    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)

            # Add tabs for different functionalities
            tab1, tab2 = st.tabs(["📝 Extract Text", "📦 Detect Bounding Boxes"])
            
            with tab1:
                if st.button("Extract Text", key="extract_text"):
                    with st.spinner("Extracting text..."):
                        text = extract_text(image)
                        if text:
                            st.text_area("Extracted Text:", value=text, height=300)
                            st.download_button(
                                label="Download Text",
                                data=text,
                                file_name="extracted_text.txt",
                                mime="text/plain"
                            )
            
            with tab2:
                bbox_type = st.selectbox(
                    "Select bounding box type:",
                    ["word", "line", "paragraph", "block", "page"],
                    help="Choose the level of text segments to detect"
                )
                
                if st.button("Detect Bounding Boxes", key="detect_bboxes"):
                    with st.spinner("Detecting bounding boxes..."):
                        bboxes = extract_bboxes(image, bbox_type)
                        if bboxes:
                            # Create annotated image
                            annotated_image = draw_bboxes(image, bboxes)
                            
                            # Display results
                            with col2:
                                st.subheader("Annotated Image")
                                st.image(annotated_image, use_column_width=True)
                                
                                # Download button for annotated image
                                st.markdown(
                                    get_image_download_link(
                                        annotated_image,
                                        f"annotated_{uploaded_file.name}"
                                    ),
                                    unsafe_allow_html=True
                                )
                            
                            # Display detected text segments
                            st.subheader(f"Detected {bbox_type.title()} Segments")
                            segments_text = ""
                            for i, bbox in enumerate(bboxes, 1):
                                if bbox['text'].strip():
                                    confidence_info = f"(Confidence: {bbox['conf']}%)" if 'conf' in bbox else ""
                                    segment_info = f"""
                                    Segment {i}:
                                    - Text: {bbox['text']}
                                    - Position: ({bbox['x_min']}, {bbox['y_min']}) to ({bbox['x_max']}, {bbox['y_max']}) {confidence_info}
                                    """
                                    segments_text += segment_info
                                    st.markdown(f"""
                                        **Segment {i}:**
                                        - Text: {bbox['text']}
                                        - Position: ({bbox['x_min']}, {bbox['y_min']}) to ({bbox['x_max']}, {bbox['y_max']}) {confidence_info}
                                    """)
                            
                            # Add download button for segments text
                            if segments_text:
                                st.download_button(
                                    label="Download Segments Info",
                                    data=segments_text,
                                    file_name=f"segments_{uploaded_file.name}.txt",
                                    mime="text/plain"
                                )
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()