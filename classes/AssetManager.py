"""
Module asset_manager.

Ce module définit la classe AssetManager, responsable de la gestion
des erreurs liées aux ressources externes du jeu (fichiers manquants).
Il fournit des utilitaires simples pour signaler les problèmes de
chargement de fichiers (images, sons, polices, etc.).
"""


class AssetManager:
    """Gère les utilitaires communs liés aux ressources du jeu.

    Cette classe sert de base pour centraliser les comportements
    partagés concernant la gestion des assets, notamment l'affichage
    des messages d'erreur lorsque des fichiers requis sont absents.
    """

    def __init__(self):
        """Initialise le gestionnaire de ressources.

        Pour l'instant, cette méthode ne réalise aucune opération,
        mais elle permet une extension future de la classe.
        # pragma: no cover signifie que cette ligne n'est pas prise
        en compte pour le calcul de couverture des tests unittest.
        """
        pass  # pragma: no cover

    def print_file_missing_error(self, file_path):
        """Affiche un message d'erreur lorsqu'un fichier est introuvable.

        Cette méthode est utilisée pour signaler de manière explicite
        qu'une ressource nécessaire au jeu n'a pas pu être localisée.

        Args:
            file_path (str): Chemin du fichier manquant.
        """
        print(f'[ERREUR]: Le fichier "{file_path}" est introuvable.')
