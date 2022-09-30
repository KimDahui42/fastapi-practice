# fast api 자습서 메모

## 동기와 비동기

### 동기(synchronous:동시에 일어난다)

요청과 결과가 동시에 발생

-   요청을 보냈을 때 응답을 받아야만 다음 동작을 수행할 수 있다.
-   태스크가 순차적으로 수행된다.

#### 장점

설계가 간단, 직관적

#### 단점

결과가 주어질 때까지 대기(블로킹, 작업중단)해야함

### 비동기(asynchronous:동시에 일어나지 않는다)

요청과 결과가 동시에 발생 X

-   요청을 보냈을 때 응답이 돌아오지 않아도 다음 동작을 수행할 수 있다.
-   태스크가 비순차적으로 수행된다.

#### 장점

동기에 비해 복잡

#### 단점

결과까지 대기 없이 다른 작업 처리가 가능 -> 자원의 효율적인 사용 가능

## async/await in FastAPI

-   async def로 선언된 함수 내부에서만 await를 사용할 수 있다.
-   async def 사용이 필수가 아님 def로 선언 가능

```python
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

## 순서

path operation은 순차적으로 판별된다.
