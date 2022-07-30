""" 

"""
import asyncio
import js
from js import document, FileReader
from pyodide import create_proxy
import docx
import os


def read_complete(event):
    # event is ProgressEvent
    # console.log('read_complete')

    data = event.target.result
    filename = "./doc_to_parse.docx"
    f1 = open(filename, "wb")
    f1.write(data.encode())
    document.getElementById("content").innerHTML = data.encode()
    f1.close()
    print(os.path.getsize(filename))

    # f2 = open(filename, "rb")
    import io

    f = io.BytesIO(data.encode())
    wd = docx.Document(f)
    # f2.close()
    document.getElementById("content").innerHTML = wd.paragraphs[2].text


async def process_file(event):
    # fileList = event.target.files.to_py()
    # for f in fileList:
    # data = await f.text()
    # document.getElementById("content").innerHTML = data

    fileList = document.getElementById("myfile").files
    for f in fileList:
        # reader is a pyodide.JsProxy
        reader = js.FileReader.new()
        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)
        reader.onload = onload_event
        reader.readAsBinaryString(f)


def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)
    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)

    document.getElementById("file_name").innerHTML = "Select a file"

