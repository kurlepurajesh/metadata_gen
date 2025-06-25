# 📄 Document Analyzer

A lightweight, easy-to-use document analysis tool that extracts insights and metadata from your files in seconds.

## 🌟 What it Does

Transform any document into structured insights:
- *Extract key information* from PDFs, Word docs, and text files
- *Identify important topics* and themes automatically  
- *Generate summaries* and readability scores
- *Find entities* like dates, percentages, and email addresses
- *Export results* as JSON or text reports

## 🚀 Quick Start

### 1. Install Python Requirements
bash
pip install streamlit PyPDF2 python-docx textstat


### 2. Run the App
bash
streamlit run app.py


### 3. Start Analyzing!
- Upload a file or paste text
- Click "Analyze Document"
- View insights and download results

## 📱 How to Use

### Upload Files
Drag and drop or browse for:
- 📄 *PDF files* (text-based)
- 📝 *Word documents* (.docx)
- 📋 *Text files* (.txt, .md)
- 💻 *Code files* (.py, .js, .html)

### Paste Text
Copy and paste any text content directly into the analyzer.

### Try Samples
Test with built-in sample documents to see how it works.

## 🎯 Features

### Smart Analysis
- *Document type detection* (Academic, Business, Technical, etc.)
- *Word and character counting*
- *Readability scoring* (how easy to read)
- *Key topic extraction*

### Entity Recognition
- 📅 *Dates* and time references
- 📊 *Percentages* and statistics  
- 📧 *Email addresses*
- 🔢 *Numbers* and quantities

### Export Options
- 📄 *JSON report* with all metadata
- 📝 *Text summary* for quick reading
- 💾 *Download* results instantly

## 🛠 Installation Options

### Basic Setup (Recommended)
bash
# Essential packages only
pip install streamlit


### Full Features
bash
# For PDF support
pip install PyPDF2

# For Word documents  
pip install python-docx

# For readability scores
pip install textstat


### Optional Enhancements
bash
# Advanced text analysis
pip install spacy
python -m spacy download en_core_web_sm

# Better summaries
pip install transformers


## 📋 Supported Files

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | .pdf | Text-based PDFs only |
| Word | .docx | Modern Word format |
| Text | .txt | Plain text files |
| Markdown | .md | Formatted text |
| Code | .py, .js, .html | Programming files |

## 🎨 What You Get

### Quick Overview
- File statistics (words, characters)
- Document type classification
- Readability assessment
- Processing time

### Detailed Analysis
- *Summary*: First few sentences
- *Topics*: Most important keywords
- *Entities*: Dates, emails, percentages found
- *Insights*: Document structure analysis

### Export Formats
json
{
  "document_info": {
    "filename": "my_document.pdf",
    "word_count": 1250,
    "document_type": "Business Document"
  },
  "extracted_data": {
    "summary": "This quarterly report shows...",
    "key_topics": ["revenue", "growth", "market"],
    "dates": ["2024", "Q3 2024"],
    "percentages": ["15%", "23%"]
  }
}


## 🔧 Customization

### Modify Analysis
Edit the analyze_document() function to:
- Add new entity types
- Change topic extraction rules
- Adjust readability calculations
- Include custom metrics

### Update UI
Modify the Streamlit interface:
- Change colors and styling
- Add new input methods
- Create custom visualizations
- Integrate with other tools

## 🐛 Common Issues

*File won't upload?*
- Check file size (max 200MB)
- Ensure supported format
- Try converting to .txt first

*PDF text is garbled?*
- File might be image-based
- Install OCR support: pip install pytesseract
- Convert to text manually

*Missing features?*
- Install optional packages above
- Check Python version (3.7+ required)
- Restart the app after installing packages

## 🎯 Use Cases

### Students & Researchers
- Analyze research papers
- Extract key findings
- Generate quick summaries
- Track important dates

### Business Users
- Process reports and proposals
- Extract key metrics
- Analyze document complexity
- Generate executive summaries

### Content Creators
- Analyze writing quality
- Check readability scores
- Extract main topics
- Optimize content structure

## 🔮 Future Ideas

- *Multi-language support*
- *OCR for scanned documents*
- *AI-powered insights*
- *Document comparison*
- *Batch processing*
- *Integration with cloud storage*

## 📞 Support

Having issues? Try these steps:
1. Check your Python version: python --version
2. Update packages: pip install --upgrade streamlit
3. Clear browser cache and refresh
4. Restart the Streamlit app

## 🏷 Tags

document-analysis metadata-extraction text-processing streamlit python pdf-processing nlp automation

---

*Made with ❤ using Python and Streamlit*
