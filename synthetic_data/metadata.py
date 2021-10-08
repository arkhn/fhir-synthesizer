import os

from glom import Coalesce

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/")

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

NOT_ANON_RESOURCE_TYPES = list(NOT_ANON_REQUESTS.keys())
ANON_RESOURCES_TYPES = list(ANON_REQUESTS.keys())
ALL_RESOURCE_TYPES = NOT_ANON_RESOURCE_TYPES + NOT_ANON_RESOURCE_TYPES

# {resource_name : [(spec, n_flatten), ...]}
SPECS_TO_SAMPLE = {
    "patients_actifs": [(("entry", ["resource.managingOrganization"]), 0)],
    "activités_planifiees": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.description"]), 0),
        (("entry", ["resource.start"]), 0),
        (("entry", ["resource.end"]), 0),
    ],  # Participants ?
    "soins_planifies": [
        (("entry", ["resource.code"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.occurrenceTiming"]), 0),
        (("entry", ["resource.performerType"]), 0),
    ],
    "vacs_hospit_sejours": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.class"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
        (("entry", [Coalesce("resource.serviceProvider", default=None)]), 0),
        (("entry", [Coalesce("resource.priority", default=None)]), 0),
    ],
    "hospitalisations": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
        (("entry", [Coalesce("resource.serviceProvider", default=None)]), 0),
    ],
    "sejours": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
        (("entry", [Coalesce("resource.serviceProvider", default=None)]), 0),
        (("entry", ["resource.location"]), 1),
    ],
    "sejours_actifs": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
        (("entry", [Coalesce("resource.serviceProvider", default=None)]), 0),
        (("entry", ["resource.location"]), 1),
    ],
    "vacances": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
    ],
    "consultations_specialisees": [
        (("entry", ["resource.status"]), 0),
        (("entry", [Coalesce("resource.type", default=None)]), 1),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
        (("entry", ["resource.priority"]), 0),
    ],
    "consultations_pedicure": [
        (("entry", ["resource.status"]), 0),
        (("entry", ["resource.subject"]), 0),
        (("entry", ["resource.period"]), 0),
    ],
}

# {resource_name : [spec, ...]}
SPECS_TO_DELETE = {
    "patients_actifs": [
        ("entry", ["resource.birthDate"]),
        ("entry", [("resource.name", ["text"])]),
        ("entry", [("resource.name", ["family"])]),
        ("entry", [("resource.name", ["given"])]),
    ],
    "activités_planifiees": [],
    "soins_planifies": [("entry", ["resource.note"])],
    "vacs_hospit_sejours": [("entry", [Coalesce("resource.type", default=None)])],
    "hospitalisations": [("entry", [Coalesce("resource.type", default=None)])],
    "sejours": [],
    "sejours_actifs": [],
    "vacances": [("entry", [Coalesce("resource.type", default=None)])],
    "consultations_specialisees": [
        ("entry", [Coalesce("resource.reasonCode", default=None)]),
        ("entry", ["resource.hospitalization"]),
    ],
    "consultations_pedicure": [("entry", [Coalesce("resource.reasonCode", default=None)])],
}
