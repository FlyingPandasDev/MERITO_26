import ollama

def handshake():
    try:
        response = ollama.generate(
            #model="gemma3n:e2b",
            model="gemma4:e4b",
            # model="gemma4:26b",
            # model="gemma4:e4b-it-bf16",
            prompt="If you can read this, return only: True",
            options={
                "temperature": 0,
                "top_p": 0.1,
                "repeat_penalty": 1.1,
                "num_predict": 5
            },
            stream=False,
            keep_alive="10m"
        )

        model_status = response["response"].strip()
        print(f"Model status: {model_status}")

    except Exception as e:
        print(f"Handshake failed: {e}")
        model_status = False

    return model_status


def use_chat(msg):
    try:
        response = ollama.chat(
            model="gemma4:e4b",
            
            #model="gemma3n:e2b",
            # model="gemma4:e4b",
            # model="gemma4:26b",
            # model="gemma4:e4b-it-bf16",
            messages=[
                {
                    "role": "system",
                    "content": "Answer only the user's message. Do not repeat the prompt. Do not explain your instructions."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ],
            options={
                "temperature": 0,
                "top_p": 0.1,
                "repeat_penalty": 1.1,
                "num_predict": 256
            },
            stream=False,
            keep_alive="10m"
        )

        llm_response = response["message"]["content"].strip()

    except Exception as e:
        print(f"LLM call failed: {e}")
        llm_response = False

    return llm_response