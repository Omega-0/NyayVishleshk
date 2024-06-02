from bot_utility.main import get_page_wise_text_chunk
chunks = get_page_wise_text_chunk('referrence_docs\IPC.txt')
print(chunks[3])