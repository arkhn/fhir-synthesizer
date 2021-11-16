from glom import Coalesce

META = (
    "entry.{}.resource.meta",
    {"tag": [{"system": "http://terminology.arkhn.org/Synthetic", "code": "gen-3"}]},
)

ID = "entry.{}.resource.id"
URL = "entry.{}.fullUrl"

RESOURCE_NAMES = [
    "ehpads",
    "services",
    "soins",
    "animations",
    "chambres",
    "patients_actifs",
    "activites_planifiees",
    "soins_planifies",
    "hospitalisations",
    "sejours",
    "vacances",
    "consultations_specialisees",
    # "consultations_pedicure",  # No result for the corresponding request, so commented out in
    # the following
    "practitioner",
]

REQUESTS = {
    # Requêter tous les ehpads
    "ehpads": "Organization?type=C0028688&",
    # Requêter tous les services d'un ehpad
    "services": "Organization?type=C4069076&partof.identifier=140016957&",
    # Liste des soins
    "soins": "ActivityDefinition?topic=C0011211&",
    # Liste des animations
    "animations": "ActivityDefinition?topic=C0680153&",
    # Liste des chambres
    "chambres": "Location?",
    # Liste des patients actifs
    "patients_actifs": "Patient?active=true&",
    # Liste des activités planifiées
    "activites_planifiees": "Appointment?",
    # Liste des soins planifiés
    "soins_planifies": "ServiceRequest?status=active&subject.active=true&",
    # Hospitalisations
    "hospitalisations": "Encounter?class=C0019993&",
    # Tous les séjours en EHPAD
    "sejours": "Encounter?class=C1658399&subject.active=true&",
    # Toutes les vacances planifiées
    "vacances": "Encounter?class=C0019843&subject.active=true&",
    # Toutes les consultations spécialisées planifiées
    "consultations_specialisees": "Encounter?class=C2090905&subject.active=true&",
    # Consultations de pedicure
    # "Encounter?class=C0850352&subject.active=true&",
    "practitioner": "Practitioner?",
}

# Attributes to sample
# {resource_name : [(path, spec, n_flatten), ...]}
PATHS_TO_SAMPLE = {
    "activites_planifiees": [
        ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
        ("entry.{}.resource.description", ("entry", ["resource.description"]), 0),
        # ("entry.{}.resource.start", ("entry", ["resource.start"]), 0),
        # ("entry.{}.resource.end", ("entry", ["resource.end"]), 0),
    ],
    "soins_planifies": [
        ("entry.{}.resource.code", ("entry", ["resource.code"]), 0),
        ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
        ("entry.{}.resource.occurrenceTiming", ("entry", ["resource.occurrenceTiming"]), 0),
        ("entry.{}.resource.performerType", ("entry", ["resource.performerType"]), 0),
    ],
    "hospitalisations": [
        ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
        ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
        ("entry.{}.resource.period", ("entry", ["resource.period"]), 0),
        (
            "entry.{}.resource.serviceProvider",
            ("entry", [Coalesce("resource.serviceProvider", default=None)]),
            0,
        ),
    ],
    "sejours": [
        ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
        ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
        ("entry.{}.resource.period", ("entry", ["resource.period"]), 0),
        (
            "entry.{}.resource.serviceProvider",
            ("entry", [Coalesce("resource.serviceProvider", default=None)]),
            0,
        ),
        ("entry.{}.resource.location", ("entry", ["resource.location"]), 1),
    ],
    "vacances": [
        ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
        ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
        ("entry.{}.resource.period", ("entry", ["resource.period"]), 0),
    ],
    "consultations_specialisees": [
        ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
        ("entry.{}.resource.type", ("entry", [Coalesce("resource.type", default=None)]), 1),
        ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
        ("entry.{}.resource.period", ("entry", ["resource.period"]), 0),
        ("entry.{}.resource.priority", ("entry", ["resource.priority"]), 0),
        ("entry.{}.resource.hospitalization", ("entry", ["resource.hospitalization"]), 0),
    ],
    # "consultations_pedicure": [
    #     ("entry.{}.resource.status", ("entry", ["resource.status"]), 0),
    #     ("entry.{}.resource.subject", ("entry", ["resource.subject"]), 0),
    #     ("entry.{}.resource.period", ("entry", ["resource.period"]), 0),
    # ],
    # "practitioner": [
    #     (
    #         "entry.{}.resource.qualification",
    #         ("entry", [Coalesce("resource.qualification", default=None)]),
    #         1,
    #     )
    # ],
}

# Attributes that must be deleted
# {resource_name : [spec, ...]}
PATHS_TO_DELETE = {
    "patients_actifs": [
        "entry.{}.resource.birthDate",
        # "entry.{}.resource.name",  # We will sample fake names instead
        "entry.{}.resource.text",
        "entry.{}.resource.identifier",
    ],
    "hospitalisations": ["entry.{}.resource.type"],
    "vacances": ["entry.{}.resource.type"],
    "consultations_pedicure": ["entry.{}.resource.name", "entry.{}.resource.identifier"],
    "practitioner": [
        # "entry.{}.resource.name",  # We will sample fake names instead
        "entry.{}.resource.identifier",
    ],
}

# Attributes that must be set to a default value
# {resource_name : [(path, default_value), ...]}
PATHS_DEFAULT_VALUE = {
    "ehpads": [META],
    "services": [META],
    "soins": [META],
    "animations": [META],
    "chambres": [META],
    "patients_actifs": [META],
    "activites_planifiees": [META],
    "soins_planifies": [META, ("entry.{}.resource.note", [{"text": "DEFAULT NOTE"}])],
    "hospitalisations": [META],
    "sejours": [META],
    "vacances": [META],
    "consultations_specialisees": [
        META,
        ("entry.{}.resource.reasonCode", [{"text": "DEFAULT REASONCODE"}]),
        ("entry.{}.resource.type.text", [{"text": "DESCRIPTION DU RDV"}]),
    ],
    # "consultations_pedicure": [
    #     META,
    #     ("entry.{}.resource.reasonCode", "DEFAULT REASONCODE"),
    # ],
    "practitioner": [META],
}

# Attributes that are ids or refs to which we must add a suffix
PATHS_ID_REF = {
    "ehpads": [ID, URL],
    "services": [ID, URL, "entry.{}.resource.partOf.reference"],
    "soins": [ID, URL],
    "animations": [ID, URL],
    "chambres": [ID, URL, "entry.{}.resource.managingOrganization.reference"],
    "patients_actifs": [ID, URL, "entry.{}.resource.managingOrganization.reference"],
    "activites_planifiees": [ID, URL],
    "soins_planifies": [ID, URL, "entry.{}.resource.subject.reference"],
    "hospitalisations": [ID, URL, "entry.{}.resource.serviceProvider.reference"],
    "sejours": [
        ID,
        URL,
        "entry.{}.resource.subject.reference",
        "entry.{}.resource.location.0.location.reference",
        "entry.{}.resource.serviceProvider.reference",
    ],
    "vacances": [ID, URL, "entry.{}.resource.subject.reference"],
    "consultations_specialisees": [ID, URL, "entry.{}.resource.subject.reference"],
    # "consultations_pedicure": [ID, URL],
    "practitioner": [ID, URL],
}
