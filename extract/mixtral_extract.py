from exllamav2 import *
from exllamav2.generator import *
import sys, torch, json

config = ExLlamaV2Config()
config.model_dir = "/mnt/models/"
config.prepare()

model = ExLlamaV2(config)
cache = ExLlamaV2Cache(model, lazy = True)

model.load_autosplit(cache)

tokenizer = ExLlamaV2Tokenizer(config)
generator = ExLlamaV2StreamingGenerator(model, cache, tokenizer)
generator.set_stop_conditions([tokenizer.eos_token_id])
gen_settings = ExLlamaV2Sampler.Settings()

def process_with_language_model(input_text):
    instruction_ids = tokenizer.encode(f"[INST] {input_text} [/INST]", add_bos = True)
    context_ids = instruction_ids if generator.sequence_ids is None \
        else torch.cat([generator.sequence_ids, instruction_ids], dim = -1)
    generator.begin_stream(context_ids, gen_settings)

    output_text = ""
    while True:
        chunk, eos, _ = generator.stream()
        if eos: break
        output_text += chunk
        sys.stdout.flush()

    return output_text.strip()

input_file_path = '/apple-vision/parsing/all_pages_text.json'  # Update this to your file path
with open(input_file_path, 'r') as file:
    document = json.load(file)

summaries = {}
for index, page_dict in enumerate(document):
    print(f"Processing page {index}...")
    text = page_dict['chunk']  # assuming each dictionary in the list has a 'chunk' key
    full_input = "Identify the key topics and concepts discussed on this page of the research paper: " + text
    summary = process_with_language_model(full_input)
    summaries[index] = {
        "chunk": text,
        "summary": summary
    }

output_file_path = 'output_v1.json'  # Update this to your desired output path
with open(output_file_path, 'w') as outfile:
    json.dump(summaries, outfile, indent=4)

print("Processing complete. Summaries saved to:", output_file_path)


## version 1: instruction_ids = tokenizer.encode(f"[INST] {input_text} [/INST]", add_bos = True)
## version 1: full_input = "Identify the key topics and concepts discussed on this page of the research paper: " + text

## version 2: instruction_ids = tokenizer.encode(f"{input_text}", add_bos = True)
## version 2: full_input = "[INST] Carefully read the following text from a research paper page. Identify and list only the central concepts, theories, or ideas discussed, excluding any author names, affiliations, or other non-conceptual text. Focus on the academic content and key points that are essential to understanding the subject matter of this page.[/INST] " + text

## version 3: instruction_ids = tokenizer.encode(f"{input_text}", add_bos = True)
## version 3: full_input = "[INST] Carefully read the following text from a research paper page. Identify and list only the central concepts, theories, or ideas discussed, excluding any author names, affiliations, or other non-conceptual text. Focus on the academic content and key points that are essential to understanding the subject matter of this page.[/INST] Some of the key concepts discussed were: \n 1." + text





