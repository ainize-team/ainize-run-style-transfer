# Ainize-run-style-transfer

[![Run on Ainize](https://ainize.ai/static/images/run_on_ainize_button.svg)](https://www.ainize.ai/vyvydkf628/style-transfer-gpu)

## Docker build
```
docker build -t style-transfer .
```

## Docker run
```
docker run -t style-transfer
```


## How to request using cURL

First of all, you should download [sample-base-image.jpg](https://github.com/ainize-team/ainize-run-style-transfer/blob/master/images/sample-base-image.jpg) and [sample-style-image.jpg](https://github.com/ainize-team/ainize-run-style-transfer/blob/master/images/sample-style-image.jpg).

1. Try on ainized [sample service](https://www.ainize.ai/vyvydkf628/style-transfer-gpu)
```
curl -X POST "https://style-transfer-gpu.vyvydkf628.endpoint.ainize.ai/transfer" -H "accept: images/*" -H "Content-Type: multipart/form-data" -F "base_image=@sample-base-image.jpg;type=image/jpeg" -F "style_image=@sample-style-image.jpg;type=image/jpeg" -o result.jpg
```

2. Try on your localhost
```
curl -X POST "http://localhost:80/transfer" -H "accept: images/*" -H "Content-Type: multipart/form-data" -F "base_image=@sample-base-image.jpg;type=image/jpeg" -F "style_image=@sample-style-image.jpg;type=image/jpeg" -o localhost-result.jpg
```

## References
1. [Neural style transfer](https://www.tensorflow.org/tutorials/generative/style_transfer)
