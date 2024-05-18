import base64
import json
import os
import time
import urllib.parse
from io import BytesIO

import boto3
import ffmpeg
import streamlit as st
from PIL import Image
from botocore.exceptions import ClientError


# Author: Gary A. Stafford
# Purpose: Call an Amazon SageMaker Asynchronous Inference endpoint to generate a short video from image using SVD-XT 1.1 image-to-video model
# Date: 2024-05-13
# License: MIT License

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# AWS Configuration - *** CHANGE ME! ***
S3_BUCKET = "sagemaker-us-east-1-676164205626"
ENDPOINT_NAME = "huggingface-pytorch-inference-2024-05-09-01-03-47-190"

s3_client = boto3.client("s3")

# Local File Paths
REQUEST_PAYLOAD = "request_payloads/payload.json"
RESPONSE_PAYLOAD = "response_payloads/output.json"


def main():
    configure_page()
    reset_session_states()
    handle_file_upload()
    display_input_fields()
    handle_video_creation()


def configure_page():
    st.set_page_config(page_title="Generative Video Creation")

    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap');
        html, body, p, li, a, h1, h2, h3, h4, h5, h6, table, td, th, div, form, input, button, textarea, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown("# Generative Video Creation")
    st.markdown("### Stable Video Diffusion XT 1.1 Image-to-Video Generation")
    st.markdown("---")


