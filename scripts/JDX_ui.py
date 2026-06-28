import sys
from pathlib import Path

import gradio as gr
from modules import scripts

SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from procedural_engine import build_prompt, get_negative_prompt


def generate_prompt(
    category, gender, model_name, prompt_length, generation_mode, nsfw, use_nude,

    use_races, use_ethnicity, use_skin_tone,

    use_hair_colors, use_hairstyles, use_beards,

    use_eye_colors, use_eye_shapes, use_eyebrows, use_eyelashes,

    use_nose, use_lips, use_chin, use_jawline, use_cheeks, use_face_shape,
    use_ears, use_earrings,
    use_expression, use_makeup,
    use_facial_features, use_face_piercings, use_face_tattoos,

    use_body_shape, use_height, use_frame,
    use_waist, use_hips, use_butt, use_legs,
    use_shoulders, use_fitness, use_proportions,
    use_chest_size, use_chest_shape,

    use_upper_body, use_lower_body, use_legwear, use_footwear,
    use_outerwear, use_full_outfits,
    use_mature_upper_body, use_mature_lower_body,
    use_mature_outfits, use_nipples,
    use_areola, use_nsfw_actions, use_pussy_cocks,
    use_fashion_accessories,
    use_headwear, use_hair_accessories, use_eyewear,
    use_masks,

    use_body_pose, use_arm_pose, use_leg_pose, use_head_pose,
    use_hand_pose, use_dynamic_pose, use_cute_pose, use_elegant_pose, use_nsfw_pose,

    use_interior, use_exterior, use_simple_background,

    use_artstyle, use_style_theme,
    use_lighting, use_camera_settings, use_camera_angles,
    use_details, use_boosters, use_anima_artists
):
    prompt = build_prompt(
        category=category,
        gender=gender,
        model_name=model_name,
        prompt_length=prompt_length,
        generation_mode=generation_mode,
        nsfw=nsfw,
        use_nude=use_nude,

        use_races=use_races,
        use_ethnicity=use_ethnicity,
        use_skin_tone=use_skin_tone,

        use_hair_colors=use_hair_colors,
        use_hairstyles=use_hairstyles,
        use_beards=use_beards,

        use_eye_colors=use_eye_colors,
        use_eye_shapes=use_eye_shapes,
        use_eyebrows=use_eyebrows,
        use_eyelashes=use_eyelashes,

        use_nose=use_nose,
        use_lips=use_lips,
        use_chin=use_chin,
        use_jawline=use_jawline,
        use_cheeks=use_cheeks,
        use_face_shape=use_face_shape,
        use_ears=use_ears,
        use_earrings=use_earrings,
        use_expression=use_expression,
        use_makeup=use_makeup,
        use_facial_features=use_facial_features,
        use_face_piercings=use_face_piercings,
        use_face_tattoos=use_face_tattoos,

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

        use_body_pose=use_body_pose,
        use_arm_pose=use_arm_pose,
        use_leg_pose=use_leg_pose,
        use_head_pose=use_head_pose,
        use_hand_pose=use_hand_pose,
        use_dynamic_pose=use_dynamic_pose,
        use_cute_pose=use_cute_pose,
        use_elegant_pose=use_elegant_pose,
        use_nsfw_pose=use_nsfw_pose,

        use_interior=use_interior,
        use_exterior=use_exterior,
        use_simple_background=use_simple_background,

        use_artstyle=use_artstyle,
        use_style_theme=use_style_theme,
        use_lighting=use_lighting,
        use_camera_settings=use_camera_settings,
        use_camera_angles=use_camera_angles,
        use_details=use_details,
        use_boosters=use_boosters,
        use_anima_artists=use_anima_artists
    )

    negative_prompt = get_negative_prompt(model_name=model_name)
    return prompt, negative_prompt


