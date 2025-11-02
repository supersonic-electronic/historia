#!/usr/bin/env python3
"""
Combine Polish text files into a nicely formatted HTML
"""
from pathlib import Path
import re

def combine_polish_to_html(polish_dir, output_file):
    """
    Create HTML from Polish folder text files
    """
    polish_path = Path(polish_dir)

    # Find all TXT files in polish folder
    txt_files = sorted(polish_path.glob("part_*.txt"))

    if not txt_files:
        print("No TXT files found in polish folder!")
        return

    print(f"Found {len(txt_files)} TXT files in polish folder")
    print(f"Creating HTML: {output_file}")
    print("="*70)

    # Calculate total words
    total_words = 0
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            total_words += len(content.split())

    # Create HTML structure
    html_content = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pinḳes Ṿashilḳoṿer yizker bukh - Księga Pamięci Wasilkowa</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            background-color: #f5f5f5;
            color: #333;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .ai-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 0.9em;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }

        .back-home {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            font-size: 0.95em;
        }

        .back-home:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateX(-3px);
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .info-box {
            background: white;
            padding: 30px;
            margin-bottom: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }

        .info-box h2 {
            color: #764ba2;
            margin-bottom: 15px;
        }

        .info-box p {
            color: #666;
            line-height: 1.8;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .stat-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            margin-top: 5px;
        }

        .content {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .section {
            margin-bottom: 50px;
            padding: 30px;
            background: #fafafa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            margin: 0 0 20px 0;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .section-content {
            padding: 20px;
            background: white;
            border-radius: 5px;
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 16px;
            line-height: 1.8;
            white-space: pre-wrap;
        }

        .toc {
            background: white;
            padding: 30px;
            margin-bottom: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto;
        }

        .toc h2 {
            color: #764ba2;
            margin-bottom: 20px;
            position: sticky;
            top: 0;
            background: white;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .toc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }

        .toc-link {
            display: block;
            padding: 12px;
            background: #f8f9fa;
            color: #764ba2;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
            text-align: center;
        }

        .toc-link:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }

        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            font-weight: bold;
        }

        .back-to-top:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        }

        .footer {
            background: #764ba2;
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-top: 60px;
        }

        @media print {
            body {
                background: white;
            }
            .header, .toc, .back-to-top, .footer, .back-home {
                display: none;
            }
            .container {
                max-width: 100%;
            }
            .section {
                page-break-inside: avoid;
            }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }
            .stats {
                grid-template-columns: 1fr;
            }
            .toc-grid {
                grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
            }
            .back-home {
                position: static;
                display: inline-block;
                margin-bottom: 15px;
                font-size: 0.85em;
                padding: 8px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="index.html" class="back-home">← Powrót do strony głównej</a>
        <h1>📖 Pinḳes Ṿashilḳoṿer yizker bukh</h1>
        <p>Księga Pamięci Wasilkowa</p>
        <div class="ai-badge">✨ Tłumaczenie polskie z jidysz</div>
    </div>

    <div class="container">
        <div class="info-box">
            <h2>📚 O tym dokumencie</h2>
            <p>
                To jest polska wersja <strong>Księgi Pamięci Wasilkowa</strong> (Pinḳes Ṿashilḳoṿer yizker bukh),
                dokumentującej historię i życie społeczności żydowskiej w Wasilkowie przed i podczas Holokaustu.
            </p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">""" + str(len(txt_files)) + """</div>
                    <div class="stat-label">Części</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">~""" + f"{total_words:,}".replace(',', ' ') + """</div>
                    <div class="stat-label">Słów</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">508</div>
                    <div class="stat-label">Stron (oryginał)</div>
                </div>
            </div>
            <p style="margin-top: 20px; color: #666;">
                <strong>Tytuł oryginalny:</strong> Pinḳes Ṿashilḳoṿer yizker bukh<br>
                <strong>Język oryginalny:</strong> Jidysz<br>
                <strong>Redakcja:</strong> Leon Mendelewicz<br>
                <strong>Wydawca:</strong> New York Public Library Digital Collections<br>
                <strong>URL oryginału:</strong> <a href="https://digitalcollections.nypl.org/items/c796c490-0c99-0133-f442-58d385a7bbd0" target="_blank">NYPL Digital Collections</a>
            </p>
        </div>

        <div class="toc">
            <h2>📑 Spis Treści - Szybka Nawigacja</h2>
            <div class="toc-grid">
"""

    # Add table of contents
    for i, txt_file in enumerate(txt_files, 1):
        part_num = txt_file.stem.replace('part_', '')
        html_content += f"""                <a href="#section-{part_num}" class="toc-link">Część {part_num}</a>
"""

    html_content += """            </div>
        </div>

        <div class="content">
"""

    # Add sections from text files
    for txt_file in txt_files:
        part_num = txt_file.stem.replace('part_', '')

        # Read the file content
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        print(f"Processing: {txt_file.name} - {len(content)} chars, {len(content.split())} words")

        html_content += f"""            <div class="section" id="section-{part_num}">
                <div class="section-header">Część {part_num}</div>
                <div class="section-content">{content if content else '[Brak treści w tej części]'}</div>
            </div>
"""

    html_content += """        </div>
    </div>

    <a href="#" class="back-to-top">↑ Góra</a>

    <div class="footer">
        <p><strong>Pinḳes Ṿashilḳoṿer yizker bukh</strong> - Księga Pamięci Wasilkowa</p>
        <p style="margin-top: 10px; opacity: 0.8;">Dokumentacja historii społeczności żydowskiej Wasilkowa</p>
        <p style="margin-top: 5px; opacity: 0.6; font-size: 0.9em;">
            יזכור - Pamiętaj
        </p>
    </div>
</body>
</html>"""

    # Write to file
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size = output_path.stat().st_size / 1024

    print("="*70)
    print(f"\n✓ HTML file created!")
    print(f"  File: {output_file}")
    print(f"  Size: {file_size:.1f} KB")
    print(f"  Parts: {len(txt_files)}")
    print(f"  Total words: ~{total_words:,}")

if __name__ == "__main__":
    polish_dir = Path("/home/jin23/Code/Yizkor/polish")
    output_file = Path("/home/jin23/Code/Yizkor/wasilkow-yizkor.html")

    print("="*70)
    print("Create HTML from Polish Folder")
    print("="*70)

    combine_polish_to_html(polish_dir, output_file)

    print("\n✓ Done!")
