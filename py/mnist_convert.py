import argparse

import coremltools

from pathlib import Path

OUTPUT_PATH = Path("../PencilKitMNIST/")
SCALE = 1 / 255.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", default="MNIST.mlmodel", help="Name of output CoreML model")
    parser.add_argument(
        "--artifact",
        required=True,
        help="h5 file to convert into CoreML model")

    args = parser.parse_args()

    output_name = OUTPUT_PATH / args.name

    mlmodel = coremltools.converters.keras.convert(
        args.artifact,
        input_names="image",
        image_input_names="image",
        output_names="output",
        image_scale=SCALE)
    mlmodel.author = "Hidehisa Arai"
    mlmodel.license = "MIT"
    mlmodel.short_description = "MNIST sample model"
    mlmodel.input_description[
        "image"] = "Grayscale image contains a handwitten digit"
    mlmodel.output_description["output"] = "Output a predicted digit class"
    mlmodel.save(str(output_name))
