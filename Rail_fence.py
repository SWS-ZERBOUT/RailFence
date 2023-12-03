import streamlit as st
def chiffrer_rail_fence(message_clair, cle):
    # Initialisation de la matrice 
    rail = [['\n' for i in range(len(message_clair))]
            for j in range(cle)]

    # Trouver la direction
    dir_descendante = False
    ligne, colonne = 0, 0

    for i in range(len(message_clair)):
        if (ligne == 0) or (ligne == cle - 1):
            dir_descendante = not dir_descendante

        rail[ligne][colonne] = message_clair[i]
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
    return "".join(resultat)


def dechiffrer_rail_fence(message_chiffre, cle):
    # Initialiser la matrice du rail fence
    rail = [['\n' for i in range(len(message_chiffre))]
            for j in range(cle)]

    # Déterminer la direction du remplissage de la matrice
    dir_descendante = None
    ligne, colonne = 0, 0

    for i in range(len(message_chiffre)):
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
            colonne += 1

        if dir_descendante:
            ligne += 1
        else:
            ligne -= 1

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
    