from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
# 유저 목록이 출력되는 뷰
# + 기능 Follow라는 기능
# 중간 테이블을 직접 생성 - 모델

# 유저 모델을 커스터마이징 -> 1. 커스터마이징 하는 방법을 배워서
# 확장 하는 방법에 따라서
# 1) 새로운 유저 모델을 만드는 방법 - 기존 유저 데이터를 유지할 수가 없다.
# 2) 기존 모델을 확장 하는 방법 - DB 다운 타임 alter table - table lock
# 나 유저 모델
# 나를 팔로우한 사람 필드
# 내가 팔로우한 사람 필드

# 커스터마이징 할 수가 없다면?
# 새로운 모델을 추가하는 방법


# 사진 모델
# 사진을 좋아요한 사람 필드
# 사진을 저장한 사람 필드


"""
1. 유저 목록 혹은 유저 프로필에서 팔로우 버튼
1-1. 전체 유저 목록을 출력해주는 뷰 - User모델에 대한 ListView

2. 팔로우 정보를 저장하는 뷰
"""
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from .forms import SignupForm

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'


# 기존에 입력받는 뷰인 Create를 상속받아서하면 커스텀이 힘들다
# 기존의 회원가입 -> User 모델에 값을 입력받는다. -> CreateView
# 현재는 회원 가입시 모델 필드외에 추가 입력이 필요하다.
# 커스텀을 하려면 함수형 뷰가 적절하다

def signup(request):
    if request.method == "POST":
        # Post로 넘어온 data를 받을수있다
        # get안의 인자는 label의 이름과 같아야 한다
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # print(username, password)
        #
        # user = User()
        # user.username = username
        # user.set_password(password)
        # user.save()

        # data가 채워진형태로 form을 만든다
        signup = SignupForm(request.POST)

        if signup.is_valid():
            # False를 하지 않으면 DBdp 저장한다음 다시 암호화를 하고
            # 저장하기 때문에 DB에 불필요한 접근을 방지하기위해 False를 한다

            # 1. 인스턴스 생성
            user_instance = signup.save(commit=False)

            # 해쉬키와 섞어서 암호화 한다
            user_instance.set_password(signup.cleaned_data['password'])
            user_instance.save()

            id = user_instance.username

            return render(request, 'accounts/signup_complete.html', {'id' : id })

    else:
        # 아무것도 채워지지 않은 폼이 만들어진다
        signup = SignupForm()

        # render의 역할 :
        # 1. 템플릿 불러오기
        # 2. 템플릿 렌더링 하기
        # 3. HTTP Response하
    return render(request, 'accounts/signup.html', {'form' : signup})


