""" 

"""
import asyncio
import js
from js import document, FileReader
from pyodide import create_proxy
import docx


def read_complete(event):
    # event is ProgressEvent
    # console.log('read_complete')
    print("Create a file, read the file and print the contents:")
    f = open("docfile.docx", "w")

    data = event.target.result
    document.getElementById("content").innerHTML = data

    f.write(data)
    document.getElementById("file_name").innerHTML = "docfile.docx"
    f.close()
    f = open("docfile.docx", "rb")
    wd = docx.Document(f)
    f.close()
    document.getElementById("content").innerHTML = wd.paragraphs[2].text

    f.close()


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
        print("Setting up reader")


def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)
    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)

    document.getElementById("file_name").innerHTML = "Select a file"

