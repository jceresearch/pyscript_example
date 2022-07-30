#%%
import docx

#%%
f = open("./test.docx", "rb")
wd = docx.Document(f)
print(wd.paragraphs[2].text)

# %%
