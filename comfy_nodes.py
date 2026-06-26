import sys
import copy
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

try:
    from procedural_engine import build_prompt, get_negative_prompt
except ImportError:
    import scripts.procedural_engine as pe
    build_prompt = pe.build_prompt
    get_negative_prompt = pe.get_negative_prompt

class JDXBaseConfig:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "category": (["portrait", "anime", "furry"], {"default": "portrait"}),
                "gender": (["female", "male"], {"default": "female"}),
                "model_name": (["flux", "anima"], {"default": "flux"}),
                "prompt_length": (["short", "medium", "long"], {"default": "medium"}),
                "generation_mode": (["smart", "creative", "chaos"], {"default": "smart"}),
                "nsfw": ("BOOLEAN", {"default": False}),
                "use_nude": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ("JDX_CONFIG",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    def execute(self, **kwargs):
        return (kwargs,)


class JDXCharacterModifiers:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "jdx_config": ("JDX_CONFIG",),
                
                "use_subject": ("BOOLEAN", {"default": False}),
                "use_ethnicity": ("BOOLEAN", {"default": False}),
                "use_skin_tone": ("BOOLEAN", {"default": False}),
                
                "use_hair_colors": ("BOOLEAN", {"default": False}),
                "use_hairstyles": ("BOOLEAN", {"default": False}),
                "use_beards": ("BOOLEAN", {"default": False}),
                
                "use_eye_colors": ("BOOLEAN", {"default": False}),
                "use_eye_shapes": ("BOOLEAN", {"default": False}),
                "use_eyebrows": ("BOOLEAN", {"default": False}),
                "use_eyelashes": ("BOOLEAN", {"default": False}),
                
                "use_nose": ("BOOLEAN", {"default": False}),
                "use_lips": ("BOOLEAN", {"default": False}),
                "use_chin": ("BOOLEAN", {"default": False}),
                "use_jawline": ("BOOLEAN", {"default": False}),
                "use_cheeks": ("BOOLEAN", {"default": False}),
                "use_face_shape": ("BOOLEAN", {"default": False}),
                "use_ears": ("BOOLEAN", {"default": False}),
                "use_earrings": ("BOOLEAN", {"default": False}),
                "use_expression": ("BOOLEAN", {"default": False}),
                "use_makeup": ("BOOLEAN", {"default": False}),
                "use_facial_features": ("BOOLEAN", {"default": False}),
                "use_face_piercings": ("BOOLEAN", {"default": False}),
                "use_face_tattoos": ("BOOLEAN", {"default": False}),
                
                "use_body_shape": ("BOOLEAN", {"default": False}),
                "use_height": ("BOOLEAN", {"default": False}),
                "use_frame": ("BOOLEAN", {"default": False}),
                "use_waist": ("BOOLEAN", {"default": False}),
                "use_hips": ("BOOLEAN", {"default": False}),
                "use_butt": ("BOOLEAN", {"default": False}),
                "use_legs": ("BOOLEAN", {"default": False}),
                "use_shoulders": ("BOOLEAN", {"default": False}),
                "use_fitness": ("BOOLEAN", {"default": False}),
                "use_proportions": ("BOOLEAN", {"default": False}),
                "use_chest_size": ("BOOLEAN", {"default": False}),
                "use_chest_shape": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ("JDX_CONFIG",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    def execute(self, jdx_config, **kwargs):
        cfg = copy.deepcopy(jdx_config)
        cfg.update(kwargs)
        return (cfg,)


class JDXClothingModifiers:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "jdx_config": ("JDX_CONFIG",),
                
                "use_upper_body": ("BOOLEAN", {"default": False}),
                "use_lower_body": ("BOOLEAN", {"default": False}),
                "use_legwear": ("BOOLEAN", {"default": False}),
                "use_footwear": ("BOOLEAN", {"default": False}),
                "use_outerwear": ("BOOLEAN", {"default": False}),
                "use_full_outfits": ("BOOLEAN", {"default": False}),
                "use_mature_upper_body": ("BOOLEAN", {"default": False}),
                "use_mature_lower_body": ("BOOLEAN", {"default": False}),
                "use_mature_outfits": ("BOOLEAN", {"default": False}),
                "use_nipples": ("BOOLEAN", {"default": False}),
                "use_areola": ("BOOLEAN", {"default": False}),
                "use_nsfw_actions": ("BOOLEAN", {"default": False}),
                "use_pussy_cocks": ("BOOLEAN", {"default": False}),
                "use_fashion_accessories": ("BOOLEAN", {"default": False}),
                "use_headwear": ("BOOLEAN", {"default": False}),
                "use_hair_accessories": ("BOOLEAN", {"default": False}),
                "use_eyewear": ("BOOLEAN", {"default": False}),
                "use_masks": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ("JDX_CONFIG",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    def execute(self, jdx_config, **kwargs):
        cfg = copy.deepcopy(jdx_config)
        cfg.update(kwargs)
        return (cfg,)


class JDXStyleModifiers:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "jdx_config": ("JDX_CONFIG",),
                
                "use_body_pose": ("BOOLEAN", {"default": False}),
                "use_hand_pose": ("BOOLEAN", {"default": False}),
                "use_interior": ("BOOLEAN", {"default": False}),
                "use_exterior": ("BOOLEAN", {"default": False}),
                "use_simple_background": ("BOOLEAN", {"default": False}),
                "use_artstyle": ("BOOLEAN", {"default": False}),
                "use_style_theme": ("BOOLEAN", {"default": False}),
                "use_lighting": ("BOOLEAN", {"default": False}),
                "use_camera": ("BOOLEAN", {"default": False}),
                "use_details": ("BOOLEAN", {"default": False}),
                "use_boosters": ("BOOLEAN", {"default": False}),
                "use_anima_artists": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ("JDX_CONFIG",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    def execute(self, jdx_config, **kwargs):
        cfg = copy.deepcopy(jdx_config)
        cfg.update(kwargs)
        return (cfg,)


class JDXGeneratePrompt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "jdx_config": ("JDX_CONFIG",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "negative_prompt",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    @classmethod
    def IS_CHANGED(cls, jdx_config):
        import time
        return time.time()

    def execute(self, jdx_config):
        cfg = copy.deepcopy(jdx_config)
        
        # Build prompt extracts exactly what it needs from the config dictionary
        prompt = build_prompt(
            category=cfg.get("category", "portrait"),
            gender=cfg.get("gender", "female"),
            model_name=cfg.get("model_name", "flux"),
            prompt_length=cfg.get("prompt_length", "medium"),
            generation_mode=cfg.get("generation_mode", "smart"),
            nsfw=cfg.get("nsfw", False),
            use_nude=cfg.get("use_nude", False),
            
            use_subject=cfg.get("use_subject", False),
            use_ethnicity=cfg.get("use_ethnicity", False),
            use_skin_tone=cfg.get("use_skin_tone", False),
            
            use_hair_colors=cfg.get("use_hair_colors", False),
            use_hairstyles=cfg.get("use_hairstyles", False),
            use_beards=cfg.get("use_beards", False),
            
            use_eye_colors=cfg.get("use_eye_colors", False),
            use_eye_shapes=cfg.get("use_eye_shapes", False),
            use_eyebrows=cfg.get("use_eyebrows", False),
            use_eyelashes=cfg.get("use_eyelashes", False),
            
            use_nose=cfg.get("use_nose", False),
            use_lips=cfg.get("use_lips", False),
            use_chin=cfg.get("use_chin", False),
            use_jawline=cfg.get("use_jawline", False),
            use_cheeks=cfg.get("use_cheeks", False),
            use_face_shape=cfg.get("use_face_shape", False),
            use_ears=cfg.get("use_ears", False),
            use_earrings=cfg.get("use_earrings", False),
            use_expression=cfg.get("use_expression", False),
            use_makeup=cfg.get("use_makeup", False),
            use_facial_features=cfg.get("use_facial_features", False),
            use_face_piercings=cfg.get("use_face_piercings", False),
            use_face_tattoos=cfg.get("use_face_tattoos", False),
            
            use_body_shape=cfg.get("use_body_shape", False),
            use_height=cfg.get("use_height", False),
            use_frame=cfg.get("use_frame", False),
            use_waist=cfg.get("use_waist", False),
            use_hips=cfg.get("use_hips", False),
            use_butt=cfg.get("use_butt", False),
            use_legs=cfg.get("use_legs", False),
            use_shoulders=cfg.get("use_shoulders", False),
            use_fitness=cfg.get("use_fitness", False),
            use_proportions=cfg.get("use_proportions", False),
            use_chest_size=cfg.get("use_chest_size", False),
            use_chest_shape=cfg.get("use_chest_shape", False),
            
            use_upper_body=cfg.get("use_upper_body", False),
            use_lower_body=cfg.get("use_lower_body", False),
            use_legwear=cfg.get("use_legwear", False),
            use_footwear=cfg.get("use_footwear", False),
            use_outerwear=cfg.get("use_outerwear", False),
            use_full_outfits=cfg.get("use_full_outfits", False),
            use_mature_upper_body=cfg.get("use_mature_upper_body", False),
            use_mature_lower_body=cfg.get("use_mature_lower_body", False),
            use_mature_outfits=cfg.get("use_mature_outfits", False),
            use_nipples=cfg.get("use_nipples", False),
            use_areola=cfg.get("use_areola", False),
            use_nsfw_actions=cfg.get("use_nsfw_actions", False),
            use_pussy_cocks=cfg.get("use_pussy_cocks", False),
            use_fashion_accessories=cfg.get("use_fashion_accessories", False),
            use_headwear=cfg.get("use_headwear", False),
            use_hair_accessories=cfg.get("use_hair_accessories", False),
            use_eyewear=cfg.get("use_eyewear", False),
            use_masks=cfg.get("use_masks", False),
            
            use_body_pose=cfg.get("use_body_pose", False),
            use_hand_pose=cfg.get("use_hand_pose", False),
            
            use_interior=cfg.get("use_interior", False),
            use_exterior=cfg.get("use_exterior", False),
            use_simple_background=cfg.get("use_simple_background", False),
            
            use_artstyle=cfg.get("use_artstyle", False),
            use_style_theme=cfg.get("use_style_theme", False),
            use_lighting=cfg.get("use_lighting", False),
            use_camera=cfg.get("use_camera", False),
            use_details=cfg.get("use_details", False),
            use_boosters=cfg.get("use_boosters", False),
            use_anima_artists=cfg.get("use_anima_artists", False)
        )
        negative_prompt = get_negative_prompt(model_name=cfg.get("model_name", "flux"))
        
        return (prompt, negative_prompt)

NODE_CLASS_MAPPINGS = {
    "JDXBaseConfig": JDXBaseConfig,
    "JDXCharacterModifiers": JDXCharacterModifiers,
    "JDXClothingModifiers": JDXClothingModifiers,
    "JDXStyleModifiers": JDXStyleModifiers,
    "JDXGeneratePrompt": JDXGeneratePrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JDXBaseConfig": "JDX 1. Base Config",
    "JDXCharacterModifiers": "JDX 2. Character",
    "JDXClothingModifiers": "JDX 3. Clothing",
    "JDXStyleModifiers": "JDX 4. Style & Environment",
    "JDXGeneratePrompt": "JDX 5. Generate Prompt"
}
