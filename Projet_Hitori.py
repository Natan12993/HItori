from upemtk import *
from copy import deepcopy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fonctions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tâche 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lire_grille(nom_fichier):
    '''
    Prend en argument une chaîne de caractères nom_fichier et renvoie une liste de listes
    décrivant les valeurs des cellules de la grille.
    '''
    niveau = open(nom_fichier, "r").read()
    lst_princ = []
    lst_inter = []
    for obj in niveau:
        if obj != ' ':
            if obj == '\n':
                lst_princ.append(lst_inter)
                lst_inter = []
            else:
                lst_inter.append(obj)
    return lst_princ

def afficher_grille(grille):
    '''
    Prend en argument une liste de listes représentant une grille, et l’affiche joliment sur
    le terminal.
    '''
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            print(grille[i][j], end=' ')
        print("")

def ecrire_grille(grille, nom_fichier):
    '''
    Prend en argument une grille sous forme de liste de listes de nombres et un nom de fichier,
    et sauvegarde la grille fournie dans le fichier indiqué, en respectant le même format.
    '''
    cache = open(nom_fichier, "w")
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            cache.write(str(grille[i][j])+" ")
        cache.write("\n")
    cache.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tâche 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sans_conflit(grille, noircies):
    '''
    Renvoie True si la règle du jeu numéro 1 est respectée, autrement dit si aucune des cellules
    visibles de la grille ne contient le même nombre qu’une autre cellule visible située sur la même
    ligne ou la même colonne, et False sinon.
    '''
    copie = deepcopy(grille)
    for element in noircies:
        (a, b) = element
        copie[a][b] = None
    copie_verticale = [[colonne[i] for colonne in copie] for i in range(len(copie[0]))]
    for i in range(len(copie)):
        for j in range(len(copie[0])):
            if copie[i][j] != None:
                if copie[i].count(copie[i][j]) > 1:
                    return False
                if copie_verticale[i].count(copie[i][j]) > 1:
                    return False
    return True

def sans_voisines_noircies(noircies):
    '''
    Renvoie True si la règle du jeu numéro 2 est respectée, autrement dit si aucune cellule noircie
    n’est voisine (par un de ses quatre bords) d’une autre cellule noircie, et False sinon.
    '''
    voisin = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for element in noircies:
        for i in range(len(voisin)):
            (a, b, c, d) = element + voisin[i]
            if (a + c, b + d) in noircies:
                return False
    return True

def connexe(grille, noircies):
    '''
    Renvoie True si la règle du jeu numéro 3 est respectée, autrement dit si les cellules visibles
    de la grille forment une seule zone (ou région, ou composante connexe), et False sinon.
    '''
    i, j = 0, 0
    set_connexe = set()
    while (i, j) in noircies:
        if j == len(grille[0]):
            i += 1
            j = 0
        else:
            j += 1
    aide_connexe(i, j, set_connexe, grille, noircies)
    if len(set_connexe)+len(noircies) == len(grille)*len(grille[0]):
        return True
    else:
        return False

