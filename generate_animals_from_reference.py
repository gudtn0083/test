#!/usr/bin/env python
"""Generate images of different animals that match the style and composition of a reference image.

Example usage:
    python generate_animals_from_reference.py \
        --image_path input/cat.jpg \
        --output_dir output/ \
        --animals "dog,fox,rabbit" \
        --num_inference_steps 50 \
        --strength 0.75

Prerequisites:
1. `pip install -r requirements.txt`
2. Set your Hugging Face access token via environment variable `export HUGGINGFACE_TOKEN=your_token`

This script will create one image per requested animal, saved under the specified output directory.
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import List

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate animal images similar to a reference image")
    parser.add_argument("--image_path", type=str, required=True, help="Path to the reference image")
    parser.add_argument("--animals", type=str, required=True, help="Comma-separated list of animal names, e.g. 'dog,fox,wolf'")
    parser.add_argument("--output_dir", type=str, default="generated_animals", help="Directory to store generated images")
    parser.add_argument("--model_name", type=str, default="runwayml/stable-diffusion-v1-5", help="Stable Diffusion checkpoint or repo id")
    parser.add_argument("--num_inference_steps", type=int, default=50, help="Number of inference steps")
    parser.add_argument("--guidance_scale", type=float, default=7.5, help="Classifier-free guidance scale")
    parser.add_argument("--strength", type=float, default=0.75, help="How much to transform the reference image (0-1)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return parser.parse_args()


def load_pipeline(model_name: str) -> StableDiffusionImg2ImgPipeline:
    """Load Stable Diffusion Img2Img pipeline with a memory-efficient scheduler."""
    token = os.environ.get("HUGGINGFACE_TOKEN")
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        use_auth_token=token,
    )
    # Use a fast & memory-efficient scheduler
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    return pipe


def generate_for_animal(
    pipe: StableDiffusionImg2ImgPipeline,
    reference: Image.Image,
    animal: str,
    num_steps: int,
    scale: float,
    strength: float,
    seed: int | None = None,
) -> Image.Image:
    """Run img2img for a single animal prompt and return the generated image."""
    prompt = f"a high-resolution photo of a {animal}, ultra realistic, same pose and composition as the reference image"
    negative_prompt = (
        "blurry, lowres, distorted, watermark, text, bad anatomy, bad hands, deformed, disfigured, "
        "poorly drawn, cropped"
    )

    generator = torch.Generator(device=pipe.device).manual_seed(seed) if seed is not None else None

    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=reference,
        strength=strength,
        guidance_scale=scale,
        num_inference_steps=num_steps,
        generator=generator,
    ).images[0]
    return image


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

def main() -> None:
    args = parse_arguments()

    # Prepare output directory
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load reference image
    reference = Image.open(args.image_path).convert("RGB")

    # Load model
    pipe = load_pipeline(args.model_name)

    animals: List[str] = [a.strip() for a in args.animals.split(",") if a.strip()]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for animal in animals:
        print(f"\nGenerating {animal} ...")
        gen_image = generate_for_animal(
            pipe,
            reference,
            animal,
            num_steps=args.num_inference_steps,
            scale=args.guidance_scale,
            strength=args.strength,
            seed=args.seed,
        )
        filename = out_dir / f"{timestamp}_{animal}.png"
        gen_image.save(filename)
        print(f"Saved {filename}")

    print("\nGeneration complete ✨")


if __name__ == "__main__":
    main()