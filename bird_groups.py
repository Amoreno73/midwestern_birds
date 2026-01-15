import re

"""
Central place to define bird groupings for eBird common names (comName).

Usage:
    from bird_groups import BIRD_GROUPS, get_group_for_species
"""
# -------------------------------------------------------------------
# 1) DEFINE GROUPS HERE
# -------------------------------------------------------------------
BIRD_GROUPS: dict[str, list[str]] = {
    "Dabbling Ducks": [
        "Mallard",
        "American black duck",
        "Mallard/American Black Duck", 
        "Gadwall",
        "American wigeon",
        "Northern pintail",
        "Northern shoveler",
        "Green-winged teal",
        "Blue-winged teal",
        "Wood duck",
    ],

    "Diving Ducks": [
        "Canvasback",
        "Redhead",
        "Ring-necked duck",
        "Greater scaup",
        "Lesser scaup",
        "Common goldeneye",
        "Bufflehead",
        "Long-tailed duck",
        "Ruddy duck",
        "White-winged scoter",
    ],

    "Geese": [
        "Canada goose",
        "Snow goose",
        "Ross's goose",
        "Greater white-fronted goose",
        "Brant",
        "Red-breasted goose",
    ],

    "Swans": [
        "Mute swan",
        "Trumpeter swan",
        "Tundra swan",
        "Black swan",
    ],

    "Grebes": [
        "Pied-billed grebe",
        "Eared grebe",
    ],

    "Herons & Egrets": [
        "Great blue heron",
        "Great egret",
        "Green heron",
    ],

    "Pelicans & Cormorants": [
        "American white pelican",
        "Double-crested cormorant",
    ],

    "Gulls & Terns": [
        "American Herring Gull",
        "Ring-billed gull",
        "Caspian tern",
        "Common tern",
    ],

    "Cranes": [
        "Sandhill crane",
        "Whooping crane",
    ],

    "Raptors - Hawks & Eagles": [
        "Bald eagle",
        "Golden eagle",
        "Red-tailed hawk",
        "Red-shouldered hawk",
        "Cooper's hawk",
        "Sharp-shinned hawk",
        "Broad-winged hawk",
        "Rough-legged hawk",
        "Northern harrier",
    ],

    "Raptors - Falcons": [
        "Peregrine falcon",
        "American kestrel",
        "Osprey",
    ],

    "Owls": [
        "Great horned owl",
        "Barred owl",
        "Eastern Screech-Owl",
        "Snowy owl",
    ],

    "Vultures": [
        "Turkey vulture",
        "Black vulture",
    ],

    "Passerines": [
        "American robin",
        "Barn swallow",
        "Dark-eyed junco",
        "Hermit thrush",
        "Horned lark",
        "Red-winged blackbird",
        "Blue jay",
        "American crow",
        "Common raven",
        "European starling",
        "House sparrow",
    ],

    "Pigeons & Coots": [
        "Rock pigeon",
        "American coot",
    ],
}

# --- helper: normalize strings to improve matching ---
def _norm(s: str) -> str:
    s = "" if s is None else str(s)

    # Normalize unicode punctuation to ASCII
    s = (s.replace("’", "'")
           .replace("–", "-")
           .replace("—", "-"))

    # Collapse whitespace and lowercase
    s = " ".join(s.strip().lower().split())

    # Normalize spaces around slash (A / B -> A/B)
    s = re.sub(r"\s*/\s*", "/", s)

    return s

# -------------------------------------------------------------------
# 2) AUTO-BUILD REVERSE LOOKUP: species -> group
# -------------------------------------------------------------------
SPECIES_TO_GROUP: dict[str, str] = {}

for group, species_list in BIRD_GROUPS.items():
    for sp in species_list:
        k = _norm(sp)
        if k in SPECIES_TO_GROUP:
            raise ValueError(
                f"Species '{sp}' appears in multiple groups: "
                f"{SPECIES_TO_GROUP[k]} and {group}"
            )
        SPECIES_TO_GROUP[k] = group


def get_group_for_species(species_common_name: str, default: str = "NOT_IN_GROUPS") -> str:
    """
    Map eBird comName -> group name (case/punctuation-insensitive).
    If no match, returns 'NOT_IN_GROUPS' by default.
    """
    return SPECIES_TO_GROUP.get(_norm(species_common_name), default)
