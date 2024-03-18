import os
import random
from PIL import Image
import cv2

lsid= []

for i in range(1,1000):

  bk= random.randint(1, 23)
  bd= random.randint(1, 12)
  by= random.randint(1, 23)
  ey= random.randint(1, 26)
  ht= random.randint(1, 16)
  mt= random.randint(1, 15)
  ac= random.randint(1, 34)

  if (f"{bk}{bd}{by}{ey}{ht}{mt}{ac}") not in lsid:

    background= Image.open (f"./background/background_{bk}.png")
    bod= Image.open (f"./bod/bod_{bd}.png")
    body= Image.open (f"./body/body_{by}.png")
    eye= Image.open (f"./eye/eye_{ey}.png")
    hat= Image.open (f"./hat/hat_{ht}.png")
    mouth= Image.open (f"./mouth/mouth_{mt}.png")
    access= Image.open (f"./access/access_{ac}.png")

    background.paste(bod, (0, 0), bod)
    background.paste(body, (0, 0), body)
    background.paste(eye, (0, 0), eye)
    background.paste(hat, (0, 0), hat)
    background.paste(mouth, (0, 0), mouth)
    background.paste(access, (0, 0), access)


    background.save(f"./outputs/{i}.png")

    png_img = cv2.imread(f"./outputs/{i}.png")

    cv2.imwrite(f"./output2/{i}.jpg", png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    lsid.append(f"{bk}{bd}{by}{ey}{ht}{mt}{ac}")

  else:
  
    print("jjjj")

print(len(lsid))
print("now")
