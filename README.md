# OCR Text & Bounding Box Extractor

A Streamlit-based web application that performs Optical Character Recognition (OCR) on images and provides text extraction and bounding box detection capabilities. The application uses Tesseract OCR engine to detect and extract text from images at various levels (word, line, paragraph, block, and page).

## 🌟 Features

- **Text Extraction**: Extract all text from uploaded images
- **Bounding Box Detection**: Detect and visualize text regions at different levels:
  - Word level (with confidence scoring)
  - Line level
  - Paragraph level
  - Block level
  - Page level
- **Visual Results**: Side-by-side display of original and annotated images
- **Download Options**: 
  - Download extracted text
  - Download annotated images
  - Download detailed segment information

## 📋 Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.7+**
2. **Tesseract OCR Engine**:
   - Windows: Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

## 🛠️ Installation

1. Clone this repository or download the source code:
```bash
git clone <repository-url>
cd ocr-text-extractor
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install streamlit pytesseract pillow
```

## ⚙️ Configuration

1. For Windows users, verify the Tesseract installation path in the code:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

2. For Mac/Linux users, ensure Tesseract is in your system PATH.

## 🚀 Running the Application

1. Navigate to the project directory:
```bash
cd ocr-text-extractor
```

2. Run the Streamlit app:
```bash
streamlit run ocr_app.py
```

3. The application will open in your default web browser.

## 📝 Usage Instructions

1. **Upload Image**:
   - Click "Choose an image file" to upload an image containing text
   - Supported formats: PNG, JPG, JPEG

2. **Extract Text**:
   - Select the "Extract Text" tab
   - Click "Extract Text" button
   - View and download the extracted text

3. **Detect Bounding Boxes**:
   - Select the "Detect Bounding Boxes" tab
   - Choose the detection level (word, line, paragraph, block, or page)
   - Click "Detect Bounding Boxes" button
   - View the annotated image and text segment information
   - Download the annotated image or segment information

## 🎨 Visual Guide

For word-level detection, bounding boxes are color-coded based on confidence:
- 🟩 Green: High confidence (≥80%)
- 🟨 Yellow: Medium confidence (50-79%)
- 🟥 Red: Low confidence (<50%)

## 📄 Sample requirements.txt
```
streamlit==1.27.0
pytesseract==0.3.10
Pillow==10.0.0
```

## ⚠️ Troubleshooting

1. **Tesseract Not Found Error**:
   - Verify Tesseract is installed correctly
   - Check the path in the code matches your Tesseract installation path
   - Ensure Tesseract is added to system PATH (Mac/Linux)

2. **Image Upload Issues**:
   - Verify the image format (PNG, JPG, JPEG only)
   - Check if the image file is corrupted
   - Try reducing the image size if it's too large

3. **Poor Recognition Results**:
   - Ensure the image has good quality and contrast
   - Check if the text is clearly visible and not rotated
   - Try preprocessing the image (improving contrast, removing noise)

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements. For major changes, please open an issue first to discuss what you would like to change.


## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Streamlit](https://streamlit.io/)
- [Python Pillow](https://python-pillow.org/)

