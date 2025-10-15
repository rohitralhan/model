import argparse
from huggingface_hub import snapshot_download
import os

def download_huggingface_model(model_name, download_dir, token=None):
    """
    Downloads a model from the Hugging Face Hub to a specified local directory.

    Args:
        model_name (str): The repository ID of the model on Hugging Face (e.g., "openai/whisper-tiny").
        download_dir (str): The local directory path where the model should be downloaded.
        token (str, optional): Hugging Face access token for gated/private models.
    """
    try:
        # Create the download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        print(f"Attempting to download model '{model_name}' to '{download_dir}'...")

        # Download the entire repository (model)
        local_path = snapshot_download(repo_id=model_name, local_dir=download_dir,token=token,
            resume_download=True)

        print(f"Model '{model_name}' successfully downloaded to: {local_path}")
    except Exception as e:
        print(f"Error downloading model '{model_name}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a model from Hugging Face Hub.")
    parser.add_argument("--model_name", type=str, required=True,
                        help="The repository ID of the model on Hugging Face (e.g., 'openai/whisper-tiny').")
    parser.add_argument("--download_dir", type=str, required=True,
                        help="The local directory path where the model should be downloaded.")

    args = parser.parse_args()

    download_huggingface_model(args.model_name, args.download_dir,"")
