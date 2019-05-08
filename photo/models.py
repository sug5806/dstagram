from django.db import models

# Create your models here.
# 기본 모델
"""

작성자 : author
본문글 : text
사진 : image
작성일 : created
수정일 : updated

+ tag, like
-- comment
"""
from django.contrib.auth.models import User
# url pattern 이름을 가지고 주소를 만들어주는 함수
from django.urls import reverse

# User모델은 확장 가능
# settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    # related_name으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 실행해야 한다.
    # 내 프로필 페이지 - 내가 올린 사진만 뜬다.

    # models.ForeignKey(get_user_model(), )
    # CASCADE 연속해서 지운다. 탈퇴하면 사진도 싹 지운다.
    # PROTECT 사진 다 안지우면 너 탈퇴 안됨 - 탈퇴 프로세스에 사진을 우선 삭제하고 탈퇴 시킨다.
    # 특정값으로 셋팅 -

    text = models.TextField(blank=True)

    # upload_to는 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)

    # 예약어를 필드명으로 사용하면 안된다.
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('photo:detail', args=[self.id])