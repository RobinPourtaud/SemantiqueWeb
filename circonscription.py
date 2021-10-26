import json


def get_polygons(polygons, polygons_type):
    if polygons_type == 'Polygon':
        polygons = polygons[0]
        coords = [f"{p[0]} {p[1]}" for p in polygons]

        return f"schema:polygon \"{' '.join(coords)}\""

    else:
        multipolygon = []

        i = 0

        for subpolygons in polygons:
            subpolygons = subpolygons[0]
            i += 1
            coords = [f"{p[0]} {p[1]}" for p in subpolygons]
            multipolygon.append(f"schema:polygon \"{' '.join(coords)}\"")

        return "; ".join(multipolygon)
    # return [f'schema:polygon {}' for polygon in polygons]


with open('./france-circonscriptions-legislatives-2012.json') as f:
    data = json.load(f)
    with open('./administrativeArea.ttl', "w") as turtle_file:
        turtle_file.write("""
@prefix schema:  <https://schema.org/> .
@prefix dbo:  https://dbpedia.org/ontology/ .
@prefix rdf:  http://www.w3.org/1999/02/22-rdf-syntax-ns# .
@prefix administrativeRegion:  https://fuseki.dolr.es/administrativeArea/ .\n\n
        """)

        for feature in data['features']:
            row = feature['properties']
            row["ID"] = f'{row["code_dpt"]}-{row["num_circ"]}'
            turtle_file.write(f"""
:{row["ID"]} rdf:type schema:administrativeArea .
:{row["ID"]} schema:name "{row["nom_dpt"]}-{row["num_circ"]}" .
:{row["ID"]} schema:address "{row["code_dpt"]}" .
:{row["ID"]} schema:geo [ rdf:type schema:GeoShape; schema:postalCode "{row["code_dpt"]}"; {get_polygons(feature["geometry"]["coordinates"], feature["geometry"]["type"])} ] .
            """)

        # for depute in data['deputes']:
        #    turtle_file.write(f'\n')
        #    depute = depute['depute']
        #    for i, column in enumerate(columns):
        #        if depute.get(column, None) and depute.get('id_an', None):
        #            turtle_file.write(
        #                f':PA{depute["id_an"]} custom:{predicates[i]} {depute[column]} .\n')
