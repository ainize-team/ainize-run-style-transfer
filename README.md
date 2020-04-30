# Ainize-run-style-transfer

[![Run on Ainize](https://ainize.ai/static/images/run_on_ainize_button.svg)](https://ainize.ai/hyunhyerim/style-transfer)

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
```
https://style-transfer.hyunhyerim.endpoint.ainize.ai/transfer?base=1X9bbW6hT8kf8vyG-h8EAvdMEmluHfOtC&style=1q7Bj12gKP-GTve9GIBkdRdvUEwrpc4IP
```

You have to pass id for base and style image. This may take a few seconds (~30sec).

### upload image to google drive 

For convience, we open public [google drive](https://drive.google.com/drive/folders/1Ou30F1YEa0Wnh6V1gPjSwmxNmobqe_X2) for upload images. 

You can get image id from shareable link.  
<img src="/images/guide.png" width="250" />
<img src="/images/guide2.png" width="250" />

## References
1. [Neural style transfer](https://www.tensorflow.org/tutorials/generative/style_transfer)