class Script(scripts.Script):

    def title(self):
        return "JDX Generator"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):

        with gr.Accordion("JDX Generator", open=True):

            with gr.Row():
                category = gr.Dropdown(
                    choices=["portrait", "anime", "furry"],
                    value="portrait",
                    label="Category"
                )

                gender = gr.Dropdown(
                    choices=["female", "male"],
                    value="female",
                    label="Gender"
                )

                model_name = gr.Dropdown(
                    choices=["flux", "anima"],
                    value="flux",
                    label="Model"
                )

                prompt_length = gr.Dropdown(
                    choices=["short", "medium", "long"],
                    value="medium",
                    label="Prompt Length"
                )

                generation_mode = gr.Dropdown(
                    choices=["smart", "creative", "chaos"],
                    value="smart",
                    label="Generation Mode"
                )

            with gr.Accordion("Prompt Builder", open=True):

                with gr.Tabs():

                    with gr.Tab("Character"):
                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### Core")
                                use_races = gr.Checkbox(value=False, label="Races / Species")
                                use_ethnicity = gr.Checkbox(value=False, label="Ethnicity")
                                use_skin_tone = gr.Checkbox(value=False, label="Skin Tone")

                            with gr.Column():
                                gr.Markdown("### Eyes")
                                use_eye_colors = gr.Checkbox(value=False, label="Eye Colors")
                                use_eye_shapes = gr.Checkbox(value=False, label="Eye Shapes")
                                use_eyebrows = gr.Checkbox(value=False, label="Eyebrows")
                                use_eyelashes = gr.Checkbox(value=False, label="Eyelashes")

                            with gr.Column():
                                gr.Markdown("### Face Structure")
                                use_face_shape = gr.Checkbox(value=False, label="Face Shape")
                                use_nose = gr.Checkbox(value=False, label="Nose")
                                use_lips = gr.Checkbox(value=False, label="Lips")
                                use_chin = gr.Checkbox(value=False, label="Chin")
                                use_jawline = gr.Checkbox(value=False, label="Jawline")
                                use_cheeks = gr.Checkbox(value=False, label="Cheeks")
                                use_facial_features = gr.Checkbox(value=False, label="Facial Features")

                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### Face Details")
                                use_ears = gr.Checkbox(value=False, label="Ears")
                                use_earrings = gr.Checkbox(value=False, label="Earrings")
                                use_expression = gr.Checkbox(value=False, label="Expression")
                                use_makeup = gr.Checkbox(value=False, label="Makeup")
                                use_face_piercings = gr.Checkbox(value=False, label="Face Piercings")
                                use_face_tattoos = gr.Checkbox(value=False, label="Face Tattoos")

                            with gr.Column():
                                gr.Markdown("### Hair")
                                use_hair_colors = gr.Checkbox(value=False, label="Hair Colors")
                                use_hairstyles = gr.Checkbox(value=False, label="Hairstyles")
                                use_beards = gr.Checkbox(value=False, label="Beards")

                    with gr.Tab("Body"):
                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### Body Shape")
                                use_body_shape = gr.Checkbox(value=False, label="Body Shape")
                                use_height = gr.Checkbox(value=False, label="Height")
                                use_frame = gr.Checkbox(value=False, label="Frame")
                                use_proportions = gr.Checkbox(value=False, label="Proportions")

                            with gr.Column():
                                gr.Markdown("### Body Details")
                                use_waist = gr.Checkbox(value=False, label="Waist")
                                use_hips = gr.Checkbox(value=False, label="Hips")
                                use_butt = gr.Checkbox(value=False, label="Butt")
                                use_legs = gr.Checkbox(value=False, label="Legs")
                                use_shoulders = gr.Checkbox(value=False, label="Shoulders")
                                use_fitness = gr.Checkbox(value=False, label="Fitness")
                                use_chest_size = gr.Checkbox(value=False, label="Chest Size")
                                use_chest_shape = gr.Checkbox(value=False, label="Chest Shape")

                    with gr.Tab("Fashion"):
                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### Clothing")
                                use_upper_body = gr.Checkbox(value=False, label="Upper Body")
                                use_lower_body = gr.Checkbox(value=False, label="Lower Body")
                                use_legwear = gr.Checkbox(value=False, label="Legwear")
                                use_footwear = gr.Checkbox(value=False, label="Footwear")
                                use_outerwear = gr.Checkbox(value=False, label="Outerwear")
                                use_full_outfits = gr.Checkbox(value=False, label="Full Outfits")
                                use_fashion_accessories = gr.Checkbox(value=False, label="Fashion Accessories")

                            with gr.Column():
                                gr.Markdown("### Head / Extra")
                                use_headwear = gr.Checkbox(value=False, label="Headwear")
                                use_hair_accessories = gr.Checkbox(value=False, label="Hair Accessories")
                                use_eyewear = gr.Checkbox(value=False, label="Eyewear")
                                use_masks = gr.Checkbox(value=False, label="Masks")

                    with gr.Tab("Scene & Style"):
                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### Posing")
                                use_body_pose = gr.Checkbox(value=False, label="Body Pose")
                                use_arm_pose = gr.Checkbox(value=False, label="Arm Pose")
                                use_leg_pose = gr.Checkbox(value=False, label="Leg Pose")
                                use_head_pose = gr.Checkbox(value=False, label="Head Pose")
                                use_hand_pose = gr.Checkbox(value=False, label="Hand Pose")
                                use_dynamic_pose = gr.Checkbox(value=False, label="Dynamic Pose")
                                use_cute_pose = gr.Checkbox(value=False, label="Cute Pose")
                                use_elegant_pose = gr.Checkbox(value=False, label="Elegant Pose")
                                use_nsfw_pose = gr.Checkbox(value=False, label="NSFW Pose" )

                            with gr.Column():
                                gr.Markdown("### Background")
                                use_interior = gr.Checkbox(value=False, label="Interior")
                                use_exterior = gr.Checkbox(value=False, label="Exterior")
                                use_simple_background = gr.Checkbox(value=False, label="Simple Background")

                            with gr.Column():
                                gr.Markdown("### Style")
                                use_artstyle = gr.Checkbox(value=False, label="Artstyle")
                                use_style_theme = gr.Checkbox(value=False, label="Style Theme")
                                use_lighting = gr.Checkbox(value=False, label="Lighting")
                                use_camera_settings = gr.Checkbox(value=False, label="Camera Settings")
                                use_camera_angles = gr.Checkbox(value=False, label="Camera Angles")
                                use_details = gr.Checkbox(value=False, label="Details")
                                use_boosters = gr.Checkbox(value=False, label="Boosters")
                                use_anima_artists = gr.Checkbox(value=False, label="Anima Artists")

                    with gr.Tab("NSFW"):
                        with gr.Row():

                            with gr.Column():
                                gr.Markdown("### NSFW Mode")
                                nsfw = gr.Checkbox(value=False, label="Enable NSFW")
                                use_nude = gr.Checkbox(value=False, label="Nude Body")

                            with gr.Column():
                                gr.Markdown("### Mature Fashion")
                                use_mature_upper_body = gr.Checkbox(value=False, label="Mature Upper Body")
                                use_mature_lower_body = gr.Checkbox(value=False, label="Mature Lower Body")
                                use_mature_outfits = gr.Checkbox(value=False, label="Mature Outfits")
                                use_nipples = gr.Checkbox(value=False, label="Nipples")
                                use_areola = gr.Checkbox(value=False, label="Areola")
                                use_nsfw_actions = gr.Checkbox(value=False, label="NSFW Actions")
                                use_pussy_cocks = gr.Checkbox(value=False, label="Pussy & Cocks")

                            with gr.Column():
                                gr.Markdown("### Info")
                                gr.Markdown(
                                    "Enable NSFW to unlock mature prompt behavior. Nude Body removes upper body, "
                                    "lower body, outerwear, full outfits and mature clothing, then adds nude body. "
                                    "Legwear, footwear and accessories can still be used."
                                )

            generated_prompt = gr.Textbox(
                lines=10,
                label="Generated Prompt",
                show_copy_button=True
            )

            negative_prompt = gr.Textbox(
                lines=4,
                label="Negative Prompt",
                show_copy_button=True
            )

            with gr.Row():
                generate_btn = gr.Button("Generate Prompt")
                clear_all_btn = gr.Button("Clear All")
                send_to_prompt_btn = gr.Button("Send to Prompt")

            all_inputs = [
                category, gender, model_name, prompt_length, generation_mode, nsfw, use_nude,

                use_races, use_ethnicity, use_skin_tone,

                use_hair_colors, use_hairstyles, use_beards,

                use_eye_colors, use_eye_shapes, use_eyebrows, use_eyelashes,

                use_nose, use_lips, use_chin, use_jawline, use_cheeks, use_face_shape,
                use_ears, use_earrings,
                use_expression, use_makeup,
                use_facial_features, use_face_piercings, use_face_tattoos,

                use_body_shape, use_height, use_frame,
                use_waist, use_hips, use_butt, use_legs,
                use_shoulders, use_fitness, use_proportions,
                use_chest_size, use_chest_shape,

                use_upper_body, use_lower_body, use_legwear, use_footwear,
                use_outerwear, use_full_outfits,
                use_mature_upper_body, use_mature_lower_body,
                use_mature_outfits, use_nipples,
                use_areola, use_nsfw_actions, use_pussy_cocks,
                use_fashion_accessories,
                use_headwear, use_hair_accessories, use_eyewear,
                use_masks,

                use_body_pose, use_arm_pose, use_leg_pose, use_head_pose,
    use_hand_pose, use_dynamic_pose, use_cute_pose, use_elegant_pose, use_nsfw_pose,

                use_interior, use_exterior, use_simple_background,

                use_artstyle, use_style_theme,
                use_lighting, use_camera_settings, use_camera_angles,
                use_details, use_boosters, use_anima_artists
            ]

            generate_btn.click(
                generate_prompt,
                inputs=all_inputs,
                outputs=[generated_prompt, negative_prompt]
            )

            send_to_prompt_btn.click(
                fn=lambda prompt, negative: (prompt, negative),
                inputs=[generated_prompt, negative_prompt],
                outputs=[generated_prompt, negative_prompt],
                _js="""
                (prompt, negative) => {
                    const root = typeof gradioApp === "function" ? gradioApp() : document;

                    const setField = (selectors, value) => {
                        for (const selector of selectors) {
                            const field = root.querySelector(selector);

                            if (field) {
                                field.value = value;

                                field.dispatchEvent(new Event("input", {
                                    bubbles: true
                                }));

                                field.dispatchEvent(new Event("change", {
                                    bubbles: true
                                }));

                                if (typeof updateInput === "function") {
                                    updateInput(field);
                                }

                                return true;
                            }
                        }

                        return false;
                    };

                    setField([
                        "#txt2img_prompt textarea",
                        "#txt2img_prompt > label > textarea",
                        "textarea[data-testid='textbox']"
                    ], prompt);

                    setField([
                        "#txt2img_neg_prompt textarea",
                        "#txt2img_neg_prompt > label > textarea"
                    ], negative);

                    setField([
                        "#img2img_prompt textarea",
                        "#img2img_prompt > label > textarea"
                    ], prompt);

                    setField([
                        "#img2img_neg_prompt textarea",
                        "#img2img_neg_prompt > label > textarea"
                    ], negative);

                    return [prompt, negative];
                }
                """
            )


            clear_all_btn.click(
                fn=None,
                inputs=[],
                outputs=[],
                _js="""
                () => {
                    const root = typeof gradioApp === "function" ? gradioApp() : document;

                    root.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                        if (cb.checked) {
                            cb.click();
                        }
                    });

                    return [];
                }
                """
            )

        return []
