# JDX Generator V1 Slot Engine
# Slot-based prompt order + Smart / Creative / Chaos rules.

from pathlib import Path
from functools import lru_cache
import hashlib
import json
import random


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPT_LIBRARY_DIR = DATA_DIR / "prompt_library"
RULES_DIR = DATA_DIR / "rules"

ENGINE_VERSION = "1.2.0"


# ---------------------------------------------------------------------------
# Seeding
#
# A single master seed drives the whole generation, but every slot draws from
# its OWN derived stream, and every candidate tag gets its OWN key. This means:
#   * toggling one category off never shifts the result of another category,
#   * reordering or adding lines in a .txt file does not disturb tags that were
#     already there,
#   * raising a slot's count is additive (the first pick stays, the next-best
#     is added) instead of rerolling the whole slot.
# Seeding stays isolated to this module, so it neither disturbs nor is disturbed
# by any other node in the workflow.
# ---------------------------------------------------------------------------
_master_seed = None


def seed_engine(seed=None):
    """Set the master seed. Pass None for fully random (non-reproducible) output."""
    global _master_seed
    _master_seed = int(seed) if seed is not None else None


def _derive_seed(*parts):
    """Deterministically fold the master seed plus some labels into a 64-bit int."""
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def _tag_unit(slot, tag):
    """A stable uniform-[0,1) value for a (slot, tag) pair under the master seed."""
    if _master_seed is None:
        return random.random()
    return random.Random(_derive_seed(_master_seed, slot, tag)).random()


def _weighted_pick(items, count, slot):
    """Pick `count` distinct tags from a weighted list using per-tag keys.

    `items` is a sequence of (tag, weight) pairs. Selection uses the
    Efraimidis-Spirakis scheme (key = u ** (1/weight)); the top-`count` keys
    win, so higher weights are proportionally more likely without ever being
    guaranteed. Keys are tied to the tag text, not its position, which is what
    makes the result stable under reordering and unrelated edits.
    """
    if not items:
        return []
    count = max(0, min(int(count), len(items)))
    if count == 0:
        return []
    keyed = []
    for tag, weight in items:
        weight = weight if weight and weight > 0 else 1.0
        u = _tag_unit(slot, tag)
        # u is in [0, 1); guard the exact-0 corner so the key stays well defined.
        if u <= 0.0:
            u = 1e-12
        keyed.append((u ** (1.0 / weight), tag))
    keyed.sort(key=lambda kv: kv[0], reverse=True)
    return [tag for _, tag in keyed[:count]]


def _parse_weighted_line(line):
    """Parse 'tag::3' into ('tag', 3.0); a bare 'tag' is weight 1.0.

    If the text after the last '::' is not a number it is treated as part of
    the tag, so tags that legitimately contain '::' are left untouched.
    """
    if "::" in line:
        tag, _, raw = line.rpartition("::")
        try:
            weight = float(raw.strip())
            if weight <= 0:
                weight = 1.0
            return tag.strip(), weight
        except ValueError:
            return line, 1.0
    return line, 1.0


