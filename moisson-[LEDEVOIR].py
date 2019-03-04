# coding: utf-8

# NOTES : Le site du Devoir a fait preuve de quelques caprices, dont le non-respect de la période sélectionnée dans L'URL et une certaine inconstance dans ses URL. J'ai tout de même pu retirer l'ensemble des informations que je recherchais. Bonne correction!

import csv
import requests
from bs4 import BeautifulSoup

entete = {
	"User-Agent": "Laurent Lavoie",
	"From":"laurent.lavoie96@gmail.com"
}

fichier = "misession.csv"
for onglets in range(1, 10000) :
	url = "https://www.ledevoir.com/recherche/{onglets}?tri=date_asc&section_id=&expression=&tri_widget=date_asc&tri_widget=date_asc&date=depuis_1998&format=tous&section=&date_debut=2019-02-11&date_fin=2019-03-15&section=&collaborateur_nom=".format(onglets=onglets)
	#print (len(url))

	contenu = requests.get(url, headers=entete)

	page = BeautifulSoup(contenu.text, "html.parser")

	textes = (page.find_all("article"))

	for texte in textes :
			if not texte.find("a", "/lettres-la-parole-a-nos-lecteurs") :
				titre = (texte.find("h2").text)
				#print(texte.find("a")["href"])
				#descriptif = (texte.find("p").text)
				date = (texte.find("time").text[-15:])
				auteur = (texte.find("span").find_next("").text) 
				section = (texte.find("span").find_next(class_="section").text)
				infos =  [titre, date, auteur, section]
				print(infos)
				print("*"*30)
				#Agences = ["Agence France-Presse", "Associated Presse", "La Presse canadienne", "Reuters"]
					#for Agence in infos : 
						#print(Agence)

			f2 = open(fichier,"a")
			final = csv.writer(f2)
			final.writerow(infos)

#if not texte.find("span", "Rectificatif", class_="sans-datetime") :

#n = 0

#		for Agences in infos : 
#			n += 1
#			print(Agences)


# Pour avoir les bons caractères : .encode("latin-1").decode("utf-8")

# print()
# print(len(page.find_all("article", class_="has-img"))) #une virgule signifie nouvel élément. Pour que class marche, il faut mettre une barre de soulignement
# #pour avoir toute la liste, mettre "find_all"
# print()

