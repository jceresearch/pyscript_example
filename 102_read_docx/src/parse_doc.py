""" 

"""
from datetime import datetime
import docx
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_COLOR_INDEX
import pandas as pd
import os


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def parse_doc(doc, RULE_DICT):
    """
    Parses a docx file and returns a list of paragraphs.
    """

    for block in iter_block_items(doc):
        # read Paragraph
        if isinstance(block, Paragraph):
            if "highlight" in block.text:
                for r in block.runs:
                    r.font.highlight_color = WD_COLOR_INDEX.YELLOW  # read table
        elif isinstance(block, Table):
            pass

    paragraph1 = doc.add_paragraph(
        "It was noted that mistakes were made"
    )  # create new paragraph
    comment = paragraph1.add_comment(
        "This is a new comment", author="Archer", initials="A"
    )  # add a comment on the entire paragraph

    result = "Process finished " + str(datetime.now())
    return result


if __name__ == "__main__":
    print("Manually executed")
    print(os.getcwd())
    os.chdir(os.path.dirname(__file__))
    file_ref = open("./test.docx", "rb")
    df_rules = pd.read_excel("./rules.xlsx")
    rules = df_rules.to_dict("index")
    print(rules[10])
    doc = docx.Document(file_ref)
    res = parse_doc(doc, rules)
    print(res)
    doc.save("./output.docx")
