import pygame, random
from ctypes import windll
import os
windll.shcore.SetProcessDpiAwareness(1)

pygame.init()

def img():
    bank = {}
    bank["imageFond"] = pygame.image.load("background2.jpg").convert_alpha()
    bank["imageFond2"] = pygame.image.load("battleback1.png").convert_alpha()
    bank["balle"] = pygame.image.load("balle.png").convert_alpha()
    bank["imagePerso"] = pygame.image.load("perso.png").convert_alpha()
    bank["bonus"] = pygame.image.load("bonus.png").convert_alpha()
    bank["coeur"] = pygame.image.load("coeur.png").convert_alpha()
    bank["pause"] = pygame.image.load("pause.png").convert_alpha()
    bank["speed"] = pygame.image.load("speed.png").convert_alpha()
    bank["mort"] = pygame.image.load("mort.png").convert_alpha()

    return bank

def nouvelleBalle(x, y, vx, vy, bonus = 0):
	if bonus == 0:
		rect = bank['balle'].get_rect()

	if bonus == 1:
		rect = bank['bonus'].get_rect()

	if bonus == 2:
		rect = bank["coeur"].get_rect()

	if bonus == 3:
		rect = bank["speed"].get_rect()

	if bonus == 4:
		rect = bank["mort"].get_rect()

	rect.x = x
	rect.y = y
	return (rect, vx, vy, 0, bonus)


def deplacerPerso(touches, rect,hauteur,largeur):
	if touches[pygame.K_UP] and rect.y > 0:
		rect.y = monter(rect.y)

	if touches[pygame.K_DOWN] and rect.y < hauteur-rect.h:
		rect.y = descendre(rect.y)

	if touches[pygame.K_LEFT] and rect.x > 0:
		rect.x = gauche(rect.x)

	if touches[pygame.K_RIGHT] and rect.x < largeur-rect.w:
		rect.x = droite(rect.x)
	

def monter(y):
    y-=6
    return y

def descendre(y):
    y+=6
    return y

def droite(x):
    x+=6
    return x

def gauche(x):
    x-=6
    return x

i = 0
balles = []

#creation de la fenetre
largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))

bank = img()

# creation d'un rectangle pour positioner l'image du fond
rectFond = bank["imageFond"].get_rect()
rectFond.x = -420
rectFond.y = -170

# creation d'un rectangle pour positioner l'image du fond
rectFond2 = bank["imageFond2"].get_rect()
rectFond2.x = 0
rectFond2.y = 0

# creation d'un rectangle pour positioner l'image du personnage
rectPerso = bank["imagePerso"].get_rect()
rectPerso.x = 150
rectPerso.y = 100

font2 = pygame.font.Font(None, 55)
imageText2 = font2.render("Press Space to start", 1, (255, 255, 255))
rectText2 = imageText2.get_rect()
rectText2.x = 140
rectText2.y = 230

continuer = 1
horloge = pygame.time.Clock()

mon_fichier = open("./aide.txt","r")
contenue = mon_fichier.read()
state = "menu"

print(contenue)
mon_fichier.close()

while continuer:
	touches = pygame.key.get_pressed();
	events = pygame.event.get()
	horloge.tick(60)
	if state=="menu":
		i = 0
		balles = []
		vies = 10
		fenetre.blit(bank["imageFond2"], rectFond2)
		fenetre.blit(imageText2,rectText2)

		if touches[pygame.K_ESCAPE] :
			continuer=0
		if touches[pygame.K_SPACE] :
			state="jeu"
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 0))

	if state == "pause":
		# creation d'un rectangle pour positioner l'image du fond
		rectPause = bank["pause"].get_rect()
		rectPause.x = 220
		rectPause.y = 120
		fenetre.blit(bank["pause"], rectPause)

		if touches[pygame.K_SPACE] :
			state = "jeu"

	if state =="jeu":
		fenetre.blit(bank["imageFond"], rectFond)			
		font = pygame.font.Font(None, 34)
		i+=1
		balles_mortes = []
		touch = False

		imageText = font.render(str(vies), 1, (255, 255, 255))
		rectText = imageText.get_rect()
		rectText.x = 10
		rectText.y = 10

		imageText3 = font.render(str(i), 1, (255, 255, 255))
		rectText3 = imageText3.get_rect()
		rectText3.x = 10
		rectText3.y = 35

		deplacerPerso(touches,rectPerso, hauteur, largeur)
		
		# Switch mode
		if touches[pygame.K_RETURN] :
			state = "pause"

		# Deplace les balles
		for n in range(len(balles)):
			rectBalle, vx, vy, reb , bonus = balles[n]
			rebondi = False

			if rectBalle.x < 0:
				vx = abs(vx)
				rebondi = True

			if rectBalle.x +rectBalle.w > largeur :
				vx = -abs(vx)
				rebondi = True

			if rectBalle.y < 0 : 
				vy = abs(vy)
				rebondi = True

			if rectBalle.y +rectBalle.h > hauteur :
				vy = -abs(vy)
				rebondi = True

			if rebondi:
				reb += 1

			rectBalle.x+=vx
			rectBalle.y+=vy
			balles[n] = rectBalle, vx, vy, reb, bonus

		# Collisions balles Perso
		for n in range(len(balles)):
			rectBalle, vx, vy, reb , bonus = balles[n]
			if bonus == 0:
				fenetre.blit(bank["balle"], rectBalle)

			if bonus == 1:
				fenetre.blit(bank["bonus"], rectBalle)

			if bonus == 2:
				fenetre.blit(bank["coeur"], rectBalle)

			if bonus == 4:
				fenetre.blit(bank["mort"], rectBalle)

			if rectBalle.colliderect(rectPerso):
				if bonus == 1:
					balles_mortes = 'kill all'

				if bonus == 2:
					vies+=1

				if bonus == 4:
					vies-=2

				if bonus == 0:
					vies-=1 

			# Game_Over
			if vies <= 0 :
				state = "menu"

			if rectBalle.colliderect(rectPerso) and balles_mortes != 'kill all':
				balles_mortes.append(balles[n])

			if reb == 3 :
				balles_mortes.append(balles[n])

		# Nettoyage des balles out
		if balles_mortes == 'kill all':
			balles = []
			balles_mortes = []
		else:
			for b in balles_mortes:
				balles.remove(b)

		if i%100 == 0 and len(balles)<10:
		#if random.random() < 0.01 :
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 0))

		if random.random() < 0.002 :
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 1))

		if random.random() < 0.001 :
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 3))

		if random.random() < 0.001 :
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 2))

		if random.random() < 0.001 :
			balles.append(nouvelleBalle(random.randint(int(largeur/4), int(3*largeur/4)), random.randint(int(hauteur/4), int(3*hauteur/4)) ,5,5, bonus = 4))

		# On blite le tout !

		fenetre.blit(bank["imagePerso"], rectPerso)
		fenetre.blit(imageText3, rectText3)
		fenetre.blit(imageText, rectText)

	if touches[pygame.K_ESCAPE] :
		continuer=0

	for event in events:  
		if event.type == pygame.QUIT:     
			continuer = 0
	#Rafraichissement
	pygame.display.flip()

pygame.quit()