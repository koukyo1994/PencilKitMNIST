import argparse

import cv2
import keras as ks
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", default="artifacts/mnist.h5")
    parser.add_argument("--image", required=True)

    args = parser.parse_args()

    model = ks.models.load_model(args.artifact)

    img = cv2.imread(args.image)
    img = img.reshape(1, 28, 28, 1).astype(np.float32)
    img /= 255

    import pdb
    pdb.set_trace()

    output = model.predict(img)
