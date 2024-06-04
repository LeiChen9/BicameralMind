 from modelscope import AutoModelForCausalLM, AutoTokenizer
  2 import torch
  3 import pdb
  4 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  5 print(f"Using device: {device}")
  6 
  7 tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8")
  8 exe_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8").to(device)
  9 ins_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-4B-Chat-GPTQ-Int8").to(device)
 10 
 11 def model_mentor(model, history):
 12     # prompt = "告诉我今天上海的天气如何."
        prompt = "Please respond only in the Chinese language. Do not explain what you are doing. \
                  Do not self reference. You are an expert text analyst. \
                  Please summary the theme of the dialog and extract only the most relevant keywords \
                  and key phrases from a piece of text. Please showcase the results in 3 list: \
                  theme, keywords, key phrases. Please analyze the following text: "
 13     messages = [
 14         {"role": "system", "content": "You are a mentor of executive model. Your job is extracting, organizing, analyzing and summarizing the history information, and distill important information for executive model\
 15                                         and make him works better."},
 16         {"role": "user", "content": prompt + history}
 17     ]
 18     text = tokenizer.apply_chat_template(
 19         messages,
 20         tokenize=False,
 21         add_generation_prompt=True
 22     )
 23     model_inputs = tokenizer([text], return_tensors="pt").to(device)
 24 
 25     generated_ids = model.bfloat16().generate(
 26         model_inputs.input_ids,
 27         max_new_tokens=512
 28     )
 29     generated_ids = [
 30         output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
 31     ]
 32 
 33     response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
 34     return response
 35 
 36 def model_chat(model, prompt, input_text):
 37     # prompt = "告诉我今天上海的天气如何."
 38     messages = [
 39         {"role": "system", "content": "You are a helpful assistant. Based on the input text and key messages in your head about previous dialog, \
                                you need to provide a response."},
            {"role": "system", "content": "history theme, key words and key phrases are {}".format(prompt)}
 40         {"role": "user", "content": input_text}
 41     ]
 42     text = tokenizer.apply_chat_template(
 43         messages,
 44         tokenize=False,
 45         add_generation_prompt=True
 46     )
 47     model_inputs = tokenizer([text], return_tensors="pt").to(device)
 48 
 49     generated_ids = model.bfloat16().generate(
 50         model_inputs.input_ids,
 51         max_new_tokens=512
 52     )
 53     generated_ids = [
 54         output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
 55     ]
 56 
 57     response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
 58     return response
 59 
 60 prompt = "你今天心情怎么样？"
 61 response = model_chat(exe_model, prompt)
 62 print("Chat said: ", response)
 63 history = {
 64     'role': "use", "content": prompt,
 65     'role': "executive model", "contenct": response}
 66 mentor_response = model_mentor(ins_model, str(history))
 67 print("Mentor thought: ,", mentor_response)
 68 pdb.set_trace()