def aide_connexe(i, j, set_connexe, grille, noircies):
    voisin = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    set_connexe.add((i, j))
    for k in range(len(voisin)):
        (a, b) = voisin[k]
        if 0 <= i + a < len(grille) and 0 <= j + b < len(grille[0]):
            if (i + a, j + b) not in noircies and (i + a, j + b) not in set_connexe:
                aide_connexe(i + a, j + b, set_connexe, grille, noircies)
    return set_connexe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tâche 3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dessine_plateau(taille, espace, grille):
    '''
    Dessine des rectangles permettant d'afficher graphiquement une grille. Elle permet egalemnt
    d'afficher les chiffres dans les case.
    '''
    COULEURS = ['#FFFF6B', '#BBD2E1', '#98FB98', '#E67E30',
                '#FF5E4D', '#888888', '#EE82EE', '#00FF00', '#E6E6FA']
    for i in range(len(grille[0])):
        for j in range(len(grille)):
            rectangle(i * taille + espace, j * taille + espace, (i + 1) * taille + espace,
                      (j + 1) * taille + espace, remplissage=COULEURS[int(grille[j][i])], epaisseur=2)
            texte(i * taille + espace + 22, j * taille + espace + 14, grille[j][i])
    rectangle(espace, (len(grille[0]) + 1)* taille + espace,
              espace + 2 * taille, (len(grille[0]) + 2)* taille + espace, couleur='black',
              epaisseur=3, remplissage='grey')
    rectangle((len(grille[0])- 2) * taille + espace, (len(grille[0]) + 1)* taille + espace,
              (len(grille[0])) * taille + espace, (len(grille[0]) + 2)* taille + espace,
              couleur='black', epaisseur=3, remplissage='grey')
    rectangle(320, (len(grille[0]) + 1)* taille + espace, 380,
              (len(grille[0]) + 2) * taille + espace, couleur='black', epaisseur=3, remplissage='grey')
    texte(espace + 16, (len(grille[0]) + 1)* taille + espace + 10, "Undo",
          taille=28, couleur='snow')
    texte((len(grille[0]) - 2) * taille + espace + 10, (len(grille[0]) + 1) * taille + espace + 10,
          "Reset", taille=28, couleur='snow')
    texte(332, (len(grille[0]) + 1) * taille + espace - 2, '︿', taille=28, couleur='snow')
    texte(327, (len(grille[0]) + 1) * taille + espace + 25, '︱', taille=18, couleur='snow')
    texte(350, (len(grille[0]) + 1) * taille + espace + 25, '︱', taille=18, couleur='snow')
    texte(340, (len(grille[0]) + 1) * taille + espace + 8, '_', taille=28, couleur='snow')
    texte(300, (len(grille[0]))*taille + espace + 20, "Press 'S' to solve", taille=10)

def pixel_vers_case(x, y, taille):
    '''
    Convertie les coordonnées (x, y) du clique (en pixel) à celles de la case dans laquelle on
    clique.
    '''
    return (y-espace) // taille, (x-espace) // taille

def maj_noircies(noircies, i, j):
    '''
    Met à jour l'ensemble "noircies" en ajoutant la case dans ce dernier lorsque l'on clique dessus
    et le retirant lorsqu'il est deja dans "noircies" et que l'on clique dessus.
    '''
    efface('noir')
    if (i, j) in noircies:
        noircies.remove((int(i), int(j)))
    else:
        noircies.add((int(i), int(j)))

def cases_noires(noircies, taille, espace):
    '''
    Affiche graphiquement les cases noires lorsqu'elles sont dans "noircies".
    '''
    for case in noircies:
        (j, i) = case
        rectangle(i * taille + espace, j * taille + espace, (i + 1) * taille + espace,
                  (j + 1) * taille + espace, remplissage='black', tag='noir')

