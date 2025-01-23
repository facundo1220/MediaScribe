from azure.storage.blob import BlobServiceClient
import os
import re
from pathlib import Path


class Azure_Storage:
    def __init__(self, account_url, credential, container_name):
        try:
            self.blob_service_client = BlobServiceClient(
                account_url, credential=credential
            )

            self.container_name = container_name

        except Exception as e:
            print(f"Error init azure storage: {e}")

    def upload_file(self, blob, file_path):
        try:
            print(f"Uploading to Azure Storage as blob:{file_path}")

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob
            )

            with open(file_path, mode="rb") as data:
                blob_client.upload_blob(data, overwrite=True)

        except Exception as e:
            print(f"Error uploading file to azure storage: {e}")

    def ls_files(self, client, path="", recursive=True):
        if not path.endswith("/"):
            path += "/"

        blob_iter = client.list_blobs(name_starts_with=path)
        files = []

        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or not "/" in relative_path:
                files.append(blob.name)

        return files

    def create_images_file_content(self, image_files):
        lines = []
        pattern = re.compile(r"(SPEAKER_\d+)\.jpg")
        for image in image_files:
            path = Path(image)
            filename = path.name
            match = pattern.search(filename)
            if match:
                speaker = match.group(1)
                Image_text = f"Speaker: {speaker} - Image_path: {image}"
                lines.append(Image_text)
        result_string = "\n".join(lines)
        return result_string

    def get_image_url(self, path):
        client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        url = client.get_blob_client(path).url

        return url

    def get_folder_files(self, folder_name, index=False):
        try:

            client = self.blob_service_client.get_container_client(
                container=self.container_name
            )

            files = self.ls_files(client, path=folder_name)

            image_files = [file for file in files if file.endswith(".jpg")]
            text = client.download_blob(
                [file for file in files if file.endswith(".txt")][0]
            )

            azure_text_file = text.readall().decode("utf-8")

            # azure_image_text = self.create_images_file_content(image_files)

            if index:
                vector_store = ""
            else:
                vector_store = client.download_blob(
                    [file for file in files if file.endswith(".pkl")][0]
                )

            return (azure_text_file, image_files, vector_store)
        except Exception as e:
            print(f"Error in get folde files: {e}")
