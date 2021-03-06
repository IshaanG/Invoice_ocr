import os
import converter
import  constants
import run_ocr
import preproces
import extraction 
import tables
import converter
from tkinter import Tk, Entry, Frame, LabelFrame, Label, Button, END
import numpy as np
import xlsxwriter


filename=constants.filename
cur_path= os.getcwd() 
joined_path=os.path.join(cur_path,"Details\\"+filename)
try:
    os.mkdir(joined_path)
except OSError as er:
    print("-----Directory for "+filename+" detected----------")
try:
    os.mkdir(os.path.join(joined_path,'Pages'))
    os.mkdir(os.path.join(joined_path,'Intermediates'))
    os.mkdir(os.path.join(joined_path,'Rows'))
except OSError as er:
    print("-----Directory for "+filename+" detected----------")
if filename.split(".")[-1]=="pdf":
    converter.convert_to_jpeg(cur_path+"\\example\\"+filename,joined_path+"\\Pages")
else:
    converter.in_jpeg(cur_path+"\\example\\"+filename,joined_path+"\\Pages")

preproces.box_extraction(joined_path+"\\Pages\\page1.jpg")
run_ocr.run_tesseract()
buyer, seller, invoice= extraction.get_details()
array= tables.get_data()

root = Tk()

# keep track of widgets
seller_tk = np.empty(seller.shape, dtype=object)
buyer_tk = np.empty(buyer.shape, dtype=object)
invoice_tk = np.empty(invoice.shape, dtype=object)
array_tk = np.empty(array.shape, dtype=object)

# top frame ----------
topframe = Frame(root)
topframe.pack()

# seller details
frame0 = LabelFrame(topframe, text="seller details")
frame0.grid(row=0, column=0)
rows = seller.shape[0]
for i in range(rows):
    l = Label(frame0, text=seller[i][0])
    l.grid(row=i, column=0)
    seller_tk[i][0] = l
    e = Entry(frame0)
    e.grid(row=i, column=1)
    e.insert(END, seller[i][1])
    seller_tk[i][1] = e

# buyer details
frame1 = LabelFrame(topframe, text="buyer details")
frame1.grid(row=0, column=1)
rows = buyer.shape[0]
for i in range(rows):
    l = Label(frame1, text=buyer[i][0])
    l.grid(row=i, column=0)
    buyer_tk[i][0] = l
    e = Entry(frame1)
    e.grid(row=i, column=1)
    e.insert(END, buyer[i][1])
    buyer_tk[i][1] = e

# invoice details
frame2 = LabelFrame(topframe, text="invoice details")
frame2.grid(row=0, column=2)
rows = invoice.shape[0]
for i in range(rows):
    l = Label(frame2, text=invoice[i][0])
    l.grid(row=i, column=0)
    invoice_tk[i][0] = l
    e = Entry(frame2)
    e.grid(row=i, column=1)
    e.insert(END, invoice[i][1])
    invoice_tk[i][1] = e


# bottom frame ----------
# insert table into the grid
bottomframe = LabelFrame(root, text="transactions")
bottomframe.pack()
rows = array.shape[0]
cols = array.shape[1]
for i in range(rows):
    for j in range(cols):
        e = Entry(bottomframe)
        e.grid(row=i, column=j)
        e.insert(END, array[i][j])
        array_tk[i][j] = e

# functions
# generate xls file from the data in present in tk entries

path_to_write= os.getcwd()+"/Details/"+filename
def genxlsx():
    workbook = xlsxwriter.Workbook(path_to_write+'/Invoice.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    max_row = 0
    for i in seller_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
    max_row = max(max_row, row)
    row = 0
    col += 4
    for i in buyer_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
        max_row = max(max_row, row)
    row = 0
    col += 4
    for i in invoice_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
    max_row = max(max_row, row)
    row = max_row + 2
    col = 0
    for i in array_tk:
        for j in i:
            worksheet.write(row, col, j.get())
            col += 1
        col = 0
        row += 1
    workbook.close()


# buttons
buttons = Frame(root)
buttons.pack()
gen = Button(buttons, text="GENERATE", fg="green", command=genxlsx)
gen.grid(row=0, column=0)
quit = Button(buttons, text="QUIT", fg="red", command=root.destroy)
quit.grid(row=0, column=1)


# mainloop
root.mainloop()