def menu():
    while True:
        mise_a_jour()
        rectangle(0, 0, l, h, remplissage='#FDFD96')
        rectangle(250, 630, 450, 680, remplissage='black')
        for i in range(1, 7):
            rectangle(250, i * 90, 450, i * 90 + 50, remplissage='black')
            if i == 1:
                texte(350, i * 90 + 25, 'Test Level', couleur='white', ancrage='center', taille=16)
            else:
                texte(350, i * 90 + 25, 'Level ' + str(i - 1), couleur='white', ancrage='center', taille=16)

        # On remplie chaque rectangle du menu avec un texte qui explique chaques paramètres et
        # explique ce qu'il faut faire dans le menu pour lancer la partie et explique les différents paramètres
        texte(350, 45, 'Hitori', couleur='black', ancrage='center', taille=48)
        texte(350, 645, 'Select a level', couleur='white', ancrage='center', taille=10)
        texte(350, 665, ' and press Return', couleur='white', ancrage='center', taille=10)

        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'ClicGauche':  # A chaque fois que le joueur va selectionner avec son clic gauche un paramètre on affiche à l'écran ce que le joueur à selectionner comme paramètres de partie.
            x, y = abscisse(ev), ordonnee(ev)
            if 250 <= x <= 450:
                for i in range(1, 7):
                    if i * 90 <= y <= i * 90 + 50:
                        if i == 1:
                            texte(215, i * 90 + 53, 'Test Level Selected', couleur='red', taille=24, tag='j')
                        else:
                            texte(235, i * 90 + 53, 'Level ' + str(i - 1) + ' Selected', couleur='red', taille=24,
                                  tag='j')
                        niveau = levels[i - 1]
                        attente(1)
                        efface('j')
        if ty == 'Touche':
            if touche(ev) == 'Return':
                if niveau in levels:
                    efface_tout()
                    break
        if ty == 'Quitte':
            ferme_fenetre()
    return niveau

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tâche 4 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def resoudre(grille, noircies, i, j):
    if sans_voisines_noircies(noircies) == False or connexe(grille, noircies) == False:
        return None
    elif sans_conflit(grille, noircies) and sans_voisines_noircies(noircies) and connexe(grille, noircies):
        return noircies
    else:
        if i < len(grille):
            copie = deepcopy(grille)
            for element in noircies:
                (a, b) = element
                copie[a][b] = None
            copie_verticale = [[colonne[x] for colonne in copie] for x in range(len(copie[0]))]
            if copie.count(grille[i][j]) == 1 and copie_verticale.count(grille[i][j]) == 1 and copie[i][j] != None:
                if j == len(grille[0])-1:
                    return resoudre(grille, noircies, i + 1, 0)
                else:
                    return resoudre(grille, noircies, i, j+1)
            else:
                noircies.add((i, j))
                if j == len(grille[0]) - 1:
                    res = resoudre(grille, noircies, i + 1, 0)
                else:
                    res = resoudre(grille, noircies, i, j + 1)

                if res is not None:
                    return noircies
                else:
                    noircies.discard((i, j))
                    if j == len(grille[0])-1:
                        res = resoudre(grille, noircies, i+1, 0)
                    else:
                        res = resoudre(grille, noircies, i, j+1)
                    if res is not None:
                        return noircies
                    else:
                        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def res_tenaille(resolue, impossible):
    '''
    Cette technique ne permet pas de noircir une case, mais elle permet d’assurer que certaines cases
    ne le seront pas. La technique de la tenaille est appliquée lorsqu’un chiffre se trouve entre deux
    chiffres différents de lui. Par contre, ces deux chiffres doivent être identiques.
    '''
    for i in range(len(resolue)):
        for j in range(1, len(resolue[0])-1):
            if resolue[i][j-1] == resolue[i][j+1] and resolue[i][j] != resolue[i][j+1]:
                impossible.add((i, j))
    for i in range(1, len(resolue)-1):
        for j in range(len(resolue[0])):
            if resolue[i-1][j] == resolue[i+1][j] and resolue[i][j] != resolue[i+1][j]:
                impossible.add((i, j))

def res_doublet(resolue, possible):
    '''
    Cette technique permet de noircir une case. Pour utiliser cette technique, il faut repérer dans
    une même colonne ou dans une ligne un doublet (un doublet est un groupe de deux cases identiques
    côte à côte) et que dans la même ligne ou colonne, se trouve une troisième fois le même chiffre
    et que ce dernier ne touche pas le doublet.
    '''
    for i in range(len(resolue)):
        for j in range(len(resolue[0])-1):
            if resolue[i][j] == resolue[i][j+1]:
                for k in range(len(resolue[0])):
                    if resolue[i][k] == resolue[i][j] and j-1 != k and j != k and j+1 != k and j+2 != k:
                        possible.add((i, k))
    for i in range(len(resolue)-1):
        for j in range(len(resolue[0])):
            if resolue[i][j] == resolue[i+1][j]:
                for l in range(len(resolue)):
                    if resolue[l][j] == resolue[i][j] and i-1 != l and i != l and i+1 != l and i+2 != l:
                        possible.add((l, j))

