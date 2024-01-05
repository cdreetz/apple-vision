```
mkdir /mnt/models
pip install huggingface-hub[cli]
huggingface-cli download turboderp/Mixtral-8x7B-instruct-exl2 --revision 3.0bpw --local-dir-use-symlinks False --local-dir /mnt/models

git clone https://github.com/cdreetz/apple-vision
cd apple-vision/extract
pip install exllamav2

python mixtral_extract.py
```
