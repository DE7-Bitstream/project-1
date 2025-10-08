# web-service
```python
repo
|- dataframes
|    |- < 기능별 이름 ex. weekly_chart ... >
|        | csv파일들 ...
|- bitstream
|- < 기능별 이름  >
|     |- static
|        |- < 기능별 이름 >
|            |- css
|                | css 파일
|            |- js
|                | js 파일
|     |- templates
|        |- < 기능별 이름 >
|            | html 파일
| README.md
| manage.py
| ...

```
-------
## 데이터 load 방법

- weekly 데이터
```python
python manage.py load_weekly_chart
```

- hitmakers 데이터

```python
# 1) 모델 생성
python manage.py migrate hitmakers

# 2) 데이터 로드
python manage.py load_hitmakers_data
```

-------
## 공통 레이아웃 적용 방법
만드신 각 app의 html에서, 아래 코드를 이용하면 레이아웃 사용할 수 있습니다.  


```html
{% extends "layout.html" %}

{% block content %}
  <h2>이건 weekly_chart 페이지입니다</h2>
  <p>파이팅.</p>
{% endblock %}
```   

`templates/layout.html` 은 베이스 html 파일  
`static/` 내부 파일들은 `layout.html` 에서 사용한 style과 이미지이고,  
`bitstream/settings.py` 내부에서   
```python
...

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

...

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]


```  

수정해서 templates와 static 반영하게 수정했습니다.