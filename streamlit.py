import streamlit as st
import os
import json
import time
from pathlib import Path
from collections import Counter
import tempfile
import re

# Configure page
st.set_page_config(
    page_title="Document Analyzer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .result-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .topic-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def check_libraries():
    """Check available libraries"""
    available = {}
    try:
        import PyPDF2
        available['pdf'] = True
    except:
        available['pdf'] = False
    
    try:
        import docx
        available['docx'] = True
    except:
        available['docx'] = False
    
    try:
        import textstat
        available['textstat'] = True
    except:
        available['textstat'] = False
    
    return available

def extract_text_from_file(file_path, file_type):
    """Extract text from different file types"""
    try:
        if file_type == 'pdf':
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        
        elif file_type == 'docx':
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
                
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def analyze_document(text, filename):
    """Analyze document and generate metadata"""
    start_time = time.time()
    
    # Basic stats
    words = text.split() if text else []
    word_count = len(words)
    char_count = len(text)
    
    # Document type detection
    text_lower = text.lower()
    if any(word in text_lower for word in ['abstract', 'introduction', 'methodology', 'conclusion']):
        doc_type = "📚 Academic Paper"
    elif any(word in text_lower for word in ['executive', 'business', 'market', 'strategy']):
        doc_type = "💼 Business Document"
    elif any(word in text_lower for word in ['chapter', 'novel', 'story']):
        doc_type = "📖 Literary Work"
    elif word_count < 100:
        doc_type = "📝 Short Document"
    else:
        doc_type = "📄 General Document"
    
    # Readability score
    readability = 0
    try:
        import textstat
        if text:
            readability = textstat.flesch_reading_ease(text)
    except:
        pass
    
    # Key topics (frequent words)
    stop_words = {'the', 'and', 'are', 'for', 'with', 'this', 'that', 'from', 'they', 'have', 'been', 'will', 'can', 'was', 'were', 'not', 'you', 'your', 'but', 'all', 'may', 'said', 'each', 'which', 'their', 'time'}
    clean_words = [w.lower().strip('.,!?;:"()[]') for w in words if len(w) > 3 and w.lower() not in stop_words]
    topics = [word for word, count in Counter(clean_words).most_common(8)]
    
    # Simple summary (first two sentences)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    summary = '. '.join(sentences[:2]) + '.' if len(sentences) >= 2 else text[:200] + "..."
    
    # Extract entities
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}\b', text)
    percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    
    processing_time = time.time() - start_time
    
    return {
        'filename': filename,
        'word_count': word_count,
        'char_count': char_count,
        'doc_type': doc_type,
        'readability': readability,
        'topics': topics,
        'summary': summary,
        'dates': list(set(dates))[:5],
        'percentages': list(set(percentages))[:5],
        'emails': list(set(emails))[:3],
        'processing_time': processing_time
    }

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📄 Document Analyzer</h1>
        <p>Upload documents or paste text to extract insights and metadata</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check available libraries
    libs = check_libraries()
    if not all(libs.values()):
        with st.expander("⚠️ Optional Features Available"):
            if not libs['pdf']:
                st.code("pip install PyPDF2  # For PDF support")
            if not libs['docx']:
                st.code("pip install python-docx  # For Word documents")
            if not libs['textstat']:
                st.code("pip install textstat  # For readability scores")
    
    # Input method selection
    st.subheader("Choose Input Method")
    input_method = st.radio(
        "",
        ["📁 Upload File", "✍️ Paste Text", "🎯 Try Sample"],
        horizontal=True
    )
    
    text_content = ""
    filename = ""
    
    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx', 'md', 'py', 'js', 'html', 'css'],
            help="Supports: TXT, PDF, DOCX, MD, and code files"
        )
        
        if uploaded_file:
            filename = uploaded_file.name
            file_extension = Path(filename).suffix.lower()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                if file_extension == '.pdf':
                    text_content = extract_text_from_file(tmp_path, 'pdf')
                elif file_extension == '.docx':
                    text_content = extract_text_from_file(tmp_path, 'docx')
                else:
                    text_content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
            finally:
                os.unlink(tmp_path)
    
    elif input_method == "✍️ Paste Text":
        filename = st.text_input("Document name (optional)", "pasted_text.txt")
        text_content = st.text_area(
            "Paste your text here:",
            height=150,
            placeholder="Enter or paste your text content here..."
        )
    
    elif input_method == "🎯 Try Sample":
        sample_options = {
            "Research Paper": """Abstract: Machine learning applications in healthcare have shown remarkable progress in recent years. This study examines the implementation of deep learning algorithms for medical image analysis. Introduction: Artificial intelligence is revolutionizing healthcare diagnostics. Our methodology involves convolutional neural networks trained on medical imaging datasets. Results indicate 95% accuracy in tumor detection. Conclusion: AI-powered diagnostic tools show great promise for improving patient outcomes.""",
            
            "Business Report": """Executive Summary: Q3 financial results show strong growth across all business segments. Revenue increased 18% year-over-year to $2.4 billion, driven by digital transformation initiatives. Market expansion in Asia-Pacific region contributed 25% of total growth. Strategic recommendations include investing in cloud infrastructure and expanding our e-commerce platform. Customer satisfaction scores improved to 89%, reflecting our commitment to service excellence.""",
            
            "Technical Guide": """Installation Instructions: This guide covers the setup process for our new software platform. System Requirements: Windows 10 or macOS 10.15+, 8GB RAM minimum, 20GB available storage. Step 1: Download the installer from our official website. Step 2: Run the installer with administrator privileges. Step 3: Configure database connections and API endpoints. Troubleshooting: Common issues include firewall blocking port 8080 and insufficient disk space."""
        }
        
        selected_sample = st.selectbox("Choose a sample:", list(sample_options.keys()))
        filename = f"{selected_sample.lower().replace(' ', '_')}.txt"
        text_content = sample_options[selected_sample]
        
        st.text_area("Sample text:", text_content, height=100, disabled=True)
    
    # Analyze button
    if st.button("🚀 Analyze Document", type="primary", use_container_width=True):
        if text_content:
            with st.spinner("🔍 Analyzing document..."):
                time.sleep(0.5)  # Small delay for UX
                results = analyze_document(text_content, filename)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Quick stats row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Words", results['word_count'])
                with col2:
                    st.metric("Characters", results['char_count'])
                with col3:
                    st.metric("Type", results['doc_type'].split(' ', 1)[1])
                with col4:
                    st.metric("Readability", f"{results['readability']:.0f}" if results['readability'] else "N/A")
                
                # Summary section
                st.subheader("📋 Summary")
                st.write(results['summary'])
                
                # Topics section
                if results['topics']:
                    st.subheader("🏷️ Key Topics")
                    topics_html = "".join([f'<span class="topic-tag">{topic}</span>' for topic in results['topics'][:6]])
                    st.markdown(topics_html, unsafe_allow_html=True)
                
                # Entities found
                col1, col2 = st.columns(2)
                
                with col1:
                    if results['dates']:
                        st.subheader("📅 Dates Found")
                        for date in results['dates']:
                            st.write(f"• {date}")
                    
                    if results['percentages']:
                        st.subheader("📊 Percentages")
                        for pct in results['percentages']:
                            st.write(f"• {pct}")
                
                with col2:
                    if results['emails']:
                        st.subheader("📧 Email Addresses")
                        for email in results['emails']:
                            st.write(f"• {email}")
                
                # Download section
                st.subheader("💾 Export Results")
                
                # Create JSON export
                export_data = {
                    "document_info": {
                        "filename": results['filename'],
                        "analysis_date": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "processing_time": f"{results['processing_time']:.2f}s"
                    },
                    "content_metrics": {
                        "word_count": results['word_count'],
                        "character_count": results['char_count'],
                        "document_type": results['doc_type'],
                        "readability_score": results['readability']
                    },
                    "extracted_data": {
                        "summary": results['summary'],
                        "key_topics": results['topics'],
                        "dates": results['dates'],
                        "percentages": results['percentages'],
                        "email_addresses": results['emails']
                    }
                }
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📄 Download JSON Report",
                        json.dumps(export_data, indent=2),
                        f"analysis_{results['filename']}.json",
                        "application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # Create text summary
                    text_summary = f"""Document Analysis Report
=====================================
File: {results['filename']}
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS:
- Words: {results['word_count']}
- Characters: {results['char_count']}
- Type: {results['doc_type']}
- Readability: {results['readability']:.1f}

SUMMARY:
{results['summary']}

KEY TOPICS:
{', '.join(results['topics'][:6])}

EXTRACTED ENTITIES:
Dates: {', '.join(results['dates']) if results['dates'] else 'None'}
Percentages: {', '.join(results['percentages']) if results['percentages'] else 'None'}
Emails: {', '.join(results['emails']) if results['emails'] else 'None'}
"""
                    
                    st.download_button(
                        "📝 Download Text Summary",
                        text_summary,
                        f"summary_{results['filename']}.txt",
                        "text/plain",
                        use_container_width=True
                    )
                
                # Raw data view
                with st.expander("🔍 View Raw Data"):
                    st.json(export_data)
        
        else:
            st.warning("⚠️ Please provide some text content to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "Document Analyzer • Built with Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()