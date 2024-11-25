from rdkit import Chem


def substructure_search(molecule_list: list, substructure: str) -> list:
    """
    Эта функция принимает на вход список молекул и подструктуру после чего,
    ищет подструктру в всех молекулах из списка молекул.
    """

    def check_input_type(molecule_list, substructure):
        if not isinstance(molecule_list, list):
            raise TypeError("Первый аргумент должен быть списком строк.")

        if not isinstance(substructure, str):
            raise TypeError("Второй аргумент должен быть строкой.")

    def rdkit_structure_search(molecule_list, substructure):
        match = []
        substructure = Chem.MolFromSmiles(substructure)
        for molecule in molecule_list:
            match.append(molecule) if Chem.MolFromSmiles(
                molecule
            ).HasSubstructMatch(substructure) else None
        return match

    check_input_type(molecule_list, substructure)
    return rdkit_structure_search(molecule_list, substructure)
