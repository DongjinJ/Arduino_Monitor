# Arduino Monitor

---

[TOC]

---

## To Do

- [x] Timer 구현

- [x] Serial Connect 구현

- [x] Layout 구성

  Grid -> setGeometry

- [x] Protocol 정립

- [x] 데이터 별 Widget 연결

- [x] 데이터 Class 구축 필요

- [ ] 실제 Serial Data를 통해 Debugging 필요

  : 현재 Terminal input값으로는 테스트 잘됨

- [x] Gauge UI 적용

- [x] C/C++ Packet 라이브러리 구현

- [ ] Arduino Demo 테스트

---

## 2021-05-25

- 최초 업로드

---

## 2021-05-31

- QTimer를 이용해 주기적인 그래프 업데이트 기능 추가

- Connect 버튼을 추가하여 Timer 구동

- LCD 디스플레이 추가

- Widget에 Combo Box를 달아 Data 매칭 계획

---

## 2021-06-01

- Packet Module 작성

- Packet Module Test

  : Checksum Encode/Decode 확인

- Thread Test

  : Debug용 Thread 테스트

- 종료 Event 관련 정의 

  : 타 Thread 종료 시그널

---

## 2021-06-04

- ComboBox 데이터 연결 구축

  : ComboBox에서 선택한 데이터 ID를 실제 Data에 연결하여 Update

- x ms 주기로 현재 데이터 Update

- ComboBox Event 분리

---

## 2021-06-10

- Grid 배치에서 Pixel 좌표 배치로 변경

  : 크기 조절 및 배치 자유도때문에 변경

  : 적용 완료

- matplotlib의 plot 에서 Y축이 정렬되어 표시되지 않는 문제 발생

  -> str type이라 정렬 안됨. int형으로 변환 후 해결

- Gauge  그리는 함수 작업 착수

  : https://github.com/StefanHol/AnalogGaugeWidgetPyQt/blob/bb92101babda5c93337635d262cc2df3799c56f0/analoggaugewidget.py#L496

  참고


---

## 2021-06-15

- Gauge 작업 중

  : 직접 Polygon 원 위 좌표 구하는 방식으로 구현 예정

  : 눈금 작업 필요

  : 바늘 구현 vs 게이지 스펙트럼 

---

## 2021-06-16

- Gauge 작업중

  : 눈금 그림 범위 0 ~ 180

  : 눈금 값 Text 새겨넣음

  : 스펙트럼 입히기 완료

    -> 원리 이해는 안됨

  : 바늘까지 작업 완료했고 값에 따라 변동되도록 설정 완료

    -> 임시로 self.testValue에 묶어놨음

    -> 추후 ComboBox 만들어서 데이터에 묶는 작업 필요

- C언어 Packet Generator 작업

  : 함수 초안 작업 중

  : Python 에서 endian 확인 필요

---

## 2021-06-21

- Gauge 작업

  : ConicalGradient 이해 완료

  : Gauge 스펙트럼 수정

    -> 스펙트럼의 경우 중앙 점을 잡아줘야 중앙점 기준으로 그라데이션이 생김

    -> grad에 넣는 color는 0~1사이에 비율을 조절해주면 원하는만큼 영역 설정이 가능함

- monitor_Packet 관련 수정

  : Byte Order차이에 따른 수정

  : Decoding 로직 및 Checksum 확인 로직 추가

---

## 2021-07-01

- Gauge Data Connecting 구현

  : 데이터를 받온 데이터를 1씩 증가시키는 방향으로 구현

  : 바로바로 대입할 시에 부자연스럽게 뚝뚝 끊김

  : QTimer의 주기를 변경해봤는데 이거는 하드웨어 연결을 통해 조율이 필요할거같음

    (100ms -> 50ms)

  : 주기 조율이 어려울 경우에는 데이터 증감률을 늘려야할것같음. 현재는 1

- Arduino Demo File 작업

  : Demo Test를 위한 코드 구현

  : 아직 보드 테스트 미완료. Endian에 따라 Code 수정이 필요할 수도 있음

---

## 2021-07-06

- 아두이노 Test 및 라이브러리 적용 

- Serial 포트 불러오기 설정

---

## 2021-07-07

- Serial Message Rx Thread 구현

- Rx Queue를 통해 GUI와 Rx Thread 간 정보 공유

- Serial Port용 ComboBox 완성

  : Test는 필요

-  GUI 내에서 Thread를 생성에 실행도도록 설계

  : 실제 Arduino를 연결해두고 Test가 필요함

---

## 2021-07-08

- Arduino Test 완료

  : 통신 안정성 필요 (4 Byte단위로 끊어 읽는데 순서가 뒤바뀌는 경우가 발생)

- 오타 및 connect 수정

- Data_Packet 오류 수정

  : 디버깅 시 Type 이나 Endian 문제 발생 해결