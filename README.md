# 📄 PDF Outline Extractor
A Python-based solution for extracting structured outlines (title and headings) from PDF documents.
Developed for the Adobe India Hackathon 2025 – Round 1A: Connecting the Dots.

## 🔹 Approach
1️⃣ Font Size Extraction:

Using pdfminer.six, extract character-level font sizes.
Determine the most common font size (body text).

2️⃣ Title Detection:

The largest font size on the first page is considered the title.

3️⃣ Heading Detection:

Regex-based rules for Chapter X, 1.1, 1.1.1.

If no pattern match but font size > body font, classify as H2.

4️⃣ Output Format:

JSON with title and an outline containing {level, text, page}.

## 📦 Libraries Used


pdfminer.six----	Extract text, font size, and layout information

os, json----	File handling and JSON output

re, Counter----	Regex-based heading detection and font statistics

## 📂 Project Structure
round1a/

│── input/         # Input PDFs

│── output/        # Extracted JSONs

│── extract_outline.py        # Main script

│── Dockerfile     # For container build

│── requirements.txt

│── README.md

## ⚙️ Building and Running (Docker)

🔹 1. Build the Docker Image

    docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .

🔹 2. Run the Container

    docker run --rm \

    -v $(pwd)/input:/app/input \
  
    -v $(pwd)/output:/app/output \
  
    --network none \
  
    mysolutionname:somerandomidentifier
  
## ✅ Expected Behavior

Processes all PDFs from /app/input/.

Generates corresponding JSON files in /app/output/ with extracted title and headings.

## 📄 Sample Output (example.json)
  
    {
      "title": "Sample PDF Document",
  
      "outline": [
  
      { "level": "H1", "text": "Chapter 1 Introduction", "page": 1 },
    
      { "level": "H2", "text": "1.1 Background", "page": 2 },
    
      { "level": "H3", "text": "1.1.1 History", "page": 3 }
    
    
    ]
  
      }
## 📌 Constraints Followed
✅ Works offline – no network calls.

✅ Compatible with linux/amd64.

✅ Runs on CPU only.

✅ Processes up to 50 pages in <10 sec.
