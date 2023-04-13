from os.path import basename
import boto3 
import imageio
import io
import json
import logging
import os
import uuid


# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
COLLECTION_ID = os.getenv("COLLECTION_ID")

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')
except Exception as e:
    logging.error(e, exc_info=True)
    raise e

def _get_s3_video(bucket, key):
    """Return the video found in the bucket
    """
    filename = '/tmp/' + str(uuid.uuid4())
    logger.debug("Downloading s3://%s/%s ...", bucket, key, filename)
    with open(filename, 'wb') as fh:
        s3.download_fileobj(bucket, key, fh)
    video = imageio.get_reader(filename, 'ffmpeg')
    return video

def _get_face_image(video, fps, timestamp, top, left, width, height):
    """Return the bytes corresponding to the given bounding box in the image
    """
    frame_index = int(fps * timestamp / 1000)
    frame = video.get_data(frame_index)
    (image_height, image_width, _) = frame.shape
    y1 = int(image_height * top)
    y2 = int(image_height * (top + height))
    x1 = int(image_width * left)
    x2 = int(image_width * (left + width))
    face_image = frame[y1:y2, x1:x2]
    return face_image

def _as_png_bytes(face_image):
    fn = "/tmp/" + str(uuid.uuid4())
    imageio.imwrite(fn, face_image, format='png')
    try:
        with open(fn, 'rb') as fh:
            return fh.read()
    finally:
        os.remove(fn) 

def _is_new_face_image(already_matched_face_images, face_image):
    """Return wether the face is new or not
    """
    for already_matched_face_image in already_matched_face_images:
        # we only have one face in the source image as the traget image.
        # Therefore we can simply check if the FaceMatches contains something.
        response = rekognition.compare_faces(
            SourceImage={ 'Bytes': _as_png_bytes(already_matched_face_image) }, 
            TargetImage={ 'Bytes': _as_png_bytes(face_image) }
        )
        if len(response["FaceMatches"]) > 0:
            return False
    return True

def add_new_faces(video, faces):
    logger.debug("Video: %s", video.get_meta_data())
    fps = video.get_meta_data()['fps']
    already_matched_face_images = [] # Should I get it from the collection?
    for face in faces:
        # I extract the face from the image using the bounding box
        timestamp = face["Timestamp"]
        bb = face["Face"]["BoundingBox"]
        face_image = _get_face_image(video, fps, timestamp, bb["Top"], bb["Left"], bb["Width"], bb["Height"])
        # Then I compare each new face to the already added faces
        if _is_new_face_image(already_matched_face_images, face_image):
            # Let's add it to the list of already matched face 
            already_matched_face_images.append(face_image)
            # And to the collection
            rekognition.index_faces(
                CollectionId=COLLECTION_ID,
                Image={ 'Bytes': _as_png_bytes(face_image) },
                DetectionAttributes=['DEFAULT'],
                QualityFilter='AUTO'
            )

def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        job_id = message["JobId"]
        status = message["Status"]
        bucket = message["Video"]["S3Bucket"]
        key = message["Video"]["S3ObjectName"]
        if status == 'SUCCEEDED':
            logger.debug("Face detection #%s has %s (s3://%s/%s)", job_id, status, bucket, key)
            video = _get_s3_video(bucket, key)
            next_token = None
            response = rekognition.get_face_detection(JobId=job_id)
            add_new_faces(video, response["Faces"])
        else:
            logger.error("Face detection #%s has %s (s3://%s/%s)", job_id, status, bucket, key)
