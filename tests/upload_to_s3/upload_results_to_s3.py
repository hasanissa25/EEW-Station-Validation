from pathlib import Path
import os
import glob
import boto3


def upload_results_to_s3(path_of_folder_to_upload, bucketName, s3directory):
    '''
    Arguments:

    path_of_folder_to_upload: The path to the directory to upload to S3
    bucketName: To which bucket to upload in S3
    s3directory: Which 'directory' in S3 to save to


    Output:

    Uploads the required folder to S3 bucket
    '''

    s3 = boto3.resource('s3')
    cwd = str(Path.cwd())
    # Join the current directory to the folder you want to upload
    p = Path(os.path.join(Path.cwd(), path_of_folder_to_upload))
    # Get the nested folders inside the directory we are looking to upload
    mydirs = list(p.glob('**'))
    for mydir in mydirs:
        # Get all the file names inside the directory we are looking to upload
        fileNames = glob.glob(os.path.join(mydir, "*"))
        fileNames = [f for f in fileNames if not Path(f).is_dir()]

        for fileName in fileNames:
            fileName = str(fileName).replace(cwd, '')
            # only modify the text if it starts with the prefix
            if fileName.startswith('/'):
                # remove one instance of prefix
                fileName = fileName.replace('/', "", 1)
            print(f"Uploading to S3: {fileName}")
            s3path = os.path.join(s3directory, str(fileName))
            s3.meta.client.upload_file(fileName, bucketName, s3path)


upload_results_to_s3(path_of_folder_to_upload="./station_validation_results",
                     bucketName="eew-validation-data",
                     s3directory="validation_results")
