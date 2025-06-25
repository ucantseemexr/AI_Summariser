from docx import Document
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image, ImageDraw, ImageFont
import io
from transformers import TableTransformerForObjectDetection, DetrImageProcessor
import torch
import requests
import os

def iter_block_items(parent):
    """
    Yield paragraphs and tables in the order they appear in the document.
    """
    for child in parent.element.body.iterchildren():
        if child.tag.endswith('tbl'):
            yield Table(child, parent)
        elif child.tag.endswith('p'):
            yield Paragraph(child, parent)

def extract_docx_content(path):
    doc = Document(path)
    content = []

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                content.append({"type": "paragraph", "text": text})
        elif isinstance(block, Table):
            rows = []
            for row in block.rows:
                cells = [
                    cell.text.strip() if cell.text.strip() else "Empty Cell"
                    for cell in row.cells
                ]
                rows.append(cells)
            content.append({"type": "table", "rows": rows})
    print(content)
    return content
