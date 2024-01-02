

1. Parse PDFs into chunks by page. Write a JSON with the raw text as {chunk: "page1 text"}, {chunks: "page2 text"},....
2. Start 3090 VM, install exllamav2, download mixtral instruct 3.0bpw
3. Run mixtral_extract version 1, generate a output_v1.json with {chunk: "chunk", summary: "summary"}
4. Do for version 2 and version 3
5. Result should be 3 different json files of Mixtral outputs per chunk
6. Terminate VM, do the same generation with gpt-3.5
7. Compare