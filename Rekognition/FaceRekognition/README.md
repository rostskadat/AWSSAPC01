# Rekognition / FaceRekognition

Showcase the use of Rekognition to analyse videos in S3 and create a face collection

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
> C:\Tools\Python38\python.exe helpers\extract_image_from_mp4.py --debug --video resources\face-demographics-walking.mp4 --output resources\still.png --timestamp 2.5
DEBUG:root:Video: {'plugin': 'ffmpeg', 'nframes': inf, 'ffmpeg_version': '4.2.2 built with gcc 9.2.1 (GCC) 20200122', 'codec': 'h264', 'pix_fmt': 'yuv420p(tv', 'fps': 12.0, 'source_size': (768, 432), 'size': (768, 432), 'duration': 61.03}


C:\Tools\Python38\python.exe helpers\extract_image_from_mp4.py --debug --video resources\face-demographics-walking.mp4 --output resources\still.png --timestamp 2.5 --top  0.417 --left 0.698 --height 0.058 --width 0.02
Cutting 320 -> 364, 301 -> 310
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-FaceRekognition
```

## Details

*Author*: rostskadat
