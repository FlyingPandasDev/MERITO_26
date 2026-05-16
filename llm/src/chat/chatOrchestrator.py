from src.chat.userValidation import validateUser
from src.connectors.llm_connector import handshake, use_chat
from src.config.llmConfig import additionalContext
from src.microservices.microServiceManager import microManager
import datetime, json


def start_user_session(user_id):
    allowed = validateUser(user_id)
    model_status = False

    if allowed:
        model_status = handshake()

    return allowed, model_status
            

def handle_user_message(user_msg: str, header: str, logger=None) -> str:
    logger = logger or (lambda *_: None)
    logger("Validating message")
    logger("Calling LLM")

    llm_message, user_backend_message, microservice_llm_message, hasFile = chat_loop(
        user_msg,
        header,
        allow_microservice=True
    )

    return llm_message, user_backend_message, microservice_llm_message, hasFile
    

def handle_backend_message(backend_msg: str, header: str, logger=None) -> str:
    print("running attachment logic")
    logger = logger or (lambda *_: None)

    llm_message, user_backend_message, microservice_llm_message, hasFile = chat_loop(
        backend_msg,
        header,
        allow_microservice=False
    )

    return llm_message
    

def chat_loop(user_msg, header, allow_microservice=True):
    route, llm_message, user_backend_message, microservice_llm_message, hasFile = chat_flow(
        user_msg,
        header,
        allow_microservice=allow_microservice
    )
    
    return llm_message, user_backend_message, microservice_llm_message, hasFile


def chat_flow(msg, header, allow_microservice=True):
    
    additional_context = additionalContext()
    contexted_msg = str(additional_context) + msg    

    raw_llm_responce = use_chat(contexted_msg)

    try:
        llm_response = clean_llm_json(raw_llm_responce)
    except (ValueError, json.JSONDecodeError, TypeError) as parse_error:
        print(f"LLM JSON parse failed, using conversation fallback: {parse_error}")
        llm_response = {
            "header": {
                "routing": "conversation",
                "microservice": "",
            },
            "llmMsg": "Wystapil problem techniczny po mojej stronie. Sprobuj prosze ponownie.",
            "conv_summary": ""
        }

    print(llm_response)

    header_obj = llm_response.get("header", {})
    route = header_obj.get("routing", "conversation")
    microservice_route = header_obj.get("microservice", "")
    llm_message = llm_response.get("llmMsg", "")

    if not isinstance(route, str) or not route:
        route = "conversation"
    if not isinstance(microservice_route, str):
        microservice_route = ""
    if not isinstance(llm_message, str) or not llm_message.strip():
        llm_message = "Napisz prosze jeszcze raz, a postaram sie pomoc."
    
    user_backend_message = ""
    microservice_llm_message = ""

    print(f"running chat flow with route {route}")
    
    if route == "conversation": 
        pass

    elif route == "endConnection":
        route = "end"

    elif route == "microservice" and allow_microservice:
        print("running microservice")
        user_backend_message, backend_llm_message, userId = microManager(microservice_route)
        microservice_llm_message = handle_backend_message(backend_llm_message, header)

    elif route == "microservice" and not allow_microservice:
        print("microservice routing blocked for backend message")
        route = "conversation"

    if microservice_llm_message == "":
        has_file = False
    else:
        has_file = True

    return route, llm_message, user_backend_message, microservice_llm_message, has_file
    

def clean_llm_json(raw_response):
    if raw_response is None:
        raise ValueError("LLM response is None. Cannot parse JSON.")

    if not isinstance(raw_response, str):
        raise TypeError(f"LLM response must be a string, got: {type(raw_response).__name__}")

    cleaned = raw_response.strip()

    if not cleaned:
        raise ValueError("LLM response is empty. Cannot parse JSON.")

    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    if not cleaned:
        raise ValueError("LLM response became empty after cleaning. Cannot parse JSON.")

    try:
        json_cleaned = json.loads(cleaned)
        return json_cleaned

    except json.JSONDecodeError as e:
        print("Invalid JSON returned by LLM:")
        print(repr(cleaned))
        raise e