from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch
import pdb
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8")
exe_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8").to(device)
ins_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8").to(device) 
def model_mentor(model, history):
    # prompt = "告诉我今天上海的天气如何."
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
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.bfloat16().generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def model_chat(model, prompt, input_text):
    # prompt = "告诉我今天上海的天气如何."
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Based on the input text and key messages in your head about previous dialog, \
                                you need to provide a response."},
            {"role": "system", "content": "history theme, key words and key phrases are {}".format(prompt)}
        {"role": "user", "content": input_text}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.bfloat16().generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

prompt = "你今天心情怎么样？"
response = model_chat(exe_model, prompt)
print("Chat said: ", response)
history = {
    'role': "use", "content": prompt,
    'role': "executive model", "contenct": response}
mentor_response = model_mentor(ins_model, str(history))
print("Mentor thought: ,", mentor_response)
pdb.set_trace()
