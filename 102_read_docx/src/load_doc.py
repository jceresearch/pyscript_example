""" 

"""

import asyncio
from js import document, FileReader, Uint8Array, console, Blob, window
from pyodide import create_proxy
from pyodide_js import FS
import docx
import os
import io
import parse_doc
import pandas as pd


async def load_file(event):

    fileList = event.target.files.to_py()
    if not os.path.exists("rules.xlsx"):
        console.log("No rules file found")
        return
    for f in fileList:
        data = Uint8Array.new(await f.arrayBuffer())
        with open("doc.docx", "wb") as outb:
            outb.write(bytearray(data))
    wd = docx.Document("doc.docx")
    RULE_DICT = pd.read_excel("rules.xlsx").to_dict(orient="records")
    res = parse_doc.parse_doc(wd, RULE_DICT)
    wd.save("doc.docx")
    document.getElementById("content").innerText += (
        "\n" + res + "\n" + "Ready to download"
    )
    blob = Blob.new([FS.readFile("doc.docx")])
    url = window.URL.createObjectURL(blob)
    element = document.createElement("a")
    element.innerHTML = "Download file"
    element.href = url
    element.download = "doc.docx"
    document.getElementById("download_links").appendChild(element)


async def load_rule(event):
    fileList = event.target.files.to_py()
    for f in fileList:
        data = Uint8Array.new(await f.arrayBuffer())
        with open("rules.xlsx", "wb") as outb:
            outb.write(bytearray(data))
            document.getElementById("content").innerText += "Rules loaded"


def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(load_file)
    # Set the listener to the callback
    e1 = document.getElementById("docfile")
    e1.addEventListener("change", file_event, False)

    file_event2 = create_proxy(load_rule)
    # Set the listener to the callback
    e2 = document.getElementById("rulefile")
    e2.addEventListener("change", file_event2, False)
