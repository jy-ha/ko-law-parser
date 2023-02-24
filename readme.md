# Korea Law Json Parser
한국 법령 Json 파싱 코드

## 사용방법
1. [법령정보센터](https://www.law.go.kr/%EB%B2%95%EB%A0%B9) 에서 원하는 법령을 열어서 텍스트로 저장합니다. ('조문목록 포함'을 체크하여야 함)

<img width="225" alt="image" src="https://user-images.githubusercontent.com/43233543/221195617-9f78a6f0-3612-4819-aa7b-9c24ae95fce6.png">

2. 텍스트만 복사해서 law 폴더에 저장합니다.
3. main.py 실행하면 다음과 같은 json 파일이 생성됩니다.

<img width="630" alt="image" src="https://user-images.githubusercontent.com/43233543/221196051-88cb44e6-eaec-430e-bcf7-9710262908b5.png">

## 기타사항

* 대한민국의 법령 [조문 체계](https://elaw.klri.re.kr/kor_service/lawsystem.do)를 따릅니다.
* 모든 법령 파싱에 검증되지 않아 일부 실패할 수 있습니다. 이슈 등록 부탁드립니다.
