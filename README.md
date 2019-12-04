# Ainize-run-style-transfer

[![Run on Ainize](https://ainize.ai/static/images/run_on_ainize_button.png)](https://ainize.web.app/redirect?git_repo=github.com/ainize-team/ainize-run-style-transfer)

## Docker build
```
docker build -t style-transfer .
```

## Docker run
```
docker run -t style-transfer
```


## How to request using https
```
http://${host}:80/transfer?base=${baseImageId}&style=${styleImageId}
```
You have to pass id for base and style image.

### upload image to google drive 

For convience, we open public [google drive](https://drive.google.com/drive/folders/1Ou30F1YEa0Wnh6V1gPjSwmxNmobqe_X2) for upload images. 

You can get image id from shareable link.  
<img src="/images/guide.png" width="250" />
<img src="/images/guide2.png" width="250" />

## References
1. [Neural style transfer](https://www.tensorflow.org/tutorials/generative/style_transfer)
