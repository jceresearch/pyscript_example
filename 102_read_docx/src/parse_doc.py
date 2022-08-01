""" 

"""
import asyncio
import js
from js import document, FileReader, Uint8Array
from pyodide import create_proxy
import docx
import os
import io


async def process_file(event):

    fileList = event.target.files.to_py()
    for f in fileList:
        data = Uint8Array.new(await f.arrayBuffer())
        with open("doc.docx", "wb") as outb:
            outb.write(bytearray(data))
        wd = docx.Document("doc.docx")
        document.getElementById("file_name").innerHTML = f.name
        document.getElementById("content").innerHTML = wd.paragraphs[3].text


def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)
    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)

