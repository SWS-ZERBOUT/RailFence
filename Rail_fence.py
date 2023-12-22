import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

st.sidebar.text("Installing dependencies...")
st.sidebar.code("!pip install matplotlib")

def chiffrer_rail_fence(message_clair, cle):
    # Initialisation de la matrice 
    rail = [['\n' for i in range(len(message_clair))]
            for j in range(cle)]
    
    #affichage du rail fence
    x_plot = []
    y_plot = []
    annotations_plot = []

    # Trouver la direction
    dir_descendante = False
    ligne, colonne = 0, 0

    for i in range(len(message_clair)):
        x_plot.append(i) #
        if (ligne == 0) or (ligne == cle - 1):
            dir_descendante = not dir_descendante

        rail[ligne][colonne] = message_clair[i]
        y_plot.append(ligne) #
        annotations_plot.append(message_clair[i]) #
        colonne += 1

        if dir_descendante:
            ligne += 1
        else:
            ligne -= 1
    resultat = []
    for i in range(cle):
        for j in range(len(message_clair)):
            if rail[i][j] != '\n':
                resultat.append(rail[i][j])

    # affichage du rail fence

    x = np.array(x_plot)
    y = np.array(y_plot)
    x_new = np.linspace(x.min(), x.max(),500)
    f = interp1d(x, y, kind='quadratic')
    y_smooth=f(x_new)

    fig, ax = plt.subplots()
    ax.plot (x_new,y_smooth, color='black')
    ax.scatter(x_plot, y_plot, label='Data Points', color='black', marker='o')

    ax.set_axis_off()
    for i in range(len(x_plot)):
        ax.annotate(annotations_plot[i], (x_plot[i], y_plot[i]), textcoords="offset points", xytext=(10, 7), ha='right')



    ax.set_title('Rail fence')
    st.pyplot(fig)


    return "".join(resultat)


def dechiffrer_rail_fence(message_chiffre, cle):
    # Initialiser la matrice du rail fence
    rail = [['\n' for i in range(len(message_chiffre))]
            for j in range(cle)]
    
    #affichage du rail fence
    x_plot = []
    y_plot = []
    annotations_plot = []

    # Déterminer la direction du remplissage de la matrice
    dir_descendante = None
    ligne, colonne = 0, 0

    for i in range(len(message_chiffre)):
        x_plot.append(i) #
        if ligne == 0:
            dir_descendante = True
        if ligne == cle - 1:
            dir_descendante = False

        rail[ligne][colonne] = '*'
        colonne += 1

        if dir_descendante:
            ligne += 1
        else:
            ligne -= 1

    # Remplir la matrice de message chifré
    index = 0
    for i in range(cle):
        for j in range(len(message_chiffre)):
            if rail[i][j] == '*' and index < len(message_chiffre):
                rail[i][j] = message_chiffre[index]
                index += 1

    # lire le resultat depuis la matrice 
    resultat = []
    ligne, colonne = 0, 0
    for i in range(len(message_chiffre)):
        if ligne == 0:
            dir_descendante = True
        if ligne == cle - 1:
            dir_descendante = False

        if rail[ligne][colonne] != '*':
            resultat.append(rail[ligne][colonne])
            y_plot.append(ligne) #
            annotations_plot.append(rail[ligne][colonne]) #
            colonne += 1

        if dir_descendante:
            ligne += 1
        else:
            ligne -= 1
    # affichage du rail fence

    x = np.array(x_plot)
    y = np.array(y_plot)
    x_new = np.linspace(x.min(), x.max(),500)
    f = interp1d(x, y, kind='quadratic')
    y_smooth=f(x_new)

    fig, ax = plt.subplots()
    ax.plot (x_new,y_smooth, color='black')
    ax.scatter(x_plot, y_plot, label='Data Points', color='black', marker='o')

    ax.set_axis_off()
    for i in range(len(x_plot)):
        ax.annotate(annotations_plot[i], (x_plot[i], y_plot[i]), textcoords="offset points", xytext=(10, 7), ha='right')



    ax.set_title('Rail fence')
    st.pyplot(fig)

    return "".join(resultat)
def lire_fichier(upload_file):
    if upload_file is not None:
        contenu = upload_file.read()
        return contenu.decode("utf-8")
    return None

def main():
    st.title("Chiffrement et Déchiffrement Rail Fence à k niveaux ")

    choix = st.radio("Choisissez une option:", ("Chiffrer", "Déchiffrer"))

    option_remplissage = st.selectbox("Choisissez une option de remplissage:", ("Manuel", "Charger depuis un fichier"))

    fichier = None
    if option_remplissage == "Charger depuis un fichier":
        fichier = st.file_uploader("Télécharger un fichier texte :", type=["txt"])

    if option_remplissage == "Manuel" or (fichier is not None and option_remplissage == "Charger depuis un fichier"):
        if fichier is not None:
            contenu_fichier = lire_fichier(fichier)
            st.text_area("Contenu du fichier:", contenu_fichier, height=200)

        if choix == "Chiffrer":
            message_clair = st.text_area("Entrez le message clair:")
            cle = st.number_input("Entrez le nombre de niveaux:", min_value=2, value=3, step=1)

            if st.button("Chiffrer"):
                if fichier is not None:
                    message_clair = contenu_fichier
                message_chiffre = chiffrer_rail_fence(message_clair, cle)
                st.success("Message chiffré: {}".format(message_chiffre))

        elif choix == "Déchiffrer":
            message_chiffre = st.text_area("Entrez le message chiffré:")
            cle = st.number_input("Entrez la clé (nombre de niveaux Rail Fence):", min_value=2, value=3, step=1)

            if st.button("Déchiffrer"):
                if fichier is not None:
                    message_chiffre = contenu_fichier
                message_dechiffre = dechiffrer_rail_fence(message_chiffre, cle)
                st.success("Message déchiffré: {}".format(message_dechiffre))

    st.markdown("NB : Ce projet a été réalisé par LAIB Mohamed et Samy Walid ZERBOUT")

if __name__ == "__main__":
    main()
