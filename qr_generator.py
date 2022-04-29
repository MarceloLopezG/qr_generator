from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import *
from PIL import Image
import tkinter as tk
import validators
import requests
import qrcode
import os

# pip install validators
# pip install Pillow
# pip install qrcode
# pip install tk

root = tk.Tk()
root.geometry("480x370")  # Size of the window 
root.title('QR-Generator')


def getInputs():
	web = input_url_web.get(1.0, "end-1c")
	logo = input_url_logo.get(1.0, "end-1c")

	valid_url_web=validators.url(web)
	valid_url_logo=validators.url(logo)
	is_valid = True

	if len(web) == 0 and len(logo) == 0:
		lbl.config(text = "Ingrese el enlace de su sitio web y logo.", foreground="red")
		is_valid = False
		return False
	else:
		if valid_url_web == True :
			pass
		else:
			lbl.config(text = "El enlace de su web no es válido.", foreground="red")
			is_valid = False
			return False

		if valid_url_logo == True :
			pass
		else:
			lbl.config(text = "El enlace de su logo no es válido.", foreground="red")
			is_valid = False
			return False

		if web == logo:
			lbl.config(text = "El enlace de su web y logo, no deben ser iguales.", foreground="red")
			is_valid = False
			return False

	
		if is_valid == True:
			lbl.config(text = "")
			qr_generator(web, logo)





def qr_generator(url_web, url_logo):
	try:
		path_to_save = filedialog.askdirectory()
		if path_to_save == None or path_to_save == '':
			lbl.config(text = "Seleccione un destino para guardar el archivo.", foreground="red")
		else:
			QRcolor = '#050505' # Taking color
			logo = Image.open(requests.get(url_logo, stream=True).raw) # Open url file
			basewidth = 100 # Taking base width

			# Adjust image size
			wpercent = (basewidth/float(logo.size[0]))
			hsize = int((float(logo.size[1])*float(wpercent)))
			logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
			QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

			QRcode.add_data(url_web) # Adding URL or text to QRcode
			QRcode.make() # Generating QR code

			# Adding color to QR code
			QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB')

			# Set size of QR code
			pos = ((QRimg.size[0] - logo.size[0]) // 2,	(QRimg.size[1] - logo.size[1]) // 2)
			QRimg.paste(logo, pos)

			# Save the QR code generated
			QRimg.save(path_to_save + '/qr_name_generated.png')
			lbl.config(text = "¡Se generó el código QR con éxito!", foreground="black") 
	except Exception as e:
		lbl.config(text = "¡Ha ocurrido un error!, inténtelo de nuevo y verifique sus enlaces.", foreground="red")
		return False
	

# Label message
label = tk.Label(root,text='Generar código QR', width=50, font=('times', 18, 'bold'), padx=20, pady=20).pack()  
# Label Creation
label_web = tk.Label(root, text="Enlace del sitio web", anchor='w', padx=10, pady=7, height=1, width=60).pack()

# TextBox Creation
input_url_web = scrolledtext.ScrolledText(root, height=1, width=50, padx=10, pady=10)
input_url_web.pack()

# Label Creation
label_web = tk.Label(root, text="Enlace del logo", anchor='w', padx=10, pady=7, height=1, width=60).pack()
# TextBox Creation
input_url_logo = scrolledtext.ScrolledText(root, height=1, width=50, padx=10, pady=10)
input_url_logo.pack()


label_btn = tk.Label(root, text="", anchor='w', pady=1).pack()
# Button Creation
printButton = tk.Button(root,text = "Generar QR", pady=5, font=('times', 10, 'bold'),command = getInputs)
printButton.pack()


lbl = tk.Label(root, text = "", anchor='w', padx=10, pady=8, height=1, width=70, font=('times', 12))
lbl.pack()
root.mainloop() # Keep the window open


if __name__=='__main':
    getInputs()