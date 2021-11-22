# An util to convert CSV files to the .ttl format
import pandas as pd
from slugify import slugify


def convert(source_file_path, file_options, convert_options):
    # On lit le fichier CSV
    df = pd.read_csv(source_file_path)

    # On créer un fichier turtle
    with open(file_options['destination_path'], "w") as turtle_file:
        # On y ajoute tous les prefix
        for prefix in file_options['prefixes']:
            turtle_file.write(f'@prefix {prefix} .\n')

        # Pour chaque row du dataframe pandas
        for i, row in df.iterrows():
            turtle_file.write('\n')

            # On commence par determiner l'id du noeud
            # en utilisant notre fonction custom
            node_id = row[file_options['node_id']['column']]
            node_id = file_options['node_id']['function'](node_id)

            # On applique les transformation de chaque colonnes
            for column in convert_options.keys():
                # On determine la valeur de la row
                value = row[column]

                # On osef des valeurs vides
                if value is not None and value is not '-':

                    # Si une fonction specifique de traitement doit etre appliquer
                    # pour la valeur, alors on l'applique
                    if convert_options[column]['function']:
                        value = convert_options[column]['function'](value)

                    # Puis en fonction du type on ecrit la valeur
                    # dans le fichier turtle de differentes manieres
                    if convert_options[column]['type'] == 'string':
                        turtle_file.write(
                            f':{node_id} {convert_options[column]["predicate"]} "{value}" .\n')

                    elif convert_options[column]['type'] == 'number':
                        turtle_file.write(
                            f':{node_id} {convert_options[column]["predicate"]} {value} .\n')

                    elif convert_options[column]['type'] == 'string[]':
                        values = value

                        for value in values:
                            turtle_file.write(
                                f':{node_id} {convert_options[column]["predicate"]} "{value}" .\n')

    return None


# Pour les groupes
file_options = {
    'destination_path': './ttl/groupes.ttl',
    'prefixes': ['rdf: <http://w3c.org/1999/02/22-rdf-syntax-ns#>',
                 'schema: <http://schema.org/>',
                 ': <https://dolr.es/groups/>'
                 ],
    'node_id': {
        'column': 'nom',
        'function': lambda key: slugify(key)
    }
}

convert_options = {
    'id': {
        'column': 'id',
        'predicate': 'schema:identifier',
        'type': 'string',
        'function': None
    },
    'nom': {
        'column': 'nom',
        'predicate': 'schema:name',
        'type': 'string',
        'function': None
    },
    'abreviation': {
        'column': 'abreviation',
        'predicate': 'schema:name',
        'type': 'string',
        'function': None
    },
    'anneeCreation': {
        'column': 'anneeCreation',
        'predicate': 'schema:foundingDate',
        'type': 'number',
        'function': None
    },
    'anneeDissolution': {
        'column': 'anneeDissolution',
        'predicate': 'schema:dissolutionDate',
        'type': 'number',
        'function': None
    },
    'url': {
        'column': 'url',
        'predicate': 'schema:url',
        'type': 'string',
        'function': None
    },
    'bordPolitique': {
        'column': 'bordPolitique',
        'predicate': 'schema:ethicsPolicy',
        'type': 'string',
        'function': None
    },
    'valeurs': {
        'column': 'valeurs',
        'predicate': 'schema:ethicsPolicy',
        'type': 'string[]',
        'function': lambda values: values.split(';')
    }
}


convert('./CSV/groupes.csv', file_options, convert_options)
