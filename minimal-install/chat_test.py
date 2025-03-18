import requests
import json

def chat_test(message, tp_url, llm_service_name, api_prefix="/api/v1/ticketpilot"):
    messages = [
        {"role": "system",
         "content": [
             {"type": "text", "text": "You are a helpful assistant."}
         ]
         },
        {"role": "user",
         "content": [
             {"type": "text", "text": message}
         ]
         },
    ]
    chat_object = {
        "messages": messages,
        "max_tokens": 1000
    }
    chat_request = {
        "service_name": llm_service_name,
        "chat_obj": chat_object
    }
    response = requests.post(tp_url+api_prefix+"/chat", data=json.dumps(chat_request))
    print(response.text)

if __name__ == '__main__':
    chat_test(message = "Please give me a cupcake recipe in markdown format",
              tp_url = "http://0.0.0.0:8012",
              llm_service_name = "gpt-35-tb")