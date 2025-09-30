import PyPDF2
import os
import logging
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

class PDFService:
    """Service for handling PDF operations"""
    
    def __init__(self, upload_folder="./uploads"):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyPDF2 with error handling"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        text += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
                        continue
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def save_uploaded_file(self, file):
        """Save uploaded file and return path"""
        if not file or file.filename == '':
            raise ValueError("No file provided")
        
        # Secure filename
        filename = secure_filename(file.filename)
        if not filename.lower().endswith('.pdf'):
            raise ValueError("Only PDF files are allowed")
        
        # Save file
        pdf_path = os.path.join(self.upload_folder, filename)
        file.save(pdf_path)
        logger.info(f"File saved: {pdf_path}")
        
        return pdf_path
    
    def cleanup_file(self, file_path):
        """Clean up uploaded file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file: {e}")
    
    def process_uploaded_pdf(self, file):
        """Complete PDF processing workflow"""
        pdf_path = None
        try:
            # Save file
            pdf_path = self.save_uploaded_file(file)
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("No readable text found in PDF or text too short")
            
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
            
        finally:
            # Always cleanup
            if pdf_path:
                self.cleanup_file(pdf_path)

    def extract_text_and_meta(self, pdf_path):
        """
        Extract text, word count, and title from PDF using PyPDF2.
        Returns: (text, word_count, title)
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        text = self.extract_text_from_pdf(pdf_path)
        word_count = len(text.split())
        title = os.path.basename(pdf_path)

        return text, word_count, title
