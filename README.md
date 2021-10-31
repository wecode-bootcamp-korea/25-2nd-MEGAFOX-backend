# MEGAFOX
  영화 예매 사이트인 megabox에서 영감을 얻은 프로젝트

## 개발 기간
2021-10-18 ~ 2021-10-29

## 개발 인원
**Back-end** : 김도훈, 이다빈

**Front-end** : 정찬영, 강단, 신혜리
  
## ERD
![](https://media.vlpt.us/images/thisisemptyyy/post/c7aa7927-2537-4b1d-8c7e-0385301be90f/megafox_20211030_233447.png)

## Technologies
- 개발
  * Python@3.8.11
  * Django@3.2.8
  * MySQL@8.0.27
 
- 배포 
  - AWS(EC2, RDS, LB)

## Features
**이다빈**
* 카카오 소셜 로그인 API를 활용한 로그인 API(`GET`)
* 유저 정보 호출 API (`GET`)
* 유저 권한 확인용 로그인 데코레이터 구현
* 리뷰 생성, 삭제, 수정 API (`POST`, `GET`, `DELETE`, `PATCH`)
* 빠른예매, 예매내역 API(`POST`, `GET`)

**김도훈**
* 영화 리스트/상세페이지 API (`GET`)
* 영화관 리스트 API (`GET`)
* 영화, 영화관, 댓글 좋아요/삭제 API (`POST`)
* 빠른예매, 예매내역 API (`POST`, `GET`)

## Endpoint
- users
  * `GET`/users/kakao/signin (로그인)
  * `GET`/users/ingo (유저정보)

- movies
  * `GET`/movie (영화 목록)
  * `GET`/movie/<movie_id> (영화 상세정보)

- theaters
  * `GET`/theaters (영화관 목록)

- reviews
  * `POST`/review/comment (리뷰 작성)
  * `GET`/review/comment (리뷰 가져오기)
  * `DELETE`/review/comment/<review_id> (리뷰 삭제)
  * `PATCH`/review/comment/<review_id> (리뷰 수정)

- likes
  * `POST`/like/movie/<movie_id> (영화 즐겨찾기)
  * `POST`/like/theater/<theater_id> (영화관 즐겨찾기)
  * `POST`/like/review/<review_id> (리뷰 좋아요)

- bookings
  * `GET`/booking (예매내역 확인)
  * `GET`/booking/reserve (예매페이지 불러오기/날짜별 상영시간 필터링)
  * `POST`/booking/reserve (영화 예매하기)