@lru_cache(maxsize=1024)
def _load_list_cached(path_str, _mtime_ns):
    """Read + parse a wordlist. Cached on (path, mtime) so file edits are picked
    up automatically but unchanged files are not re-read on every draw."""
    out = []
    with open(path_str, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(_parse_weighted_line(line))
    return tuple(out)


def load_list(path):
    """Return a tuple of (tag, weight) pairs for a wordlist, or () if missing."""
    p = Path(path)
    if not p.exists():
        print(f"[JDX Generator] Missing file: {p}")
        return ()
    return _load_list_cached(str(p), p.stat().st_mtime_ns)


def random_from_file(path, slot=None):
    items = load_list(path)
    if not items:
        return ""
    slot = slot or Path(path).stem
    picked = _weighted_pick(items, 1, slot)
    return picked[0] if picked else ""


def random_multiple_from_file(path, count=1, slot=None):
    items = load_list(path)
    if not items:
        return []
    slot = slot or Path(path).stem
    return _weighted_pick(items, count, slot)


def random_multiple_from_first_existing_file(paths, count=1, slot=None):
    slot = slot or (Path(paths[0]).stem if paths else "")
    for path in paths:
        items = load_list(path)
        if items:
            return _weighted_pick(items, count, slot)
    return []


def get_boosters(model_name="flux", prompt_length="medium"):
    model_name = model_name.lower()
    prompt_length = prompt_length.lower()

    count = 2
    if prompt_length == "short":
        count = 1
    if prompt_length == "long":
        count = 4

    if model_name == "anima":
        return random_multiple_from_file(PROMPT_LIBRARY_DIR / "anima_boosters.txt", count)

    return random_multiple_from_file(PROMPT_LIBRARY_DIR / "flux_boosters.txt", count)


def get_counts(prompt_length="medium"):
    prompt_length = prompt_length.lower()

    base = {
        "hair_colors": 1,
        "hairstyles": 1,
        "beards": 1,
        "eye_colors": 1,
        "eye_shapes": 1,
        "eyebrows": 1,
        "eyelashes": 1,
        "ears": 1,
        "earrings": 1,
        "lips": 1,
        "nose": 1,
        "chin": 1,
        "jawline": 1,
        "cheeks": 1,
        "face_shape": 1,
        "face_piercings": 1,
        "face_tattoos": 1,
        "makeup": 1,
        "upper_body": 1,
        "lower_body": 1,
        "legwear": 1,
        "footwear": 1,
        "outerwear": 1,
        "full_outfits": 1,
        "mature_upper_body": 1,
        "mature_lower_body": 1,
        "mature_outfits": 1,
        "nipples": 1,
        "areola": 1,
        "nsfw_actions": 1,
        "pussy_cocks": 1,
        "fashion_accessories": 2,
        "headwear": 1,
        "hair_accessories": 1,
        "eyewear": 1,
        "body_pose": 1,
        "hand_pose": 1,
        "expression": 1,
        "interior": 1,
        "exterior": 1,
        "simple_background": 1,
        "artstyle": 1,
        "style_theme": 1,
        "lighting": 1,
        "camera": 1,
        "details": 2,
        "masks": 1,
        "skin_tone": 1,
        "ethnicity": 1,
        "body_shape": 1,
        "height": 1,
        "frame": 1,
        "waist": 1,
        "hips": 1,
        "butt": 1,
        "legs": 1,
        "shoulders": 1,
        "fitness": 1,
        "proportions": 1,
        "facial_features": 1,
        "chest_size": 1,
        "chest_shape": 1,
    }

    if prompt_length == "short":
        base.update({
            "fashion_accessories": 1,
            "interior": 1,
            "exterior": 1,
            "simple_background": 1,
            "details": 1,
        })

    if prompt_length == "long":
        base.update({
            "hair_colors": 1,
            "hairstyles": 2,
            "fashion_accessories": 3,
            "interior": 1,
            "exterior": 2,
            "simple_background": 1,
            "artstyle": 2,
            "style_theme": 2,
            "lighting": 2,
            "camera": 2,
            "details": 4,
            "facial_features": 2,
        })

    return base



def get_mode_settings(generation_mode="smart", prompt_length="medium"):
    generation_mode = (generation_mode or "smart").lower()
    prompt_length = (prompt_length or "medium").lower()

    if generation_mode == "chaos":
        return {
            "mode": "chaos",
            "full_outfit_exclusive": False,
            "counts_override": {
                "upper_body": 2,
                "lower_body": 2,
                "legwear": 2,
                "footwear": 2,
                "outerwear": 2,
                "full_outfits": 2,
                "mature_upper_body": 2,
                "mature_lower_body": 2,
                "mature_outfits": 2,
                "nipples": 2,
                "areola": 2,
                "nsfw_actions": 2,
                "pussy_cocks": 2,
                "fashion_accessories": 5,
                "headwear": 2,
                "hair_accessories": 2,
                "eyewear": 2,
                "masks": 2,
                "body_pose": 2,
                "hand_pose": 3,
                "expression": 2,
                "interior": 2,
                "exterior": 2,
                "simple_background": 2,
                "artstyle": 2,
                "style_theme": 3,
                "lighting": 3,
                "camera": 3,
                "details": 6,
            }
        }

    if generation_mode == "creative":
        return {
            "mode": "creative",
            "full_outfit_exclusive": True,
            "counts_override": {
                "upper_body": 1,
                "lower_body": 1,
                "legwear": 1,
                "footwear": 1,
                "outerwear": 1,
                "full_outfits": 1,
                "mature_upper_body": 1,
                "mature_lower_body": 1,
                "mature_outfits": 1,
                "nipples": 1,
                "areola": 1,
                "nsfw_actions": 1,
                "pussy_cocks": 1,
                "fashion_accessories": 3 if prompt_length != "short" else 2,
                "headwear": 1,
                "hair_accessories": 1,
                "eyewear": 1,
                "masks": 1,
                "body_pose": 1,
                "hand_pose": 2,
                "expression": 1,
                "style_theme": 2 if prompt_length == "long" else 1,
                "lighting": 2 if prompt_length != "short" else 1,
                "camera": 2 if prompt_length == "long" else 1,
                "details": 4 if prompt_length == "long" else 2,
            }
        }

    return {
        "mode": "smart",
        "full_outfit_exclusive": True,
        "counts_override": {
            "upper_body": 1,
            "lower_body": 1,
            "legwear": 1,
            "footwear": 1,
            "outerwear": 1,
            "full_outfits": 1,
            "mature_upper_body": 1,
            "mature_lower_body": 1,
            "mature_outfits": 1,
            "nipples": 1,
            "areola": 1,
            "nsfw_actions": 1,
            "pussy_cocks": 1,
            "fashion_accessories": 2 if prompt_length != "short" else 1,
            "headwear": 1,
            "hair_accessories": 1,
            "eyewear": 1,
            "masks": 1,
            "body_pose": 1,
            "hand_pose": 1,
            "expression": 1,
            "style_theme": 1,
            "lighting": 1,
            "camera": 1,
            "details": 2 if prompt_length != "short" else 1,
        }
    }


def apply_mode_counts(counts, generation_mode="smart", prompt_length="medium"):
    settings = get_mode_settings(generation_mode, prompt_length)
    counts.update(settings.get("counts_override", {}))
    return counts


def clear_parts(parts, keys):
    for key in keys:
        parts[key] = []
    return parts


def apply_generation_mode_rules(parts, generation_mode="smart", nsfw=False, use_nude=False):
    """Apply JDX Clothing Rules v1.0 and environment rules.

    Smart:
        Clean logical results. Prevents outfit/background conflicts.
    Creative:
        More layering, but still prevents the worst clothing conflicts.
    Chaos:
        Mostly unrestricted. Counts are higher and collisions are allowed.
    """
    mode = (generation_mode or "smart").lower()

    def choose_one_group(keys):
        available = [key for key in keys if parts.get(key)]
        if len(available) <= 1:
            return
        if _master_seed is None:
            keep = random.choice(available)
        else:
            picker = random.Random(_derive_seed(_master_seed, "group", *available))
            keep = picker.choice(available)
        for key in available:
            if key != keep:
                parts[key] = []

    if mode == "chaos":
        if nsfw and use_nude:
            parts["nude_body"] = ["nude body"]
        return parts

    # JDX Clothing Rules v1.0
    #
    # Nude:
    #   Blocks normal clothing and mature upper/lower/outfit.
    #   Keeps nipples, areola, nsfw_actions, pussy_cocks,
    #   legwear, footwear and accessories.
    #
    # Full Outfit:
    #   Blocks normal clothing and mature outfit layers.
    #   Also blocks nipples, areola, nsfw_actions and pussy_cocks.
    #   Keeps footwear, legwear and accessories.
    #
    # Mature Outfit:
    #   Blocks normal upper/lower/full outfits.
    #   Keeps nipples, areola, nsfw_actions and pussy_cocks.
    #
    # Mature Upper:
    #   Blocks normal upper body only.
    #
    # Mature Lower:
    #   Blocks normal lower body only.

    if nsfw and use_nude:
        parts["nude_body"] = ["nude body"]

        clear_parts(parts, [
            "upper_body",
            "lower_body",
            "outerwear",
            "full_outfits",
            "mature_upper_body",
            "mature_lower_body",
            "mature_outfits",
        ])

    else:
        if parts.get("full_outfits"):
            clear_parts(parts, [
                "upper_body",
                "lower_body",
                "outerwear",
                "mature_upper_body",
                "mature_lower_body",
                "mature_outfits",
                "nipples",
                "areola",
                "nsfw_actions",
                "pussy_cocks",
            ])

        elif parts.get("mature_outfits"):
            clear_parts(parts, [
                "upper_body",
                "lower_body",
                "outerwear",
                "full_outfits",
            ])
            # Important:
            # mature_outfits must NOT remove nipples, areola, nsfw_actions or pussy_cocks.

        else:
            if parts.get("mature_upper_body"):
                parts["upper_body"] = []

            if parts.get("mature_lower_body"):
                parts["lower_body"] = []

        # nipples / areola / nsfw_actions / pussy_cocks are allowed to combine with
        # mature_upper_body, mature_lower_body and mature_outfits.
        #
        # Important:
        # If any mature fashion category is active, all four special categories may stay active
        # and each can contribute 1 tag.
        #
        # If no mature fashion category is active, Smart mode keeps only one of them
        # to avoid random clutter such as nipples + areola + pussy_cocks at once.
        mature_active = any(parts.get(key) for key in [
            "mature_upper_body",
            "mature_lower_body",
            "mature_outfits",
        ])

        if mode == "smart" and not mature_active:
            choose_one_group(["nipples", "areola", "nsfw_actions", "pussy_cocks"])

    # Smart and Creative keep one background type.
    # This avoids combinations like bedroom + forest + white background.
    choose_one_group(["interior", "exterior", "simple_background"])

    return parts

def collect_parts(
    category="portrait",
    gender="female",
    prompt_length="medium",
    generation_mode="smart",
    use_subject=True,
    use_ethnicity=True,
    use_skin_tone=True,
    use_hair_colors=True,
    use_hairstyles=True,
    use_beards=True,
    use_eye_colors=True,
    use_eye_shapes=True,
    use_eyebrows=True,
    use_eyelashes=True,
    use_ears=True,
    use_earrings=True,
    use_lips=True,
    use_nose=True,
    use_chin=True,
    use_jawline=True,
    use_cheeks=True,
    use_face_shape=True,
    use_face_piercings=True,
    use_face_tattoos=True,
    use_makeup=True,
    use_upper_body=True,
    use_lower_body=True,
    use_legwear=True,
    use_footwear=True,
    use_outerwear=True,
    use_full_outfits=False,
    use_mature_upper_body=False,
    use_mature_lower_body=False,
    use_mature_outfits=False,
    use_nipples=False,
    use_areola=False,
    use_nsfw_actions=False,
    use_pussy_cocks=False,
    use_fashion_accessories=True,
    use_headwear=True,
    use_hair_accessories=True,
    use_eyewear=True,
    use_masks=True,
    use_body_shape=True,
    use_height=True,
    use_frame=True,
    use_waist=True,
    use_hips=True,
    use_butt=True,
    use_legs=True,
    use_shoulders=True,
    use_fitness=True,
    use_proportions=True,
    use_chest_size=True,
    use_chest_shape=True,
    use_facial_features=True,
    use_body_pose=True,
    use_hand_pose=True,
    use_expression=True,
    use_interior=True,
    use_exterior=True,
    use_simple_background=True,
    use_artstyle=True,
    use_style_theme=True,
    use_lighting=True,
    use_camera=True,
    use_details=True,
    use_anima_artists=False
):
    folder = DATA_DIR / category / gender
    counts = apply_mode_counts(get_counts(prompt_length), generation_mode, prompt_length)
    mode_settings = get_mode_settings(generation_mode, prompt_length)
    use_modular_clothing = not use_full_outfits if mode_settings.get("full_outfit_exclusive", True) else True

    parts = {
        "subject": random_from_file(folder / "subject.txt") if use_subject else "",
        "ethnicity": random_multiple_from_file(folder / "ethnicity.txt", counts["ethnicity"]) if use_ethnicity else [],
        "skin_tone": random_multiple_from_file(folder / "skin_tone.txt", counts["skin_tone"]) if use_skin_tone else [],

        "hair_colors": random_multiple_from_file(folder / "hair_colors.txt", counts["hair_colors"]) if use_hair_colors else [],
        "hairstyles": random_multiple_from_file(folder / "hairstyles.txt", counts["hairstyles"]) if use_hairstyles else [],
        "beards": random_multiple_from_file(folder / "beards.txt", counts["beards"]) if use_beards else [],

        "eye_colors": random_multiple_from_file(folder / "eye_colors.txt", counts["eye_colors"]) if use_eye_colors else [],
        "eye_shapes": random_multiple_from_file(folder / "eye_shapes.txt", counts["eye_shapes"]) if use_eye_shapes else [],
        "eyebrows": random_multiple_from_file(folder / "eyebrows.txt", counts["eyebrows"]) if use_eyebrows else [],
        "eyelashes": random_multiple_from_file(folder / "eyelashes.txt", counts["eyelashes"]) if use_eyelashes else [],

        "ears": random_multiple_from_file(folder / "ears.txt", counts["ears"]) if use_ears else [],
        "earrings": random_multiple_from_file(folder / "earrings.txt", counts["earrings"]) if use_earrings else [],

        "lips": random_multiple_from_file(folder / "lips.txt", counts["lips"]) if use_lips else [],
        "nose": random_multiple_from_file(folder / "nose.txt", counts["nose"]) if use_nose else [],
        "chin": random_multiple_from_file(folder / "chin.txt", counts["chin"]) if use_chin else [],
        "jawline": random_multiple_from_file(folder / "jawline.txt", counts["jawline"]) if use_jawline else [],
        "cheeks": random_multiple_from_file(folder / "cheeks.txt", counts["cheeks"]) if use_cheeks else [],
        "face_shape": random_multiple_from_file(folder / "face_shape.txt", counts["face_shape"]) if use_face_shape else [],
        "face_piercings": random_multiple_from_file(folder / "face_piercings.txt", counts["face_piercings"]) if use_face_piercings else [],
        "face_tattoos": random_multiple_from_file(folder / "face_tattoos.txt", counts["face_tattoos"]) if use_face_tattoos else [],
        "makeup": random_multiple_from_file(folder / "makeup.txt", counts["makeup"]) if use_makeup else [],

        "upper_body": random_multiple_from_file(folder / "upper_body.txt", counts["upper_body"]) if use_upper_body and use_modular_clothing else [],
        "lower_body": random_multiple_from_file(folder / "lower_body.txt", counts["lower_body"]) if use_lower_body and use_modular_clothing else [],
        "legwear": random_multiple_from_file(folder / "legwear.txt", counts["legwear"]) if use_legwear else [],
        "footwear": random_multiple_from_file(folder / "footwear.txt", counts["footwear"]) if use_footwear else [],
        "outerwear": random_multiple_from_file(folder / "outerwear.txt", counts["outerwear"]) if use_outerwear and use_modular_clothing else [],
        "full_outfits": random_multiple_from_file(folder / "full_outfits.txt", counts["full_outfits"]) if use_full_outfits else [],

        "mature_upper_body": random_multiple_from_first_existing_file([
            folder / "mature_upper_body.txt",
            folder / "nsfw_upper_body.txt",
            folder / "mature" / "upper_body.txt",
            folder / "nsfw" / "upper_body.txt",
        ], counts["mature_upper_body"]) if use_mature_upper_body else [],

        "mature_lower_body": random_multiple_from_first_existing_file([
            folder / "mature_lower_body.txt",
            folder / "nsfw_lower_body.txt",
            folder / "mature" / "lower_body.txt",
            folder / "nsfw" / "lower_body.txt",
        ], counts["mature_lower_body"]) if use_mature_lower_body else [],

        "mature_outfits": random_multiple_from_file(folder / "mature_outfits.txt", counts["mature_outfits"]) if use_mature_outfits else [],
        "nipples": random_multiple_from_file(folder / "nipples.txt", counts["nipples"]) if use_nipples else [],
        "areola": random_multiple_from_file(folder / "areola.txt", counts["areola"]) if use_areola else [],
        "nsfw_actions": random_multiple_from_file(folder / "nsfw_actions.txt", counts["nsfw_actions"]) if use_nsfw_actions else [],
        "pussy_cocks": random_multiple_from_file(folder / "pussy_cocks.txt", counts["pussy_cocks"]) if use_pussy_cocks else [],

        "fashion_accessories": random_multiple_from_file(folder / "fashion_accessories.txt", counts["fashion_accessories"]) if use_fashion_accessories else [],
        "headwear": random_multiple_from_file(folder / "headwear.txt", counts["headwear"]) if use_headwear else [],
        "hair_accessories": random_multiple_from_file(folder / "hair_accessories.txt", counts["hair_accessories"]) if use_hair_accessories else [],
        "eyewear": random_multiple_from_file(folder / "eyewear.txt", counts["eyewear"]) if use_eyewear else [],
        "masks": random_multiple_from_file(folder / "masks.txt", counts["masks"]) if use_masks else [],
        "body_shape": random_multiple_from_file(folder / "body_shape.txt", counts["body_shape"]) if use_body_shape else [],
        "height": random_multiple_from_file(folder / "height.txt", counts["height"]) if use_height else [],
        "frame": random_multiple_from_file(folder / "frame.txt", counts["frame"]) if use_frame else [],
        "waist": random_multiple_from_file(folder / "waist.txt", counts["waist"]) if use_waist else [],
        "hips": random_multiple_from_file(folder / "hips.txt", counts["hips"]) if use_hips else [],
        "butt": random_multiple_from_file(folder / "butt.txt", counts["butt"]) if use_butt else [],
        "legs": random_multiple_from_file(folder / "legs.txt", counts["legs"]) if use_legs else [],
        "shoulders": random_multiple_from_file(folder / "shoulders.txt", counts["shoulders"]) if use_shoulders else [],
        "fitness": random_multiple_from_file(folder / "fitness.txt", counts["fitness"]) if use_fitness else [],
        "proportions": random_multiple_from_file(folder / "proportions.txt", counts["proportions"]) if use_proportions else [],
        "facial_features": random_multiple_from_file(folder / "facial_features.txt", counts["facial_features"]) if use_facial_features else [],
        "body_pose": random_multiple_from_file(folder / "body_pose.txt", counts["body_pose"]) if use_body_pose else [],
        "hand_pose": random_multiple_from_file(folder / "hand_pose.txt", counts["hand_pose"]) if use_hand_pose else [],
        "expression": random_multiple_from_file(folder / "expression.txt", counts["expression"]) if use_expression else [],
        "interior": random_multiple_from_file(folder / "interior.txt", counts["interior"]) if use_interior else [],
        "exterior": random_multiple_from_file(folder / "exterior.txt", counts["exterior"]) if use_exterior else [],
        "simple_background": random_multiple_from_file(folder / "simple_background.txt", counts["simple_background"]) if use_simple_background else [],
        "artstyle": random_multiple_from_file(folder / "artstyle.txt", counts["artstyle"]) if use_artstyle else [],
        "style_theme": random_multiple_from_file(folder / "style_theme.txt", counts["style_theme"]) if use_style_theme else [],
        "lighting": random_multiple_from_file(folder / "lighting.txt", counts["lighting"]) if use_lighting else [],
        "camera": random_multiple_from_file(folder / "camera.txt", counts["camera"]) if use_camera else [],
        "details": random_multiple_from_file(folder / "details.txt", counts["details"]) if use_details else [],
        "anima_artists": random_multiple_from_file(PROMPT_LIBRARY_DIR / "anima_artists.txt", 1) if use_anima_artists else [],
    }

    if gender.lower() == "female":
        parts["chest_size"] = (
            random_multiple_from_file(folder / "chest_size.txt", counts["chest_size"])
            if use_chest_size
            else []
        )
        parts["chest_shape"] = (
            random_multiple_from_file(folder / "chest_shape.txt", counts["chest_shape"])
            if use_chest_shape
            else []
        )
    else:
        parts["chest_size"] = []
        parts["chest_shape"] = []

    return parts


def get_nsfw_parts(category, gender):
    folder = DATA_DIR / category / gender

    return {
        "nsfw_clothing": random_multiple_from_file(folder / "nsfw_clothing.txt", 2),
        "nsfw_pose": random_multiple_from_file(folder / "nsfw_pose.txt", 2),
        "nsfw_actions": random_multiple_from_file(folder / "nsfw_actions.txt", 2),
        "nsfw_details": random_multiple_from_file(folder / "nsfw_details.txt", 2),
    }


def get_furry_parts(category, gender):
    if category != "furry":
        return {}

    folder = DATA_DIR / category / gender

    return {
        "species": random_multiple_from_file(folder / "species.txt", 1),
        "fur": random_multiple_from_file(folder / "fur.txt", 2),
        "ears": random_multiple_from_file(folder / "ears.txt", 1),
        "tail": random_multiple_from_file(folder / "tail.txt", 1),
    }


def join_parts(items):
    return ", ".join(item for item in items if item)


def get_pronoun(gender="female"):
    gender = gender.lower()
    if gender == "male":
        return "He"
    if gender == "female":
        return "She"
    return "They"


def get_gender_label(gender="female"):
    gender = gender.lower()
    if gender == "male":
        return "man"
    if gender == "female":
        return "woman"
    return "person"


def build_identity_text(gender_label, ethnicity, skin_tone, category="portrait"):
    if category == "furry":
        gender_label = f"{gender_label}, furry, anthro"

    if ethnicity and skin_tone:
        return f"{ethnicity} {gender_label} with {skin_tone}"
    if ethnicity:
        return f"{ethnicity} {gender_label}"
    if skin_tone:
        return f"{gender_label} with {skin_tone}"
    return gender_label


def get_anima_gender_tags(gender="female", category="portrait"):
    gender = gender.lower()

    if gender == "male":
        tags = ["1boy", "male", "man"]
    elif gender == "female":
        tags = ["1girl", "female", "woman"]
    else:
        tags = ["solo", "person"]

    if category == "furry":
        tags.extend(["furry", "anthro"])

    return tags


def build_flux_prompt(parts, gender="female"):
    pronoun = get_pronoun(gender)
    gender_label = get_gender_label(gender)

    def p(key):
        return join_parts(parts.get(key, []))

    def extend_from(keys):
        output = []
        for key in keys:
            value = parts.get(key, [])
            if isinstance(value, str):
                if value:
                    output.append(value)
            else:
                output.extend(value)
        return [item for item in output if item]

    ethnicity = p("ethnicity")
    skin_tone = p("skin_tone")

    identity_text = build_identity_text(
        gender_label,
        ethnicity,
        skin_tone,
        category=parts.get("category", "portrait")
    )

    anime_prefix = ""
    if parts.get("category") == "anime":
        anime_prefix = "anime style, anime artwork, anime illustration, "

    subject = parts.get("subject", "")
    species = p("species")

    if parts.get("category") == "furry":
        prompt = f"{anime_prefix}A highly detailed furry portrait of a {identity_text}"
    else:
        prompt = f"{anime_prefix}A highly detailed portrait of a {identity_text}"

    if subject:
        if species:
            prompt += f", a {subject} of the {species} species"
        else:
            prompt += f", a {subject}"

    sentences = [prompt + "."]

    # 1. BODY SLOT
    body_items = extend_from([
        "fur", "tail",
        "body_shape", "height", "frame", "waist", "hips", "butt",
        "legs", "shoulders", "fitness", "proportions",
        "chest_size", "chest_shape","nipples", "areola", "pussy_cocks",
    ])
    if body_items:
        sentences.append(f"The character has {join_parts(body_items)}.")

    # 2. FACE SLOT
    face_items = extend_from([
        "facial_features", "face_shape", "eye_colors", "eye_shapes",
        "eyebrows", "eyelashes", "ears", "earrings", "nose", "lips",
        "chin", "jawline", "cheeks", "face_piercings", "face_tattoos", "makeup",
    ])
    if face_items:
        sentences.append(f"Facial details include {join_parts(face_items)}.")

    # 3. HAIR SLOT
    hair_items = extend_from([
        "hair_colors", "hairstyles", "beards", "hair_accessories",
    ])
    if hair_items:
        sentences.append(f"Hair and grooming details include {join_parts(hair_items)}.")

    # 4. EXPRESSION SLOT
    expression = p("expression")
    if expression:
        sentences.append(f"The expression is {expression}.")

    # 5. OUTFIT SLOT
    outfit_items = extend_from([
        "full_outfits", "mature_outfits",
        "upper_body", "mature_upper_body",
        "lower_body", "mature_lower_body",
        "outerwear", "legwear", "footwear",
    ])

    nude_body = p("nude_body")
    if nude_body:
        sentences.append(f"The character is {nude_body}.")
    if outfit_items:
        sentences.append(f"{pronoun} is wearing {join_parts(outfit_items)}.")

    # 6. ACCESSORIES SLOT
    accessory_items = extend_from([
        "fashion_accessories", "headwear", "eyewear", "masks",
    ])
    accessory_items = [item for item in accessory_items if item.lower() != "no mask"]
    if accessory_items:
        sentences.append(f"Accessories include {join_parts(accessory_items)}.")

    # 7. POSE SLOT
    pose_items = extend_from(["body_pose", "hand_pose"])
    if pose_items:
        sentences.append(f"{pronoun} is posed with {join_parts(pose_items)}.")

    # 8. CAMERA SLOT
    camera = p("camera")
    if camera:
        sentences.append(f"Camera and composition: {camera}.")

    # 9. LIGHTING SLOT
    lighting = p("lighting")
    if lighting:
        sentences.append(f"Lighting: {lighting}.")

    # 10. ENVIRONMENT SLOT
    background_items = extend_from(["interior", "exterior", "simple_background"])
    if background_items:
        sentences.append(f"The background shows {join_parts(background_items)}.")

    # 11. ARTSTYLE SLOT
    artstyle = p("artstyle")
    if artstyle:
        sentences.append(f"Rendered as {artstyle}.")

    # 12. STYLE THEME SLOT
    style_theme = p("style_theme")
    if style_theme:
        sentences.append(f" {style_theme}.")

    # 13. DETAILS SLOT
    details = p("details")
    if details:
        sentences.append(f" {details}.")

    # 14. BOOSTERS SLOT
    boosters = p("boosters")
    if boosters:
        sentences.append(f" {boosters}.")


    # 15. NSFW SLOT 
    nsfw_actions = p("nsfw_actions")
    if nsfw_actions:
        sentences.append(f" {nsfw_actions}.")
    
    return " ".join(sentence for sentence in sentences if sentence)



def build_anima_prompt(parts, gender="female"):
    prompt_parts = [
        "score_7",
        "masterpiece",
        "best quality",
        "highly detailed",
    ]

    def extend(keys):
        for key in keys:
            prompt_parts.extend(parts.get(key, []))

    if parts.get("category") == "anime":
        prompt_parts.extend([
            "anime style",
            "anime artwork",
            "anime illustration"
        ])

    prompt_parts.extend(
        get_anima_gender_tags(
            gender,
            category=parts.get("category", "portrait")
        )
    )

    if parts.get("subject"):
        prompt_parts.append(parts["subject"])

    # Same fixed slot order as Flux.
    extend(["ethnicity", "skin_tone"])
    extend(["species", "fur", "tail"])

    extend([
        "body_shape", "height", "frame", "waist", "hips", "butt",
        "legs", "shoulders", "fitness", "proportions",
        "chest_size", "chest_shape",
    ])

    extend([
        "facial_features", "face_shape", "eye_colors", "eye_shapes",
        "eyebrows", "eyelashes", "ears", "earrings", "nose", "lips",
        "chin", "jawline", "cheeks", "face_piercings", "face_tattoos", "makeup",
    ])

    extend(["hair_colors", "hairstyles", "beards", "hair_accessories"])
    extend(["expression"])

    extend([
        "nude_body",
        "full_outfits", "mature_outfits",
        "nipples", "areola", "nsfw_actions", "pussy_cocks",
        "upper_body", "mature_upper_body",
        "lower_body", "mature_lower_body",
        "outerwear", "legwear", "footwear",
    ])

    extend(["fashion_accessories", "headwear", "eyewear"])

    prompt_parts.extend([
        item for item in parts.get("masks", [])
        if item.lower() != "no mask"
    ])

    extend(["body_pose", "hand_pose"])
    extend(["camera"])
    extend(["lighting"])
    extend(["interior", "exterior", "simple_background"])
    extend(["artstyle"])
    extend(["anima_artists"])
    extend(["style_theme"])
    extend(["details"])
    extend(["boosters"])

    return ", ".join(item for item in prompt_parts if item)



# ---------------------------------------------------------------------------
# Conflict rules + dedupe
# ---------------------------------------------------------------------------
@lru_cache(maxsize=4)
def _load_conflicts_cached(path_str, _mtime_ns):
    with open(path_str, "r", encoding="utf-8") as f:
        return json.load(f)


def load_conflicts():
    """Load the user-tunable conflict table (data/rules/conflicts.json).

    Returns {} when the file is absent or invalid, so the engine always falls
    back to its built-in clothing/background logic.
    """
    p = RULES_DIR / "conflicts.json"
    if not p.exists():
        return {}
    try:
        return _load_conflicts_cached(str(p), p.stat().st_mtime_ns)
    except Exception as e:
        print(f"[JDX Generator] Could not parse conflicts.json: {e}")
        return {}


def apply_conflict_rules(parts, conflicts):
    """Apply user-defined conflicts AFTER the built-in rules.

    directed_slot_rules: [{"if_present": "headwear", "remove": ["hairstyles"]}]
        -> if the trigger slot has any tag, clear each listed target slot.
    exclusive_slot_groups: [["interior", "exterior", "simple_background"]]
        -> keep only one slot in the group (deterministic under the seed).
    """
    if not conflicts:
        return parts

    for rule in conflicts.get("directed_slot_rules", []):
        trigger = rule.get("if_present")
        if trigger and parts.get(trigger):
            for target in rule.get("remove", []):
                if target in parts:
                    parts[target] = []

    for group in conflicts.get("exclusive_slot_groups", []):
        present = [k for k in group if parts.get(k)]
        if len(present) > 1:
            if _master_seed is None:
                keep = random.choice(present)
            else:
                keep = random.Random(
                    _derive_seed(_master_seed, "conflict", *present)
                ).choice(present)
            for k in present:
                if k != keep:
                    parts[k] = []

    return parts


def dedupe_parts(parts):
    """Drop exact (case-insensitive) duplicate tags across all list-valued slots.

    The subject string is seeded into 'seen' first so a list tag identical to
    the subject is removed while the subject itself is preserved.
    """
    seen = set()
    subject = parts.get("subject")
    if isinstance(subject, str) and subject.strip():
        seen.add(subject.strip().lower())

    for key, value in parts.items():
        if isinstance(value, list):
            unique = []
            for tag in value:
                norm = tag.strip().lower()
                if norm and norm not in seen:
                    seen.add(norm)
                    unique.append(tag)
            parts[key] = unique

    return parts


# ---------------------------------------------------------------------------
# Recipes (save / load for verbatim reproduction)
# ---------------------------------------------------------------------------
def build_recipe(**kwargs):
    """Resolve a prompt and return a JSON-serialisable recipe dict.

    Same arguments as build_prompt. The recipe carries the literal prompt and
    negative prompt (for verbatim replay) plus the resolved selections and the
    full config (for inspection / rebuild).
    """
    return build_prompt(_return="recipe", **kwargs)


def render_recipe(recipe, rebuild=False):
    """Return (prompt, negative_prompt, seed) from a recipe dict.

    By default the stored literal text is returned, which reproduces the prompt
    exactly even if the wordlists or engine have since changed. With
    rebuild=True the prompt is re-assembled from the stored resolved parts.
    """
    seed = int(recipe.get("seed") or 0)
    if rebuild and isinstance(recipe.get("parts"), dict):
        parts = dict(recipe["parts"])
        gender = recipe.get("gender", "female")
        model = (recipe.get("model_name", "flux") or "flux").lower()
        if model == "anima":
            prompt = build_anima_prompt(parts, gender=gender)
        else:
            prompt = build_flux_prompt(parts, gender=gender)
        return prompt, get_negative_prompt(model), seed
    return recipe.get("prompt", ""), recipe.get("negative_prompt", ""), seed


# ---------------------------------------------------------------------------
# Data validation
# ---------------------------------------------------------------------------
def validate_data(categories=("portrait", "anime", "furry"), genders=("female", "male")):
    """Scan the wordlists and report problems. Returns (report_text, is_ok)."""
    lines = []
    problems = 0
    total_files = 0
    total_tags = 0

    for cat in categories:
        per_gender_files = {}
        for g in genders:
            d = DATA_DIR / cat / g
            if not d.is_dir():
                lines.append(f"[MISSING DIR] {cat}/{g}")
                problems += 1
                continue
            files = sorted(p.name for p in d.glob("*.txt"))
            per_gender_files[g] = set(files)
            for name in files:
                total_files += 1
                items = load_list(d / name)
                if not items:
                    lines.append(f"[EMPTY] {cat}/{g}/{name}")
                    problems += 1
                    continue
                total_tags += len(items)
                lowered = [t.strip().lower() for t, _ in items]
                dupes = len(lowered) - len(set(lowered))
                if dupes:
                    lines.append(f"[DUPES x{dupes}] {cat}/{g}/{name}")
                    problems += 1

        # Cross-gender asymmetry within the SAME category is only informational
        # (female/male lists can legitimately differ, e.g. nsfw_subject).
        if len(per_gender_files) == 2:
            a, b = genders
            only_a = sorted(per_gender_files.get(a, set()) - per_gender_files.get(b, set()))
            only_b = sorted(per_gender_files.get(b, set()) - per_gender_files.get(a, set()))
            if only_a:
                lines.append(f"[INFO] {cat}: only in {a}: {', '.join(only_a)}")
            if only_b:
                lines.append(f"[INFO] {cat}: only in {b}: {', '.join(only_b)}")

    for name in ("anima_artists.txt", "anima_boosters.txt", "flux_boosters.txt"):
        p = PROMPT_LIBRARY_DIR / name
        if not p.exists():
            lines.append(f"[MISSING] prompt_library/{name}")
            problems += 1
        elif not load_list(p):
            lines.append(f"[EMPTY] prompt_library/{name}")
            problems += 1

    cp = RULES_DIR / "conflicts.json"
    if cp.exists():
        try:
            json.loads(cp.read_text(encoding="utf-8"))
            lines.append("[OK] rules/conflicts.json parses")
        except Exception as e:
            lines.append(f"[BAD JSON] rules/conflicts.json: {e}")
            problems += 1

    header = (
        f"JDX data check — {total_files} files, {total_tags} tags. "
        + ("All good." if problems == 0 else f"{problems} issue(s) found.")
    )
    body = "\n".join(lines[:120])
    return (header + ("\n" + body if body else ""), problems == 0)


def build_prompt(
    category="portrait",
    gender="female",
    model_name="flux",
    prompt_length="medium",
    generation_mode="smart",
    seed=None,
    nsfw=False,
    use_nude=False,
    use_subject=True,
    use_ethnicity=True,
    use_skin_tone=True,
    use_hair_colors=True,
    use_hairstyles=True,
    use_beards=True,
    use_eye_colors=True,
    use_eye_shapes=True,
    use_eyebrows=True,
    use_eyelashes=True,
    use_nose=True,
    use_lips=True,
    use_chin=True,
    use_jawline=True,
    use_cheeks=True,
    use_face_shape=True,
    use_ears=True,
    use_earrings=True,
    use_expression=True,
    use_makeup=True,
    use_face_piercings=True,
    use_face_tattoos=True,
    use_upper_body=True,
    use_lower_body=True,
    use_legwear=True,
    use_footwear=True,
    use_outerwear=True,
    use_full_outfits=False,
    use_mature_upper_body=False,
    use_mature_lower_body=False,
    use_mature_outfits=False,
    use_nipples=False,
    use_areola=False,
    use_nsfw_actions=False,
    use_pussy_cocks=False,
    use_fashion_accessories=True,
    use_headwear=True,
    use_hair_accessories=True,
    use_eyewear=True,
    use_masks=True,
    use_body_shape=True,
    use_height=True,
    use_frame=True,
    use_waist=True,
    use_hips=True,
    use_butt=True,
    use_legs=True,
    use_shoulders=True,
    use_fitness=True,
    use_proportions=True,
    use_chest_size=True,
    use_chest_shape=True,
    use_facial_features=True,
    use_body_pose=True,
    use_hand_pose=True,
    use_interior=True,
    use_exterior=True,
    use_simple_background=True,
    use_artstyle=True,
    use_style_theme=True,
    use_lighting=True,
    use_camera=True,
    use_details=True,
    use_boosters=True,
    use_anima_artists=False,
    _return="prompt"
):
    # Capture the toggle set up front (these are exactly the use_* parameters)
    # so it can be stored in a recipe without listing every flag by hand.
    _toggles = {k: v for k, v in locals().items() if k.startswith("use_")}
    # Seed first, before any tag is drawn, so the same seed + same toggles
    # reproduce the exact same prompt every time.
    seed_engine(seed)

    parts = collect_parts(
        category=category,
        gender=gender,
        prompt_length=prompt_length,
        generation_mode=generation_mode,
        use_subject=use_subject,
        use_ethnicity=use_ethnicity,
        use_skin_tone=use_skin_tone,
        use_hair_colors=use_hair_colors,
        use_hairstyles=use_hairstyles,
        use_beards=use_beards,
        use_eye_colors=use_eye_colors,
        use_eye_shapes=use_eye_shapes,
        use_eyebrows=use_eyebrows,
        use_eyelashes=use_eyelashes,
        use_ears=use_ears,
        use_earrings=use_earrings,
        use_lips=use_lips,
        use_nose=use_nose,
        use_chin=use_chin,
        use_jawline=use_jawline,
        use_cheeks=use_cheeks,
        use_face_shape=use_face_shape,
        use_face_piercings=use_face_piercings,
        use_face_tattoos=use_face_tattoos,
        use_makeup=use_makeup,
        use_upper_body=use_upper_body,
        use_lower_body=use_lower_body,
        use_legwear=use_legwear,
        use_footwear=use_footwear,
        use_outerwear=use_outerwear,
        use_full_outfits=use_full_outfits,
        use_mature_upper_body=use_mature_upper_body,
        use_mature_lower_body=use_mature_lower_body,
        use_mature_outfits=use_mature_outfits,
        use_nipples=use_nipples,
        use_areola=use_areola,
        use_nsfw_actions=use_nsfw_actions,
        use_pussy_cocks=use_pussy_cocks,
        use_fashion_accessories=use_fashion_accessories,
        use_headwear=use_headwear,
        use_hair_accessories=use_hair_accessories,
        use_eyewear=use_eyewear,
        use_masks=use_masks,
        use_body_shape=use_body_shape,
        use_height=use_height,
        use_frame=use_frame,
        use_waist=use_waist,
        use_hips=use_hips,
        use_butt=use_butt,
        use_legs=use_legs,
        use_shoulders=use_shoulders,
        use_fitness=use_fitness,
        use_proportions=use_proportions,
        use_chest_size=use_chest_size,
        use_chest_shape=use_chest_shape,
        use_facial_features=use_facial_features,
        use_body_pose=use_body_pose,
        use_hand_pose=use_hand_pose,
        use_expression=use_expression,
        use_interior=use_interior,
        use_exterior=use_exterior,
        use_simple_background=use_simple_background,
        use_artstyle=use_artstyle,
        use_style_theme=use_style_theme,
        use_lighting=use_lighting,
        use_camera=use_camera,
        use_details=use_details,
        use_anima_artists=use_anima_artists
    )

    parts["category"] = category
    parts.update(get_furry_parts(category, gender))

    parts["boosters"] = (
        get_boosters(model_name=model_name, prompt_length=prompt_length)
        if use_boosters
        else []
    )

    parts = apply_generation_mode_rules(parts, generation_mode, nsfw=nsfw, use_nude=use_nude)
    parts = apply_conflict_rules(parts, load_conflicts())
    parts = dedupe_parts(parts)

    if model_name.lower() == "anima":
        prompt = build_anima_prompt(parts, gender=gender)
    else:
        prompt = build_flux_prompt(parts, gender=gender)

    if _return == "recipe":
        return {
            "engine_version": ENGINE_VERSION,
            "seed": seed,
            "category": category,
            "gender": gender,
            "model_name": model_name,
            "prompt_length": prompt_length,
            "generation_mode": generation_mode,
            "nsfw": nsfw,
            "use_nude": use_nude,
            "toggles": _toggles,
            "parts": {
                k: (list(v) if isinstance(v, (list, tuple)) else v)
                for k, v in parts.items()
            },
            "prompt": prompt,
            "negative_prompt": get_negative_prompt(model_name),
        }

    return prompt


def get_negative_prompt(model_name="flux"):
    model_name = model_name.lower()

    if model_name == "anima":
        return (
            "worst quality, "
            "low quality, "
            "score_1, "
            "score_2, "
            "score_3, "
            "artist name, "
            "young"
        )

    return ""


if __name__ == "__main__":
    print(
        build_prompt(
            category="furry",
            gender="female",
            model_name="flux",
            prompt_length="long",
            nsfw=False
        )
    )
