import torch

from glados_tts_main.utils.text.cleaners import Cleaner
from glados_tts_main.utils.text.tokenizer import Tokenizer

def prepare_text(text: str)->str:
    if not ((text[-1] == '.') or (text[-1] == '?') or (text[-1] == '!')):
        text = text + '.'
    cleaner = Cleaner('english_cleaners', True, 'en-us')
    tokenizer = Tokenizer()
    return torch.as_tensor(tokenizer(cleaner(text)), dtype=torch.long, device='cpu').unsqueeze(0)