def reset_session_states():
    session_state_defaults = {
        "play_video_disabled": True,
        "invocation_time": 0,
        "movie_title": None,
        "width": 1024,
        "height": 576,
        "num_frames": 25,
        "num_inference_steps": 25,
        "min_guidance_scale": 1.0,
        "max_guidance_scale": 3.0,
        "fps": 6,
        "motion_bucket_id": 127,
        "noise_aug_strength": 0.02,
        "decode_chunk_size": 8,
        "seed": 42,
        "uploaded_image": None,
    }
    for key, value in session_state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def handle_file_upload():
    uploaded_file = st.file_uploader(
        "Upload a Conditioning Image", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(
                "The uploaded file is too large. Please upload an image smaller than 5MB."
            )
        else:
            st.session_state["uploaded_image"] = uploaded_file
            st.session_state["movie_title"] = os.path.splitext(uploaded_file.name)[0]
            image = Image.open(uploaded_file)
            st.session_state["width"], st.session_state["height"] = image.size
            display_image(image)


def display_image(image):
    st.write("Conditioning Image :camera:")
    st.image(image, width=400)


def display_input_fields():
    st.session_state["movie_title"] = st.text_input(
        "Movie Title", value=st.session_state.get("movie_title", "")
    )
    st.session_state["width"] = st.number_input(
        "Width", value=st.session_state["width"]
    )
    st.session_state["height"] = st.number_input(
        "Height", value=st.session_state["height"]
    )
    st.session_state["num_frames"] = st.number_input(
        "Number of Frames", value=st.session_state["num_frames"]
    )
    st.session_state["num_inference_steps"] = st.number_input(
        "Number of Inference Steps", value=st.session_state["num_inference_steps"]
    )
    st.session_state["min_guidance_scale"] = st.number_input(
        "Minimum Guidance Scale", value=st.session_state["min_guidance_scale"]
    )
    st.session_state["max_guidance_scale"] = st.number_input(
        "Maximum Guidance Scale", value=st.session_state["max_guidance_scale"]
    )
    st.session_state["fps"] = st.number_input(
        "Frames per Second", value=st.session_state["fps"]
    )
    st.session_state["motion_bucket_id"] = st.number_input(
        "Motion Bucket ID", value=st.session_state["motion_bucket_id"]
    )
    st.session_state["noise_aug_strength"] = st.number_input(
        "Noise Augmentation Strength", value=st.session_state["noise_aug_strength"]
    )
    st.session_state["decode_chunk_size"] = st.number_input(
        "Decode Chunk Size", value=st.session_state["decode_chunk_size"]
    )
    st.session_state["seed"] = st.number_input("Seed", value=st.session_state["seed"])


def handle_video_creation():
    create_video = st.button("Create Video")
    if create_video:
        with st.spinner("Creating video..."):
            # try:
            response_location = invoke_model()
            if response_location:
                if get_model_response(response_location):
                    process_video_frames()
                    video_path = f"video_out/{st.session_state['movie_title']}.mp4"
                    convert_frames_to_video(video_path)
                    st.success(f"Video created: {video_path}")
            # except Exception as e:
            #     st.error(f"An error occurred: {e}")
    play_video(f"video_out/{st.session_state['movie_title']}.mp4")


def upload_file(file_path):
    s3_client.upload_file(
        Filename=file_path,
        Bucket=S3_BUCKET,
        Key="async_inference/input/payload.json",
        ExtraArgs={"ContentType": "application/json"},
    )


def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def invoke_model():
    image = Image.open(st.session_state["uploaded_image"])
    data = {
        "image": encode_image(image),
        "width": st.session_state["width"],
        "height": st.session_state["height"],
        "num_frames": st.session_state["num_frames"],
        "num_inference_steps": st.session_state["num_inference_steps"],
        "min_guidance_scale": st.session_state["min_guidance_scale"],
        "max_guidance_scale": st.session_state["max_guidance_scale"],
        "fps": st.session_state["fps"],
        "motion_bucket_id": st.session_state["motion_bucket_id"],
        "noise_aug_strength": st.session_state["noise_aug_strength"],
        "decode_chunk_size": st.session_state["decode_chunk_size"],
        "seed": st.session_state["seed"],
    }

    with open(REQUEST_PAYLOAD, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    upload_file(REQUEST_PAYLOAD)

    sm_runtime_client = boto3.client("sagemaker-runtime")
    response = sm_runtime_client.invoke_endpoint_async(
        EndpointName=ENDPOINT_NAME,
        InputLocation=f"s3://{S3_BUCKET}/async_inference/input/payload.json",
        InvocationTimeoutSeconds=3600,
    )

    return response.get("OutputLocation")


def get_model_response(response_location):
    output_url = urllib.parse.urlparse(response_location)
    bucket = output_url.netloc
    key = output_url.path[1:]
    while True:
        try:
            s3_client.head_object(Bucket=bucket, Key=key)
            s3_client.download_file(Bucket=bucket, Key=key, Filename=RESPONSE_PAYLOAD)
            print("Model response successfully received.")
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey" or e.response["Error"]["Code"] == "404":
                print("Waiting for model output...")
                time.sleep(15)
                continue
            raise


def process_video_frames():
    with open(RESPONSE_PAYLOAD, "r") as f:
        data = json.load(f)
    for idx, video_frame in enumerate(data["frames"]):
        frame_name = f"frames_out/frame_{idx+1:02}.jpg"
        with open(frame_name, "wb") as fh:
            fh.write(base64.b64decode(video_frame))


def convert_frames_to_video(video_path):
    output_options = {
        "crf": 20,
        "preset": "slower",
        "movflags": "faststart",
        "pix_fmt": "yuv420p",
        "vcodec": "libx264",
    }
    ffmpeg.input(
        "frames_out/*.jpg", pattern_type="glob", framerate=st.session_state["fps"]
    ).output(video_path, **output_options).run(overwrite_output=True, quiet=True)


def play_video(video_path):
    st.session_state["play_video_disabled"] = False
    if st.button("Play Video", disabled=st.session_state["play_video_disabled"]):
        try:
            with open(video_path, "rb") as video_file:
                st.video(
                    video_file.read(), format="video/mp4", loop=True, autoplay=True
                )
        except FileNotFoundError:
            st.warning("Video does not exist. Please create the video first.")


if __name__ == "__main__":
    main()
