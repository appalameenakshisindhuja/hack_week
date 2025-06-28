#!/usr/bin/env python3
"""
Markdown to HTML Converter
A command-line tool that converts Markdown files to clean HTML files.
"""

import re
import sys
import argparse
from pathlib import Path


class MarkdownToHtml:
    def __init__(self):
        self.html_content = []
        self.in_code_block = False
        self.in_list = False
        self.list_type = None
        self.list_level = 0
    
    def convert_inline_formatting(self, text):
        """Convert inline Markdown formatting to HTML."""
        # Code blocks (backticks) - handle first to avoid conflicts
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Bold (**text** or __text__)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italics (*text* or _text_)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        
        # Links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Images ![alt](url)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
        
        # Strikethrough ~~text~~
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        
        return text
    
    def process_headers(self, line):
        """Process header lines (#, ##, ###, etc.)."""
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            text = self.convert_inline_formatting(header_match.group(2))
            return f'<h{level}>{text}</h{level}>'
        return None
    
    def process_lists(self, line):
        """Process ordered and unordered lists."""
        # Unordered list (-, *, +)
        unordered_match = re.match(r'^(\s*)([-*+])\s+(.+)$', line)
        if unordered_match:
            indent = len(unordered_match.group(1))
            text = self.convert_inline_formatting(unordered_match.group(3))
            
            if not self.in_list or self.list_type != 'ul':
                if self.in_list:
                    self.html_content.append(f'</{self.list_type}>')
                self.html_content.append('<ul>')
                self.in_list = True
                self.list_type = 'ul'
            
            return f'<li>{text}</li>'
        
        # Ordered list (1., 2., 3., etc.)
        ordered_match = re.match(r'^(\s*)(\d+\.)\s+(.+)$', line)
        if ordered_match:
            indent = len(ordered_match.group(1))
            text = self.convert_inline_formatting(ordered_match.group(3))
            
            if not self.in_list or self.list_type != 'ol':
                if self.in_list:
                    self.html_content.append(f'</{self.list_type}>')
                self.html_content.append('<ol>')
                self.in_list = True
                self.list_type = 'ol'
            
            return f'<li>{text}</li>'
        
        # Not a list item, close any open list
        if self.in_list:
            self.html_content.append(f'</{self.list_type}>')
            self.in_list = False
            self.list_type = None
        
        return None
    
    def process_code_blocks(self, line):
        """Process code blocks (```language)."""
        if line.strip().startswith('```'):
            if not self.in_code_block:
                # Starting code block
                lang = line.strip()[3:].strip()
                if lang:
                    self.html_content.append(f'<pre><code class="language-{lang}">')
                else:
                    self.html_content.append('<pre><code>')
                self.in_code_block = True
                return True
            else:
                # Ending code block
                self.html_content.append('</code></pre>')
                self.in_code_block = False
                return True
        
        if self.in_code_block:
            # Inside code block, don't process formatting
            self.html_content.append(line)
            return True
        
        return False
    
    def process_horizontal_rule(self, line):
        """Process horizontal rules (---, ***, ___)."""
        if re.match(r'^(\*{3,}|-{3,}|_{3,})$', line.strip()):
            return '<hr>'
        return None
    
    def process_blockquotes(self, line):
        """Process blockquotes (> text)."""
        blockquote_match = re.match(r'^>\s+(.+)$', line)
        if blockquote_match:
            text = self.convert_inline_formatting(blockquote_match.group(1))
            return f'<blockquote><p>{text}</p></blockquote>'
        return None
    
    def process_paragraph(self, line):
        """Process regular paragraphs."""
        if line.strip():
            text = self.convert_inline_formatting(line)
            return f'<p>{text}</p>'
        return None
    
    def convert_markdown_to_html(self, markdown_content):
        """Convert Markdown content to HTML."""
        lines = markdown_content.split('\n')
        self.html_content = []
        self.in_code_block = False
        self.in_list = False
        
        for line in lines:
            # Skip empty lines unless in code block
            if not line.strip() and not self.in_code_block:
                continue
            
            # Process code blocks first
            if self.process_code_blocks(line):
                continue
            
            # Process other elements
            html_line = None
            
            # Headers
            html_line = self.process_headers(line)
            if html_line:
                self.html_content.append(html_line)
                continue
            
            # Lists
            html_line = self.process_lists(line)
            if html_line:
                self.html_content.append(html_line)
                continue
            
            # Horizontal rules
            html_line = self.process_horizontal_rule(line)
            if html_line:
                self.html_content.append(html_line)
                continue
            
            # Blockquotes
            html_line = self.process_blockquotes(line)
            if html_line:
                self.html_content.append(html_line)
                continue
            
            # Regular paragraphs
            html_line = self.process_paragraph(line)
            if html_line:
                self.html_content.append(html_line)
        
        # Close any remaining open lists
        if self.in_list:
            self.html_content.append(f'</{self.list_type}>')
        
        return '\n'.join(self.html_content)
    
    def create_complete_html(self, body_content, title="Converted Document"):
        """Create a complete HTML document with proper structure."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        h1 {{ font-size: 2em; }}
        h2 {{ font-size: 1.5em; }}
        h3 {{ font-size: 1.25em; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        hr {{
            border: none;
            height: 1px;
            background-color: #ddd;
            margin: 2em 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        li {{
            margin: 0.5em 0;
        }}
    </style>
</head>
<body>
{body_content}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s input.md                    # Creates input.html
  %(prog)s input.md -o output.html     # Creates output.html
  %(prog)s input.md --title "My Doc"   # Sets HTML title
        '''
    )
    
    parser.add_argument('input_file', help='Input Markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file (defaults to input filename with .html extension)')
    parser.add_argument('-t', '--title', help='HTML document title (defaults to filename)')
    parser.add_argument('--no-css', action='store_true', help='Generate HTML without embedded CSS')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.md':
        print(f"Warning: Input file doesn't have .md extension")
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.html')
    
    # Determine title
    title = args.title or input_path.stem
    
    try:
        # Read Markdown file
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        converter = MarkdownToHtml()
        html_body = converter.convert_markdown_to_html(markdown_content)
        
        # Create complete HTML document
        if args.no_css:
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{html_body}
</body>
</html>"""
        else:
            html_content = converter.create_complete_html(html_body, title)
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Successfully converted '{input_path}' to '{output_path}'")
        
    except FileNotFoundError:
        print(f"Error: Could not read file '{input_path}'", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()