# 📝 Markdown to HTML Converter

A **comprehensive and feature-rich Markdown to HTML converter** built in Python. This tool supports all major Markdown syntax and generates clean, styled, responsive HTML documents.

---

## ✅ Supported Markdown Features

- Headers: `#`, `##`, `###`, etc. (H1–H6)
- **Bold text**: `**bold**` or `__bold__`
- *Italic text*: `*italic*` or `_italic_`
- ~~Strikethrough~~: `~~text~~`
- Inline code: `` `code` ``
- Code blocks: Triple backticks ```` ``` ```` with optional language
- Links: `[text](url)`
- Images: `![alt text](url)`
- Lists:
  - Ordered: `1.`, `2.`, `3.`
  - Unordered: `-`, `*`, `+`
- Blockquotes: `> quoted text`
- Horizontal rules: `---`, `***`, or `___`

---

## 🚀 Features

- 🧼 Clean HTML output with semantic structure
- 🎨 Optional embedded CSS for professional styling
- 🖥️ Responsive design with mobile-friendly layout
- 💡 Command-line interface with helpful options
- 🔒 Error handling for file read/write operations
- 🔧 Customizable HTML title and output path

---

## 📦 Installation

Make sure you have Python installed (Python 3.6+ recommended).


# 💻 Usage

## 🔁 for  Basic Conversion
python markdown.py mark.md

## 📤 To  Specify Output File
python markdown.py mark.md -o output.html

## 🏷️ Set Custom Title
python markdown.py mark.md --title "My Document"

## 🧼 Generate HTML Without Embedded CSS
python markdown.py mark.md --no-css

## 📁 Example
python md_to_html.py sample.md -o sample.html --title "Sample Page"

This command will:

Read sample.md

Convert to styled HTML

Save as sample.html with title "Sample Page"
