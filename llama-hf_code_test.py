from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Hugging Face 토큰 설정
os.environ["HF_TOKEN"] = "my_token"

# 모델 및 토크나이저 경로
model_name = "meta-llama/Llama-2-7b-hf"

# 토크나이저와 모델 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.environ["HF_TOKEN"])
model = AutoModelForCausalLM.from_pretrained(model_name, token=os.environ["HF_TOKEN"])

# 한국어 문장 생성 테스트
input_text = "한국어 문장을 생성해보세요."
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs["input_ids"], max_length=50)

# 결과 출력
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
