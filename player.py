import pygame
import os

pygame.init()
pygame.mixer.init()

# Fenêtre
largeur_fenetre, hauteur_fenetre = 800, 400
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Lecteur Audio")

# Couleurs
BLANC, NOIR = (255, 255, 255), (0, 0, 0)

# Police
police = pygame.font.Font(None, 36)

# Répertoire audio et volume
repertoire_audio = "C:\\Users\\malik\\Documents\\playerMusic\\musique"
fichiers_audio = [f for f in os.listdir(repertoire_audio) if f.endswith(('.mp3', '.wav'))]
chemins_audio = [os.path.join(repertoire_audio, fichier) for fichier in fichiers_audio]
pygame.mixer.music.set_volume(1)

# Boutons et images
def charger_image(nom, taille):
    image = pygame.image.load(nom)
    return pygame.transform.scale(image, taille)

image_bouton_pause = charger_image("pause.png", (100, 100))
image_bouton_play = charger_image("play.png", (100, 100))
image_volume_up = charger_image("plus.png", (50, 50))
image_volume_down = charger_image("moins.png", (50, 50))
image_bouton_loop = charger_image("loop.png", (50, 50))
image_bouton_supprimer = charger_image("supp.png", (50, 50))
image_bouton_ajouter = charger_image("ajouter.png", (50, 50))

# Positions des boutons
x_ajouter, y_ajouter = 5, hauteur_fenetre - 55
x_supprimer, y_supprimer = x_ajouter + 65, y_ajouter

# Rectangles des boutons
rect_bouton_pause = image_bouton_pause.get_rect(topleft=(250, 200))
rect_bouton_play = image_bouton_play.get_rect(topleft=(rect_bouton_pause.right + 10, 200))
rect_bouton_volume_up = image_volume_up.get_rect(topleft=(rect_bouton_play.right + 10, 200))
rect_bouton_volume_down = image_volume_down.get_rect(topleft=(rect_bouton_volume_up.right + 10, 200))
rect_bouton_loop = image_bouton_loop.get_rect(topleft=(rect_bouton_volume_down.right + 10, 200))
rect_bouton_ajouter = image_bouton_ajouter.get_rect(topleft=(x_ajouter, y_ajouter))
rect_bouton_supprimer = image_bouton_supprimer.get_rect(topleft=(x_supprimer, y_supprimer))

# État de lecture et boucle
en_lecture, en_boucle = False, False

# Fonctions
def toggle_loop():
    global en_boucle
    en_boucle = not en_boucle
    if en_boucle:
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    else:
        pygame.mixer.music.set_endevent(0)

def jouer_audio(index):
    global en_lecture
    pygame.mixer.music.load(chemins_audio[index])
    pygame.mixer.music.play()
    en_lecture = True


def ajuster_volume(modification):
    volume_actuel = pygame.mixer.music.get_volume()
    nouveau_volume = min(1, max(0, volume_actuel + modification))
    pygame.mixer.music.set_volume(nouveau_volume)

def ajouter_piste():
    nouveau_fichier = demander_fichier_audio()
    if nouveau_fichier:
        fichiers_audio.append(os.path.basename(nouveau_fichier))
        chemins_audio.append(nouveau_fichier)

def supprimer_piste(index):
    if 0 <= index < len(fichiers_audio):
        del fichiers_audio[index]
        del chemins_audio[index]

def demander_fichier_audio():
    pygame.mixer.stop()
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        fichier = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])

    except Exception as e:
        print(f"Erreur lors de la sélection du fichier : {e}")
        fichier = None

    return fichier

def afficher_liste():
    fenetre.fill(BLANC)
    y = 50
    for fichier in fichiers_audio:
        texte = police.render(fichier, True, NOIR)
        fenetre.blit(texte, (50, y))
        y += 40

    pause_play_bouton = image_bouton_pause if en_lecture else image_bouton_play

    fenetre.blit(pause_play_bouton, rect_bouton_pause.topleft)
    fenetre.blit(image_volume_up, rect_bouton_volume_up.topleft)
    fenetre.blit(image_volume_down, rect_bouton_volume_down.topleft)
    fenetre.blit(image_bouton_loop, rect_bouton_loop.topleft)
    fenetre.blit(image_bouton_ajouter, rect_bouton_ajouter.topleft)
    fenetre.blit(image_bouton_supprimer, rect_bouton_supprimer.topleft)

    pygame.display.flip()

def toggle_pause():
    global en_lecture
    if en_lecture:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    en_lecture = not en_lecture

# Boucle principale
running = True
selected_index = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i, _ in enumerate(fichiers_audio):
                if 50 <= x <= 550 and 50 + i * 40 <= y <= 50 + (i + 1) * 40:
                    selected_index = i
                    jouer_audio(selected_index)
                    break
            if rect_bouton_pause.collidepoint(x, y):
                toggle_pause()
            elif rect_bouton_loop.collidepoint(x, y):
                toggle_loop()
            elif rect_bouton_volume_up.collidepoint(x, y):
                ajuster_volume(0.1)
            elif rect_bouton_volume_down.collidepoint(x, y):
                ajuster_volume(-0.1)
            elif rect_bouton_ajouter.collidepoint(x, y):
                ajouter_piste()
            elif rect_bouton_supprimer.collidepoint(x, y):
                if selected_index is not None:
                    supprimer_piste(selected_index)
        
        elif event.type == pygame.constants.USEREVENT:
            if not en_boucle:
                en_lecture = False
                selected_index = None

    if en_lecture and not pygame.mixer.music.get_busy():
        if en_boucle:
            jouer_audio(selected_index)
        else:
            en_lecture = False
            selected_index = None

    afficher_liste()

pygame.quit()
