from azure.storage.blob import BlobServiceClient


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
