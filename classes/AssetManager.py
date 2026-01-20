class AssetManager:

    def __init__(self):
        pass  # pragma: no cover

    def print_file_missing_error(self, file_path):
        """Affiche un message d'erreur si un fichier est introuvable.

        Args:
            file_path (str): Chemin du fichier manquant.
        """
        print(f'[ERREUR]: Le fichier "{file_path}" est introuvable.')
