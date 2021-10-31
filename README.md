# MEGAFOX
  영화 예매 사이트인 megabox에서 영감을 얻은 프로젝트

## 개발 기간 / 개발 인원
  개발 기간: 2021-10-18 ~ 2021-10-29
  <br>
  개발 인원: 김도훈(**백엔드**), 이다빈(**백엔드**),
            정찬영(**프론트엔트**), 강단(**프론트엔트**), 신혜리(**프론트엔트**)
  
## DB modeling
![megafox_20211031_174305](https://user-images.githubusercontent.com/56703088/139575208-274bf141-6fe5-452b-8854-5945ef763cfe.png)
## Technologies
* Python
* Django
* MySQL
* AWS EC2, RDS, LB
* Git, Github
* Slack, Trello

## Features
**이다빈**
* 소셜 로그인, 유저 정보 호출 API (``GET``)
* 리뷰 생성, 삭제, 수정 API (``POST``, ``GET``, ``DELETE``, ``PATCH``)
* 빠른예매, 예매내역 API(``POST``, ``GET``)


**김도훈**
* 영화 리스트/상세페이지 API (``GET``)
* 영화관 리스트 API (``GET``)
* 영화, 영화관, 댓글 좋아요/삭제 API (``POST``)
* 빠른예매, 예매내역 API (``POST``, ``GET``)

## Endpoint
* ``GET``/users/kakao/signin (로그인)
* ``GET``/users/ingo (유저정보)
* ``GET``/movie (영화 목록)
* ``GET``/movie/<movie_id> (영화 상세정보)
* ``GET``/theaters (영화관 목록)
* ``POST``/review/comment (리뷰 작성)
* ``GET``/review/comment (리뷰 가져오기)
* ``DELETE``/review/comment/<review_id> (리뷰 삭제)
* ``PATCH``/review/comment/<review_id> (리뷰 수정)
* ``POST``/like/movie/<movie_id> (영화 즐겨찾기)
* ``POST``/like/theater/<theater_id> (영화관 즐겨찾기)
* ``POST``/like/review/<review_id> (리뷰 좋아요)
* ``GET``/booking (예매내역 확인)
* ``GET``/booking/reserve (예매페이지 불러오기/날짜별 상영시간 필터링)
* ``POST``/booking/reserve (영화 예매하기)
