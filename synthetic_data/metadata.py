import os

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
