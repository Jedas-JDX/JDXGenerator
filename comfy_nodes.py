import sys
import os
import copy
import json
import inspect
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

try:
    from procedural_engine import (
        build_prompt, build_recipe, render_recipe,
        get_negative_prompt, validate_data,
    )
except ImportError:
    import scripts.procedural_engine as pe
    build_prompt = pe.build_prompt
    build_recipe = pe.build_recipe
    render_recipe = pe.render_recipe
    get_negative_prompt = pe.get_negative_prompt
    validate_data = pe.validate_data

# Valid build_prompt parameters, so a JDX_CONFIG dict can be forwarded safely
# even if it later carries keys the engine does not accept.
_BUILD_PARAMS = set(inspect.signature(build_prompt).parameters)


def _kwargs_from_cfg(cfg, seed):
    kw = {k: v for k, v in cfg.items() if k in _BUILD_PARAMS}
    kw["seed"] = seed
    return kw


def _config_fingerprint(cfg, *extra):
    try:
        cfg_repr = json.dumps(cfg, sort_keys=True, default=str)
    except Exception:
        cfg_repr = repr(cfg)
    import hashlib
    payload = "|".join([cfg_repr] + [str(e) for e in extra])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


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
                
                "use_races": ("BOOLEAN", {"default": False}),
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
                "use_arm_pose": ("BOOLEAN", {"default": False}),
                "use_leg_pose": ("BOOLEAN", {"default": False}),
                "use_head_pose": ("BOOLEAN", {"default": False}),
                "use_hand_pose": ("BOOLEAN", {"default": False}),
                "use_dynamic_pose": ("BOOLEAN", {"default": False}),
                "use_cute_pose": ("BOOLEAN", {"default": False}),
                "use_elegant_pose": ("BOOLEAN", {"default": False}),
                "use_nsfw_pose": ("BOOLEAN", {"default": False}),
                "use_interior": ("BOOLEAN", {"default": False}),
                "use_exterior": ("BOOLEAN", {"default": False}),
                "use_simple_background": ("BOOLEAN", {"default": False}),
                "use_artstyle": ("BOOLEAN", {"default": False}),
                "use_style_theme": ("BOOLEAN", {"default": False}),
                "use_lighting": ("BOOLEAN", {"default": False}),
                "use_camera_settings": ("BOOLEAN", {"default": False}),
                "use_camera_angles": ("BOOLEAN", {"default": False}),
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
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "STRING",)
    RETURN_NAMES = ("prompt", "negative_prompt", "seed", "recipe",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, jdx_config, seed):
        # Re-run only when the seed or the config actually changes, so a fixed
        # seed reproduces the same prompt (and is cached) instead of rerolling
        # on every queue. With control_after_generate set to "randomize" the
        # seed changes each run, which naturally triggers a fresh prompt.
        return _config_fingerprint(jdx_config, seed)

    def execute(self, jdx_config, seed):
        cfg = copy.deepcopy(jdx_config)
        # Backward compatibility for older workflows saved before v1.2.
        if "use_races" not in cfg and "use_subject" in cfg:
            cfg["use_races"] = cfg.get("use_subject", False)
        if "use_camera_settings" not in cfg and "use_camera" in cfg:
            cfg["use_camera_settings"] = cfg.get("use_camera", False)
        if "use_camera_angles" not in cfg and "use_camera" in cfg:
            cfg["use_camera_angles"] = cfg.get("use_camera", False)
        recipe = build_recipe(**_kwargs_from_cfg(cfg, seed))
        recipe_json = json.dumps(recipe, ensure_ascii=False)
        prompt = recipe["prompt"]
        negative_prompt = recipe["negative_prompt"]
        # The "ui" payload is read by js/jdx_show_text.js to fill the read-only
        # preview fields on the node; "result" is the normal output tuple.
        return {
            "ui": {"positive": [prompt], "negative": [negative_prompt]},
            "result": (prompt, negative_prompt, seed, recipe_json),
        }


