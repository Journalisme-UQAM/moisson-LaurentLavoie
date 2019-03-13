# coding: utf-8

### Très bon script!
### Une bonne idée de départ, bien matérialisée par ton script.
### Ce dernier, cependant, plante après avoir recueilli 559 articles seulement (voir ci-dessous ce qui se passe)

# NOTES : Le site du Devoir a fait preuve de quelques caprices, dont le non-respect de la période sélectionnée dans L'URL et une certaine inconstance dans ses URL. J'ai tout de même pu retirer l'ensemble des informations que je recherchais. Bonne correction!

import csv
import requests
from bs4 import BeautifulSoup

entete = {
	"User-Agent": "Laurent Lavoie",
	"From":"laurent.lavoie96@gmail.com"
}

fichier = "misession.csv"
fichier = "misession_JHR.csv" ### Je crée ce fichier pour que tu voies ce qui est recueilli avec mes corrections.
for onglets in range(1, 10000) :
	url = "https://www.ledevoir.com/recherche/{onglets}?tri=date_asc&section_id=&expression=&tri_widget=date_asc&tri_widget=date_asc&date=depuis_1998&format=tous&section=&date_debut=2019-02-11&date_fin=2019-03-15&section=&collaborateur_nom=".format(onglets=onglets)
	#print (len(url))

	contenu = requests.get(url, headers=entete)

	page = BeautifulSoup(contenu.text, "html.parser")

	textes = (page.find_all("article"))

	for texte in textes :
		### Il y avait une indentation de trop
		# if not texte.find("a", "/lettres-la-parole-a-nos-lecteurs"): ### On trouve quand même des textes de lettres dans le fichier csv... Excluons-les plus tard, juste avant d'enregistrer le CSV
		if not texte.find("h2", class_="sans-datetime"): ### Il faut quand même mettre cette condition pour contourner une erreur survenant à la page 109 des résultats
			titre = (texte.find("h2").text)
			#print(texte.find("a")["href"])
			#descriptif = (texte.find("p").text)

			### Ici, il se passait des drôles de choses. Le numéro du résultat de recherche (qui se trouve dans un «span») est parfois amalgamé à la date
			### et ça donne des trucs comme «16036 mars 2019»
			### Voici une façon de contourner ce problème

			numResultat = texte.find("span").text
			# print(numResultat) ### Une autre info intéressante à ajouter au CSV

			if numResultat in texte.find("time").text:
				date = texte.find("time").text.replace(numResultat,"")
			else:
				date = texte.find("time").text

			auteur = (texte.find("span").find_next("").text)
			### Il y a beaucoup de «cochonneries» dans ta colonne «auteur»: des «pipes» | et des «returns»
			### Nettoyons le tout ainsi:
			auteur = auteur.replace("|","").replace("\n","").replace("  "," ").strip()

			### C'est à la ligne suivante que ton script plante.
			### Il arrive parfois qu'il n'y ait pas de «span» de classe «section»
			### Je mets cette ligne en commentaires
			# section = (texte.find("span").find_next(class_="section").text)

			### Et je te propose plutôt d'aller chercher l'info l'URL de l'article, pcq il contient de l'info pertinente

			urlArticle = texte.find("h2").a["href"]

			goodies = urlArticle.split("/")
			# print(goodies)
			section = goodies[1]

			### Ici, on peut choisir ce qu'on garde ou pas
			### On veut exclure:
				### Les «La parole à nos lecteurs» et tous les autres éléments «non classés»
				### Les résultats qui sont des liens vers les pages de tous les articles d'un auteur donné
				### Le contenu commandité ou la section «Bis» (des publireportages)
			### On peut le faire avec cette condition:
			if "/non-classe/" not in urlArticle and "/auteur/" not in urlArticle and "/contenu-commandite/" not in urlArticle and "/bis/" not in urlArticle:

				infos =  [numResultat,titre, date, auteur, section, urlArticle] ### Ici, j'ajoute l'URL de l'article, même s'il manque le http://www.ledevoir.com avant
				print(infos)
				print("*"*30)

				#Agences = ["Agence France-Presse", "Associated Presse", "La Presse canadienne", "Reuters"]
					#for Agence in infos : 
						#print(Agence)

### L'écriture de ton fichier était mal indentée...
				f2 = open(fichier,"a")
				final = csv.writer(f2)
				final.writerow(infos)

### Enfin, il est toujours bien que ce qu'on fait afficher dans le terminal nous donne une indication de l'endroit où on est rendu

	print("On est rendu à la page {}".format(onglets))


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

