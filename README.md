# Image-to-Image Animal Generator

This repo contains a small utility script to generate images of other animals **matching the style and composition** of a given reference image. It leverages the [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5) *img2img* pipeline from the `diffusers` library.

---

## Setup

1. **Clone** or download the repository.

2. **Install dependencies** (ideally in a virtual environment):

```bash
pip install -r requirements.txt
```

3. **Authenticate with Hugging Face** (only once):

```bash
export HUGGINGFACE_TOKEN=<your_hf_access_token>
```

A free token is sufficient for `runwayml/stable-diffusion-v1-5`.

---

## Running the script

Assuming you have a reference image at `input/cat.jpg`, run:

```bash
python generate_animals_from_reference.py \
  --image_path input/cat.jpg \
  --animals "dog,fox,rabbit" \
  --output_dir output/ \
  --strength 0.75 \
  --num_inference_steps 50
```

Arguments explained:

* `--image_path` – Path to your reference image.
* `--animals` – Comma-separated list of target animal keywords.
* `--output_dir` – Destination directory for generated images (auto-created).
* `--strength` – Transformation strength \(0 = keep source intact, 1 = ignore it completely). Typical range: 0.4–0.8.
* `--num_inference_steps` – More steps → better quality but slower (default 50).
* `--guidance_scale` – Classifier-free guidance scale (default 7.5).
* `--model_name` – Optionally point to another checkpoint or LoRA.
* `--seed` – Fix random seed for reproducibility.

The script outputs one PNG per animal named `<timestamp>_<animal>.png` in the chosen output folder.

---

## Tips & Extensions

* For even better pose preservation, combine with a ControlNet (e.g. `lllyasviel/sd-controlnet-openpose`) and swap the pipeline accordingly.
* Try alternative checkpoints (e.g. `dreamlike-art/dreamlike-photoreal-2.0`) by passing `--model_name`.
* Tune *negative prompts* inside the script to your taste.
* Generate multiple variants per animal by looping the script with different `--seed` values.

---

Happy creating! 🐱 → 🦊 🐶 🐰