# hire-me-app

### Todos

- [x] 벡터스토어 검증
  - [x] ~~`fluffy-oreo`~~
  - [x] `crunchy-ball` ✅
- [ ] 챗봇 관련
  - [x] Azure 엔드포인트에 요청 보내는 로직
  - [ ] 시스템 프롬프트를 변경하는 로직
- [ ] 파일 관련
  - [ ] 파일 업로드 요청을 보내는 로직
  - [ ] 파일 삭제 요청을 보내는 로직
- [ ] 로그인 관련
  - [ ] 로그인 요청 보내는 로직
  - [ ] 로그인을 유지하는 로직
- [ ] Azure OpenAI -> Azuer AI Foundry

### memo

```
uv init -p 3.12.9
uv sync
uv add <dependency>

uv sync

uv export -o requirements.txt --no-hashes
```

### ✅ 확인사항: 챗봇 시스템 프롬프트 변경 로직

현재 챗봇 시스템 프롬프트를 변경하는 로직에 대한 구현 진행 중이며, 몇 가지 확인 사항과 구조에 대해 아래와 같이 정리됩니다.

#### 🛠️ 현재 상황

**도우미 ID(assistant_id)**는 아직 Azure OpenAI 포털 상에서 설정되지 않은 상태이며, 현재는 임의의 값을 코드에 넣어둔 상태입니다.

시스템 프롬프트를 변경하는 과정에서 사용자의 선택에 따라 알맞은 assistant가 매칭되도록 설계하고 있습니다.

#### 🔁 전체 로직 흐름

1. 프론트엔드에서 사용자 입력

   - 사용자가 챗봇 UI에서 특정 기능을 선택합니다.
   - 해당 기능에 대한 값은 get_response_from_assistant 함수 내에서 assistant_type으로 받습니다.

2. assistant_type을 기반으로 미리 정의된 딕셔너리(assistant_mapping)에서 아래 정보를 조회합니다.

   - assistant_id: 기능에 맞는 Assistant ID
   - thread_id: 해당 Assistant에 연결된 Thread ID
     - 이 thread_id 값은 DB에서 조회하여 가져오도록 설계되어 있습니다.

3. 조회된 정보로 응답 요청 처리

   - assistant_id와 thread_id를 바탕으로 사용자의 질문에 대해 응답을 생성합니다.

#### 📌 향후 처리할 일

- assistant_id의 실제 값을 확정 및 매핑 등록
- assistant_type → assistant_id/thread_id 매핑 딕셔너리 수정
  - 현재는 DB에서 활용했던 변수명을 활용하여 assistant_type으로 받아올 수 있는 변수 범위를 설정해두었습니다.
  - 프론트엔드 측에서 수정 요청 시 수정 가능.
- 프론트엔드에서 사용자의 기능 선택에 따른 assistant_type 인자를 받아서 로직에 전달