def res_triplet(resolue, possible, impossible):
    for i in range(len(resolue)):
        for j in range(len(resolue[0])-2):
            if resolue[i][j] == resolue[i][j+1] == resolue[i][j+2]:
                if j == len(resolue[0])-3 or j == 0:
                    possible.add((i, j))
                    impossible.add((i, j+1))
                    possible.add((i, j+2))
                elif resolue[i][j+3] != resolue[i][j+2] and resolue[i][j] != resolue[i][j-1]:
                    possible.add((i, j))
                    impossible.add((i, j + 1))
                    possible.add((i, j + 2))
    for i in range(len(resolue)-2):
        for j in range(len(resolue[0])):
            if resolue[i][j] == resolue[i+1][j] == resolue[i+2][j]:
                if i == len(resolue) - 3 or i == 0:
                    possible.add((i, j))
                    impossible.add((i+1, j))
                    possible.add((i+2, j))
                elif resolue[i+3][j] != resolue[i+2][j] and resolue[i-1][j] != resolue[i][j]:
                    possible.add((i, j))
                    impossible.add((i + 1, j))
                    possible.add((i + 2, j))

def res_coin(resolue, possible, impossible):
    lst = [0, -1, 1, -2]
    for i in range(2):
        for j in range(2):
            if resolue[lst[i]][lst[j]] == resolue[lst[i]][lst[j+2]] == \
                    resolue[lst[i+2]][lst[i]] == resolue[lst[i+2]][lst[j+2]]:
                possible.add(resolue[lst[i]][lst[j]])
                possible.add(resolue[lst[i+2]][lst[j+2]])
                impossible.add(resolue[lst[i+2]][lst[i]])
                impossible.add(resolue[lst[i]][lst[j+2]])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Phase de jeu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

l = 700
h = 700
Jeu = True
cree_fenetre(l, h)

while Jeu:
    levels = [ "niveauexe.txt", "niveau1.txt", "niveau2.txt", "niveau3.txt", "niveau4.txt", "niveau5.txt"]
    grille = lire_grille(menu())
    rectangle(0, 0, l, h, remplissage='#FDFD96')
    mise_a_jour()
    resolue = deepcopy(grille)
    afficher_grille(grille)
    taille = 60
    espace = (l-((len(grille[0]))*taille))/2
    victoire = False
    noircies = set()
    impossible = set()
    possible = set()
    dessine_plateau(taille, espace, grille)
    avant = None

    res_tenaille(resolue, impossible)
    res_doublet(resolue, possible)
    res_triplet(resolue, possible, impossible)
    res_coin(resolue, possible, impossible)
    print('Black :', possible)
    print('Safe :', impossible)

    while True:
        mise_a_jour()
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == 'Quitte':
            ferme_fenetre()
            Jeu = False
            break
        if tev == 'ClicGauche':
            x, y = abscisse(ev), ordonnee(ev)
            i, j = pixel_vers_case(x, y, taille)
            if i >= 0 and i <= len(grille)-1 and j >= 0 and j <= len(grille[0])-1 and victoire == False:
                avant = (i, j)
                maj_noircies(noircies, i, j)
                cases_noires(noircies, taille, espace)
                if sans_conflit(grille, noircies) and sans_voisines_noircies(noircies) \
                        and connexe(grille, noircies):
                    texte(l / 5, espace / 2, "Félicitations vous avez gagné !", tag='ecran_vic')
                    victoire = True
            if j <= 1 and j >= 0 and i == len(grille[0]) + 1 and victoire == False:
                noircies.discard(avant)
                efface('noir')
                cases_noires(noircies, taille, espace)
            if j <= len(grille[0]) -1 and j >= len(grille[0]) - 2 and i == len(grille[0]) + 1:
                noircies = set()
                efface('noir')
                efface('ecran_vic')
                cases_noires(noircies, taille, espace)
                victoire = False
            if (len(grille[0]) + 1)* taille + espace < y < (len(grille[0]) + 2) * taille + espace and 320 < x < 380 :
                break
        if tev == 'Touche':
            if touche(ev) == 's' or touche(ev) == 'S':
                resoudre(grille, noircies, 0, 0)
                cases_noires(noircies, taille, espace)
