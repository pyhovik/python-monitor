import pytest
import random
import allure

@pytest.fixture
def params_for_sum_test():
    a = random.randint(-100, 0)
    b = random.randint(-100, 0) 
    yield a, b
    print('function teardown')

@pytest.fixture(scope='module')
def params_for_mult_test():
    print('module setup')
    a = random.randint(-100, 100)
    b = random.randint(-50, 50)
    mul = a * b 
    yield dict(val1=a, val2=b, mul=mul)
    print("module teardown")

def idfn(val):
    return f"params: {val}"

@pytest.fixture(
    scope="class",
    params=[
        (1, 0),
        (-2.5, 4),
        (10, 0.1)
    ],
    ids=idfn    # принимает функцию или список с названиями наборов
    #ids=['set-1', 'set-2', 'set-3']
)
def fixture_with_params(request):
    return request.param

@pytest.fixture(scope="session")
def session_fixture():
    print('session setup')
    allure.attach('jojojojo', 
        name='attached string', 
        attachment_type=allure.attachment_type.TEXT)
    yield
    print('session teardown')