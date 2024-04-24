import pandas as pd
import matplotlib.pyplot as plt

def main():
    chemin_fichier = input("Entrez le chemin absolu du fichier : ")

    while True:
        print("\nOptions disponibles:")
        print("1 - Lire le fichier complet")
        print("2 - Calculer la moyenne des colonnes numériques")
        print("3 - Prévisualiser les premières lignes du fichier")
        print("4 - Lire un fichier Excel")
        print("5 - Nettoyer les données en supprimant les lignes avec des valeurs manquantes")
        print("6 - Trier les données par une colonne spécifiée")
        print("7 - Sauvegarder le DataFrame dans un nouveau fichier")
        print("8 - Calculer la médiane des colonnes numériques")
        print("9 - Calculer l'écart type des colonnes numériques")
        print("10 - Visualiser un histogramme d'une colonne numérique")
        print("11 - Visualiser un graphique à barres pour une colonne catégorielle")
        print("12 - Visualiser un box plot pour les colonnes numériques")
        print("0 - Quitter le programme")
        
        choice = int(input("Que voulez-vous faire ? Entrez le numéro correspondant à votre choix : "))
        
        if choice == 0:
            print("Au revoir!")
            break
        else:
            if choice in {1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12}:
                sep = input("Entrez le séparateur utilisé dans le fichier (appuyez sur Entrée pour utiliser la virgule) : ")
                sep = sep if sep else ',' 

        if choice == 1:
            with open(chemin_fichier, "r") as f:
                print(f.read())
        elif choice == 2:
            df = pd.read_csv(chemin_fichier)
            mean_values = df.select_dtypes(include=['number']).mean()
            print("Moyennes des colonnes numériques :")
            print(mean_values)
        elif choice == 3:
            df = pd.read_csv(chemin_fichier)
            print(df.head())
        elif choice == 4:
            df = pd.read_excel(chemin_fichier)
            print(df)
        elif choice == 5:
            df = pd.read_csv(chemin_fichier)
            df_clean = df.dropna()
            print(df_clean)
        elif choice == 6:
            column = input("Entrez le nom de la colonne pour trier les données : ")
            df = pd.read_csv(chemin_fichier)
            df_sorted = df.sort_values(by=[column])
            print(df_sorted)
        elif choice == 7:
            df = pd.read_csv(chemin_fichier)
            output_path = input("Entrez le chemin de sauvegarde du fichier modifié : ")
            df.to_csv(output_path, index=False)
            print(f"Fichier sauvegardé avec succès à {output_path}")
        elif choice == 8:
            df = pd.read_csv(chemin_fichier)
            median_values = df.select_dtypes(include=['number']).median()
            print("Médianes des colonnes numériques :")
            print(median_values)
        elif choice == 9:
            df = pd.read_csv(chemin_fichier)
            std_dev = df.select_dtypes(include=['number']).std()
            print("Écart type des colonnes numériques :")
            print(std_dev)
        elif choice == 10:
            df = pd.read_csv(chemin_fichier)
            column = input("Entrez le nom de la colonne numérique : ")
            plt.hist(df[column].dropna(), bins=30, alpha=0.7)
            plt.title(f'Histogramme de {column}')
            plt.xlabel(column)
            plt.ylabel('Fréquence')
            plt.show()
        elif choice == 11:
            df = pd.read_csv(chemin_fichier)
            column = input("Entrez le nom de la colonne catégorielle : ")
            counts = df[column].value_counts()
            counts.plot(kind='bar')
            plt.title(f'Graphique à barres de {column}')
            plt.xlabel(column)
            plt.ylabel('Nombre')
            plt.show()
        elif choice == 12:
            df = pd.read_csv(chemin_fichier)
            df.select_dtypes(include=['number']).plot(kind='box')
            plt.title('Box Plot des Colonnes Numériques')
            plt.ylabel('Valeurs')
            plt.show()

if __name__ == "__main__":
    main()