class JDXBatchGenerate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "jdx_config": ("JDX_CONFIG",),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                }),
                "count": ("INT", {"default": 4, "min": 1, "max": 256}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT",)
    RETURN_NAMES = ("prompts", "negative_prompts", "seeds",)
    OUTPUT_IS_LIST = (True, True, True)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    @classmethod
    def IS_CHANGED(cls, jdx_config, seed, count):
        return _config_fingerprint(jdx_config, seed, count)

    def execute(self, jdx_config, seed, count):
        cfg = copy.deepcopy(jdx_config)
        # Back-compat for workflows saved before the race/camera split.
        if "use_races" not in cfg and "use_subject" in cfg:
            cfg["use_races"] = cfg.get("use_subject", False)
        if "use_camera_settings" not in cfg and "use_camera" in cfg:
            cfg["use_camera_settings"] = cfg.get("use_camera", False)
        if "use_camera_angles" not in cfg and "use_camera" in cfg:
            cfg["use_camera_angles"] = cfg.get("use_camera", False)
        prompts, negatives, seeds = [], [], []
        for i in range(int(count)):
            s = (int(seed) + i) & 0xffffffffffffffff
            recipe = build_recipe(**_kwargs_from_cfg(cfg, s))
            prompts.append(recipe["prompt"])
            negatives.append(recipe["negative_prompt"])
            seeds.append(s)
        return (prompts, negatives, seeds)


class JDXLoadRecipe:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "recipe": ("STRING", {"default": "", "multiline": True}),
                "rebuild_from_parts": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT",)
    RETURN_NAMES = ("prompt", "negative_prompt", "seed",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"

    @classmethod
    def IS_CHANGED(cls, recipe, rebuild_from_parts):
        return _config_fingerprint(recipe, rebuild_from_parts)

    def execute(self, recipe, rebuild_from_parts):
        text = (recipe or "").strip()
        if not text:
            return ("", "", 0)
        try:
            data = json.loads(text)
        except Exception as e:
            return (f"[JDX] Invalid recipe JSON: {e}", "", 0)
        prompt, negative_prompt, seed = render_recipe(data, rebuild=rebuild_from_parts)
        return (prompt, negative_prompt, int(seed))


class JDXSaveRecipe:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "recipe": ("STRING", {"forceInput": True}),
                "filename_prefix": ("STRING", {"default": "jdx_recipe"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"
    OUTPUT_NODE = True

    def _output_dir(self):
        try:
            import folder_paths
            base = folder_paths.get_output_directory()
        except Exception:
            base = str(Path(__file__).resolve().parent)
        out = os.path.join(base, "jdx_recipes")
        os.makedirs(out, exist_ok=True)
        return out

    def execute(self, recipe, filename_prefix):
        out_dir = self._output_dir()
        # sanitise the prefix and find the next free counter
        safe = "".join(c for c in (filename_prefix or "jdx_recipe")
                       if c.isalnum() or c in ("-", "_")) or "jdx_recipe"
        n = 1
        while True:
            path = os.path.join(out_dir, f"{safe}_{n:05}.json")
            if not os.path.exists(path):
                break
            n += 1
        with open(path, "w", encoding="utf-8") as f:
            f.write(recipe or "")
        print(f"[JDX Generator] Saved recipe to {path}")
        return (path,)


class JDXValidateData:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN",)
    RETURN_NAMES = ("report", "ok",)
    FUNCTION = "execute"
    CATEGORY = "JDXGenerator"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, trigger):
        # Re-scan every run; wordlists may have changed on disk.
        import time
        return time.time()

    def execute(self, trigger):
        report, ok = validate_data()
        print(report)
        return (report, ok)


NODE_CLASS_MAPPINGS = {
    "JDXBaseConfig": JDXBaseConfig,
    "JDXCharacterModifiers": JDXCharacterModifiers,
    "JDXClothingModifiers": JDXClothingModifiers,
    "JDXStyleModifiers": JDXStyleModifiers,
    "JDXGeneratePrompt": JDXGeneratePrompt,
    "JDXBatchGenerate": JDXBatchGenerate,
    "JDXLoadRecipe": JDXLoadRecipe,
    "JDXSaveRecipe": JDXSaveRecipe,
    "JDXValidateData": JDXValidateData,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JDXBaseConfig": "JDX 1. Base Config",
    "JDXCharacterModifiers": "JDX 2. Character / Race",
    "JDXClothingModifiers": "JDX 3. Clothing",
    "JDXStyleModifiers": "JDX 4. Style / Camera / Environment",
    "JDXGeneratePrompt": "JDX 5. Generate Prompt",
    "JDXBatchGenerate": "JDX 6. Batch / Variations",
    "JDXLoadRecipe": "JDX Load Recipe",
    "JDXSaveRecipe": "JDX Save Recipe",
    "JDXValidateData": "JDX Validate Data",
}
