from azure.storage.blob import BlobServiceClient, BlobBlock
import uuid
from responses_colection.response_json import response_json

AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=azureyellowcab;AccountKey=tlRAtEUmclKrQPupGAnwlo6GyivJyVLI2DzsAlsDxCYbGx1896Jhsr6MOHShABk+ukTMsLSnUclt+AStgk6vww==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_blob(filename: str, file):
    container = "cabfiles"
    try:
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        # Upload data by chunks
        block_list=[]
        chunk_size=1024*1024*30
        with file.file as f:
            while True:
                read_data = f.read(chunk_size)
                if not read_data:
                    break
                blk_id = str(uuid.uuid4())
                blob_client.stage_block(block_id=blk_id,data=read_data) 
                block_list.append(BlobBlock(block_id=blk_id))
        blob_client.commit_block_list(block_list)
        return response_json(message = "success")
    except Exception as e:
        return response_json(message = e, status = 500)