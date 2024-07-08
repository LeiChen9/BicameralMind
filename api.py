from http import HTTPStatus
import dashscope
import pdb
import copy
def call_with_messages(role, input_text="", mentor_ideas="", history=""):
    assert role in ["chatbot", "mentor"]
    if role == "chatbot":
        messages = [
        {"role": "system", "content": "You are a helpful assistant. Based on the input text and key messages in your head about previous dialog, \
                                you need to provide a response."},
        {"role": "system", "content": "history theme, key words and key phrases are: " + mentor_ideas},
        {"role": "user", "content": input_text}
        ]
    else:
        prompt = "Please respond only in the Chinese language. Do not explain what you are doing. \
                Do not self reference. You are an expert text analyst. \
                Please summary the theme of the dialog and extract only the most relevant keywords \
                and key phrases from a piece of text. Please showcase the results in 3 list: \
                theme, keywords, key phrases. Please analyze the following text: "
        messages = [
            {"role": "system", "content": "You are a mentor of executive model. Your job is extracting, organizing, analyzing and summarizing the history information, and distill important information for executive model\
                                            and make him works better."},
            {"role": "user", "content": prompt + history}
        ]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    result = copy.deepcopy(response)
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    return result["output"]["choices"][0]["message"]["content"]

if __name__ == '__main__':
    input_text = "给我介绍一下GLy-P1这款药物"
    mentor_ideas = ""
    response = call_with_messages(role="chatbot", input_text=input_text)
    print("Chat said: ", response)
    history = {
        'role': "user", "content": input_text,
        'role': "executive model", "contenct": response}
    mentor_ideas = call_with_messages(role="mentor", history=str(history))
    print("Mentor thought: ,", mentor_ideas)