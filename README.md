# Stable Video Diffusion XT 1.1 on Amazon SageMaker

Stability AI's [Stable Video Diffusion XT (SVT-XT) 1.1](https://medium.com/r/?url=https%3A%2F%2Fstability.ai%2Fstable-video) foundation model is a diffusion model that takes in a still image as a conditioning frame and generates a short 4 second video. The notebook walks through configuring, creating, and invoking an [Asynchronous Inference Endpoint](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html) backed by the SVT-XT foundation model on Amazon SageMaker.

## Architecture

![Architecture](architecture/async_inference.png)

## Wide-format Videos

All videos created using Notebook included in this project.

<table>
   <tr>
      <td><img src="video_samples/rocket_1.gif" alt="Rocket" width="615"/>
      </br><a href="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/svd/rocket.png">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/red_car_1.gif" alt="Red Sports Car" width="615"/>
      </br><a href="https://www.pexels.com/photo/red-alfa-romeo-c4-on-road-near-trees-210019">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/beach_bike_2.gif" alt="Motorcycle on Beach" width="615"/>
      </br><a href="https://www.pexels.com/photo/photo-of-man-riding-bicycle-4054069">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/koi_2.gif" alt="Koi" width="615"/>
      </br><a href="https://unsplash.com/photos/two-koi-fish-swimming-DpI3yVVeJyA">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/waterfall_2.gif" alt="Tropical Waterfall" width="615"/>
      </br><a href="https://www.pexels.com/photo/time-lapse-photography-of-waterfall-2406388">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/boat_ocean_1.gif" alt="Boat on Shore" width="615"/>
      </br><a href="https://www.pexels.com/photo/seinboat-sunrise-20544112">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/false_gods_1_pingpong.gif" alt="AI" width="615"/>
      </br>Source image generated with Stable Diffusion XL (SDXL) 1.0</a></td>
   </tr>
</table>

## Tall-format Videos

All videos created using Notebook included in this project.

<table>
   <tr>
      <td><img src="video_samples/coffee_1.gif" alt="Turkish Coffee" width="346"/>
      </br><a href="https://www.pexels.com/photo/a-shot-of-steaming-pot-with-a-and-glass-with-a-beverage-10351409">Source image</a></td>
      <td><img src="video_samples/champagne_2.gif" alt="Champagne" width="346"/>
      </br><a href="https://www.pexels.com/photo/close-up-of-beer-glass-against-black-background-255483">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/color_smoke_tall_1.gif" alt="Colored Smoke" width="346"/>
      </br><a href="https://www.pexels.com/photo/red-smoke-illustration-604671">Source image</a></td>
      <td><img src="video_samples/smoke_tall_1.gif" alt="Smoke" width="346"/>
      </br><a href="https://www.pexels.com/photo/close-up-of-beer-glass-against-black-background-255483">Source image</a></td>
   </tr>
</table>

## Optional: Local Environment

Setup local environment to modify `inference.py` file.

```sh
python3 -m pip install virtualenv -Uq
virtualenv svd-venv
python3 -m venv svd-venv

source svd-venv/bin/activate
```

```sh
python3 -m pip install -r requirements.txt -Uq
```

## References

- <https://github.com/aws-samples/amazon-sagemaker-asynchronous-inference-computer-vision/blob/main/mask-rcnn-async-inference.ipynb>
- <https://github.com/huggingface/diffusers/issues/6956>
- <https://github.com/huggingface/notebooks/blob/main/sagemaker/23_stable_diffusion_inference/sagemaker-notebook.ipynb>
- <https://github.com/philschmid/huggingface-inferentia2-samples/blob/main/stable-diffusion-xl/sagemaker-notebook.ipynb>
- <https://github.com/Stability-AI/generative-models/blob/main/scripts/sampling/simple_video_sample.py>
- <https://huggingface.co/docs/diffusers/en/using-diffusers/svd>
- <https://huggingface.co/docs/sagemaker/inference#create-a-model-artifact-for-deployment>
- <https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/tree/main>
- <https://sagemaker.readthedocs.io/en/stable/api/inference/async_inference.html>
- <https://www.philschmid.de/sagemaker-stable-diffusion>

---

_The contents of this repository represent my viewpoints and not of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners._
