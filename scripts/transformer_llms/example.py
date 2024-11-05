"""dummy"""

import torch
import transformers
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from torch import cuda


def test_rag():
    # print("cuda" if cuda.is_available() else "cpu")
    #
    # model_id = "meta-llama/Meta-Llama-3.1-8B"
    #
    # pipeline = transformers.pipeline(
    #     "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
    # )
    #
    # pipeline("Hey how are you doing today?")

    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
    retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
    model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

    input_dict = tokenizer.prepare_seq2seq_batch("who holds the record in 100m freestyle", return_tensors="pt")

    generated = model.generate(input_ids=input_dict["input_ids"])
    print(tokenizer.batch_decode(generated, skip_special_tokens=True)[0])

    # should give michael phelps => sounds reasonable


def main():
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )

    messages = [
        {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
        {"role": "user", "content": "Who are you?"},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )
    print(outputs[0]["generated_text"][-1])

    # pip install --upgrade transformers


if __name__ == '__main__':
    test_rag()

