# Arduino Monitor

---

[TOC]

---

## To Do

- [x] Timer 구현
- [ ] Serial Connect 구현
- [x] Layout 구성
- [ ] Protocol 정립
- [ ] 데이터 별 Widget 연결
- [ ] 데이터 Class 구축 필요

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



