import json

columns = ["semaines_presence",
           "commission_presences",
           "commission_interventions",
           "hemicycle_interventions",
           "hemicycle_interventions_courtes",
           "amendements_proposes",
           "amendements_signes",
           "amendements_adoptes",
           "rapports",
           "propositions_ecrites",
           "propositions_signees",
           "questions_ecrites",
           "questions_orales"]

predicates = ["semainesPresence",
              "commissionPresences",
              "commissionInterventions",
              "hemicycleInterventions",
              "hemicycleInterventions_courtes",
              "amendementsProposes",
              "amendementsSignes",
              "amendementsAdoptes",
              "rapports",
              "propositionsEcrites",
              "propositionsSignees",
              "questionsEcrites",
              "questionsOrales"]

with open('./nosdeputesfr.json') as f:
    data = json.load(f)
    with open('./parliamentMember.ttl', "a") as turtle_file:
        turtle_file.write(f'\n')

        for depute in data['deputes']:
            turtle_file.write(f'\n')
            depute = depute['depute']
            for i, column in enumerate(columns):
                if depute.get(column, None) and depute.get('id_an', None):
                    turtle_file.write(
                        f':PA{depute["id_an"]} custom:{predicates[i]} {depute[column]} .\n')
