import os
import logging
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)

class BlobManager:
    def __init__(self, container_name: str = "patient-reports"):
        self.container_name = container_name
        self.conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = None
        self.container_client = None

        if not self.conn_str:
            logger.warning("AZURE_STORAGE_CONNECTION_STRING not set. BlobManager will not function properly.")
        else:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
                self.container_client = self.blob_service_client.get_container_client(self.container_name)
                
                # Create container if it doesn't exist
                if not self.container_client.exists():
                    self.container_client.create_container()
                    logger.info(f"Created Azure Blob container: {self.container_name}")
            except Exception as e:
                logger.error(f"Failed to initialize BlobManager: {e}")

    def upload_report(self, filename: str, file_data: bytes) -> str:
        """Uploads a report to Azure Blob Storage."""
        if not self.container_client:
            raise RuntimeError("BlobManager is not initialized properly.")
            
        blob_client = self.container_client.get_blob_client(filename)
        blob_client.upload_blob(file_data, overwrite=True)
        return filename

    def download_report(self, filename: str) -> bytes:
        """Downloads a report from Azure Blob Storage."""
        if not self.container_client:
            raise RuntimeError("BlobManager is not initialized properly.")
            
        blob_client = self.container_client.get_blob_client(filename)
        return blob_client.download_blob().readall()
