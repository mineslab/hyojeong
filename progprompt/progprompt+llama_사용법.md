## progprompt 사이트
https://progprompt.github.io/
## progprompt 깃허브
https://github.com/NVlabs/progprompt-vh

<b>깃클론 방법</b> <br>
git clone https://github.com/NVlabs/progprompt-vh.git
<br><br>

## llama 허깅페이스 모델 다운로드 방법
허깅페이스에서 access_token을 이용해 원하는 모델의 token을 받는다<br>
https://huggingface.co/meta-llama/Llama-2-7b-hf
<br>나는 이 모델을 사용했다
<br><br>
git clone https://huggingface.co/meta-llama/Llama-2-7b-hf /home/seojin/Desktop/kwon/llama-2-7b-hf-model
<br>위 코드를 이용해 컴퓨터에 허깅페이스 'llama-2-7b-hf-model'을 다운로드 받는다
<br> ('/home/seojin/Desktop/kwon/llama-2-7b-hf-model' 부분은 내가 다운로드 받을 경로이다. 본인의 경로에 맞춰서 수정하기)
<br>이 때 패스워드를 입력하라고 나오는데, 발급받은 token을 입력하면 된다

<br> <b>이 과정을 마치면, progprompt와 llama를 이용해서 프롬프트를 생성할 수 있다.</b> <br>
<b>progprompt_final.py의 코드를 바탕으로 본인의 컴퓨터 환경에 맞춰 수정해가며 실행해볼 수 있다.</b>
