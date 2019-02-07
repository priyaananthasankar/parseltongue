import logging
import os
import pandas
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService

blob_account_name = os.getenv("BlobAccountName")
blob_account_key = os.getenv("BlobAccountKey")
block_blob_service = BlockBlobService(account_name=blob_account_name,
                                      account_key=blob_account_key)
out_blob_container_name = os.getenv("OutBlobContainerName")

# Clean blob flow from event grid events
def clean(req_body):
    blob_obj,filename = extract_blob_props(req_body[0]['data']['url']  )
    result = clean_blob(blob_obj.content,filename)
    return result

# Extract blob container name and blob file
def extract_blob_props(url):
    blob_file_name = url.rsplit('/',1)[-1]
    in_container_name = url.rsplit('/',2)[-2]
    readblob = block_blob_service.get_blob_to_text(in_container_name, 
                                                   blob_file_name)
    return readblob,blob_file_name.rsplit('.',1)[-2]

# process blob, clean, preprocess etc
def clean_blob(content,blob_file_name):
    logging.info(content)
    
    # TODO Clean blob data logic here
    block_blob_service.create_blob_from_text(out_blob_container_name, blob_file_name + "_clean.txt" , "Clean data")
    return "Success"