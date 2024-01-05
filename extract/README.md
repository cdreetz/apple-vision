```
mkdir /mnt/models
pip install huggingface-hub[cli]
huggingface-cli download turboderp/Mixtral-8x7B-instruct-exl2 --revision 3.0bpw --local-dir-use-symlinks False --local-dir /mnt/models

git clone https://github.com/cdreetz/apple-vision
cd apple-vision/extract
pip install exllamav2

python mixtral_extract.py
```

version 1: instruction_ids = tokenizer.encode(f"[INST] {input_text} [/INST]", add_bos = True)
version 1: full_input = "Identify the key topics and concepts discussed on this page of the research paper: " + text

<b>version 2 didn't work because '+ text' was outside of the [/INST]</b>
version 2: instruction_ids = tokenizer.encode(f"{input_text}", add_bos = True)
version 2: full_input = "[INST] Carefully read the following text from a research paper page. Identify and list only the central concepts, theories, or ideas discussed, excluding any author names, affiliations, or other non-conceptual text. Focus on the academic content and key points that are essential to understanding the subject matter of this page.[/INST] " + text

version 3: instruction_ids = tokenizer.encode(f"{input_text}", add_bos = True)
version 3: full_input = "[INST] Carefully read the following text from a research paper page. Identify and list only the central concepts, theories, or ideas discussed, excluding any author names, affiliations, or other non-conceptual text. Focus on the academic content and key points that are essential to understanding the subject matter of this page.[/INST] Some of the key concepts discussed were: \n 1." + text
