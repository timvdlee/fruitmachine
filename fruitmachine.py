# Tim 
TestMode = False
firsttime = """
Hoi, het lijkt erop dat dit de eerste keer is dat je dit script runt!
Het belangrijkste is dat je de afbeeldingen in de map img/ plaats.
Deze is net gemaakt! 
Verder kan je instellingen aanpassen door variabelen te veranderen in het script.
Dit kan vanaf line 35. 

Zorg ervoor dat pillow geinstallerd is. kan met pip install pillow
Dit commando moet door python uitgevoerd worden NIET door de standaard cmd
Maar als je pycharm ofzo gebruikt zou het moeten werekn.
START_README
Plaats in de map img de verschillende fotos van de leiding.
Zorg dat ze de naamstructuur image{i}.jpg (bijv i image1.jpg, image2.jpg etc)
zorg ervoor dat het aspect ratio 1:1 heeft. (Dus een vierkant) Groote maakt niet uit.
De eindfoto's worden in Result opgeslagen.
Deze kunnen liggen in a4 formaat worden geprint

VARIABLES
req_w_h = breedte en hoogte van elke foto (type = tuple)
offset = whitespace tussen individuele foto leiding
padding = wh itespace tussen kaartjes
p_cut = hoeveel kaartjes per a4
amount of pages = pcut*10 Hoeveel pagina's je wilt.
"""
import webbrowser

try:
    from PIL import \
        Image  # BELANGRIJK Kan geinstaleerd worden via python terminal door pip install pillow te typen
except ModuleNotFoundError:
    print(firsttime)
    raise Exception("Module Pillow niet geinstalleerd!")
import random
import os
import time
#__INTERNAL__
namedict = {}
usedict = {}
USED_SEED = time.time()
random.seed(USED_SEED)
#__END_Internal_

req_w_h = (400, 400)  # prefered size in pixels
offset = 25  # whitespaces tussen leidings op zelfde kaartje in pixels
padding = 75  # whitespace tussen verschillende kaartjes inpixels
p_cut = 8  # page_cutoff hoeveel kaartjes per pagina
amount_of_pages = p_cut * 20 # verander het getal door het aantal pagina's dat je wilt

def open_images():
    """
    Leest alle bestanden in in de map img en zet deze in een lijst
    :return: img_list. De lijst met leidingafbeeldingen.
    """
    img_list = []
    images = os.listdir("img/")
    for image in images:
        img = Image.open(f"img/{image}")
        img = img.resize(req_w_h)
        img_list.append(img)
        namedict[img.getdata()] = image
        usedict[image] = 0
    return img_list


def concat_fruit(im1, im2, im3, offset):
    """
    Voegt drie afbeeldingen van leiding samen met witruimte ertussen
    :param im1: afbeelding 1
    :param im2: afbeelding 2
    :param im3: afbeelding 3
    :param offset: whitespace tussen afbeeldingen
    :return: dst = individueel kaartje
    """
    dst = Image.new('RGB', (
    im1.width + im2.width + im3.width + offset * 2, im1.height), "WHITE")
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width + offset, 0))
    dst.paste(im3, (im1.width * 2 + offset * 2, 0))
    return dst


def create_fruitmachine(imglist, offset):
    """
    kiest 3 unieke foto's uit uit de afbeeldingenlijst en zet deze apart in een lijst
    :param imglist: De lijst met afbeeldingen
    :param offset: whitepace in pixels
    :return: lijst met 3 afbeeldignen
    """
    cho = random.sample(imglist, k=3)
    for img in cho:
        usedict[namedict[img.getdata()]] += 1
    final_img = concat_fruit(cho[0], cho[1], cho[2], offset)
    return final_img


def concat_cards_page(images, padding):
    """
    voegt de afbeeldingen in images toe aan 1 groote afbeelding
    (ongeveer) a4 groote. Hangt af van p_cut
    :param images: alle kaartjes op 1 pagina
    :param padding: afstand tussen kaartjes
    :return: de pagina in de vorm van een afbeelding
    """
    w = int((images[0].width * 2) + padding)
    h = int((images[0].height + padding) * (len(images) / 2))
    finalimg = Image.new('RGB', (w, h), "WHITE")
    i = 0
    hi = int((images[0].height + padding) * (i / 2))
    for img in images:
        wi = int((img.width + padding) * (i % 2))
        if i % 2 == 0:
            hi = int((img.height + padding) * (i / 2))
        finalimg.paste(img, (wi, hi))
        i += 1
    return finalimg


def main():
    """
    De main.
    Maakt eerst de kaartjes. Vervolgens roept knipt het de kaartjes in stukken van p_cut.
    Daarna roept het de functie aan die er aparte pagina's van maakt.
    :return:
    """
    if not os.path.exists("img") and not os.path.isdir("img"):
        print(firsttime)
        os.mkdir("img")
        raise Exception("directory img Not found")
    if not os.path.exists("Result"):
        print("Directory 'Result' does not exist. Creating.")
        os.mkdir("Result")

    img = open_images()
    images = []
    for i in range(amount_of_pages):
        images.append(create_fruitmachine(img, offset))
    pages = int(amount_of_pages / p_cut)
    final_img_list = []
    for i in range(pages):
        images_per_page = images[i * p_cut:(i * p_cut) + p_cut]
        if not images_per_page:
            break
        final_img = concat_cards_page(images_per_page, padding)
        final_img_list.append(final_img)
        # final_img.save(f"Result/Pagina{i + 1}.jpg")
    del final_img_list[-1]
    statsstring = f"USEDSEED = {USED_SEED}\n"
    for img_key in usedict:
        usage = usedict[img_key]
        #todo REMOVE
        if usage == 0:
            main()
            exit()
        statsstring+=f"Bestand: {img_key} is {usage} keer gebruikt. " \
                     f"Dit zijn {usage} van de {amount_of_pages*3} fotos. " \
                     f"({int(usage)/( amount_of_pages*3)*100}%)\n"

    statsstring += f"De normaalverdeling is {amount_of_pages*3/len(usedict)}/" \
                   f"{amount_of_pages*3}({amount_of_pages*3/len(usedict)/(amount_of_pages*3)*100}%)"
    path = os.path.abspath('Result/fruitmachine.pdf')
    print(
        f"Het script is sucessvol uitgevoerd. Er zijn {amount_of_pages / p_cut} pagina's gemaakt met elk {p_cut} kaartjes. Met in totaal {amount_of_pages} kaartjes.\nHiervoor zijn {len(img)} foto's gebruikt.\nDe kaartjes zijn te vinden in\t{path}\n\n{statsstring}")

    if not TestMode:
        final_img.save("Result/fruitmachine.pdf", save_all=True,
                       append_images=final_img_list)
        file = open("Result/stats.txt","w")
        file.write(statsstring)
        file.close()
        webbrowser.open_new_tab(path)
        webbrowser.open_new_tab(os.path.abspath('Result/stats.txt'))




if __name__ == "__main__":
    main()
