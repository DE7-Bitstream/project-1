# web-service
## 데이터 load 방법
- 기본 설정
```python
python manage.py makemigrations
python manage.py migrate
```

- weekly 데이터
```python
python manage.py load_weekly_chart
```

- hitmakers 데이터

```python
python manage.py load_hitmakers_data
```
