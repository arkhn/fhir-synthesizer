import json
import os

import requests

# Pas besoin d'anonymiser à priori
NOT_ANON_REQUESTS = {
    "ehpads_services": "/Organization?",  # EHPAD et services
    "ehpads": "/Organization?type=C0028688&",  # Requêter tous les ehpads
    "services": "/Organization?type=C4069076&partof.identifier=140016957&",  # Requêter tous les
    # services d'un ehpad
    "soins_animations": "/ActivityDefinition?",  # Liste des soins et animations
    "soins": "/ActivityDefinition?topic=C0011211&",  # Liste des soins
    "animations": "/ActivityDefinition?topic=C0680153&",  # Liste des animations
    "chambres": "/Location?",  # Liste des chambres
}

# A anonymiser
ANON_REQUESTS = {
    "patients_actifs": "/Patient?active=true&",  # Liste des patients actifs
    "activités_planifiees": "/Appointment?",  # Liste des activités planifiées
    "soins_planifies": "/ServiceRequest?status=active&",  # Liste des soins planifiés
    "vacs_hospit_sejours": "/Encounter?",  # Liste des Vacs / Hospit / Séjours prévus
    "hospitalisations": "/Encounter?class=C0019993&",  # Hospitalisations
    "sejours": "/Encounter?class=C1658399&",  # Tous les séjours en EHPAD
    "sejours_actifs": "/Encounter?class=C1658399&status=in-progress&",  # Les séjours actifs en
    # EHPAD
    "vacances": "/Encounter?class=C0019843&",  # Toutes les vacances planifiées
    "consultations_specialisees": "/Encounter?class=C2090905&",  # Toutes les consultations
    # spécialisées planifiées
    "consultations_pedicure": "/Encounter?class=C0850352&",  # Toutes les consultations de pédicure
}
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/")


def load_resources(only_anon: bool = True, all_pages: bool = False):
    """
    Args:
        only_anon: If True, only get resources to anonymize; else, get resources from all requests.
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page.
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    if only_anon:
        file2request = ANON_REQUESTS
    else:
        file2request = ANON_REQUESTS | NOT_ANON_REQUESTS

    for file_name, request in file2request.items():
        # A connection to the server is needed to access the data
        r = requests.get(f"http://10.203.0.30/hapi/fhir{request}_format=json")
        result = r.json()

        if not all_pages:
            with open(os.path.join(DATA_PATH, f"{file_name}.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False)
            continue

        pages = [result]
        relations = {k: v for k, v in [(link["relation"], link["url"]) for link in result["link"]]}
        while "next" in relations.keys():
            next_url = relations["next"]
            r = requests.get(next_url)
            result = r.json()
            pages.append(result)
            relations = {
                k: v for k, v in [(link["relation"], link["url"]) for link in result["link"]]
            }

        with open(os.path.join(DATA_PATH, f"{file_name}.json"), "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False)
