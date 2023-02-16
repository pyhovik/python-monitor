import pytest

@pytest.fixture(scope='function')
def fixture1():
    print('fixture1')
    return 'fix1'

@pytest.fixture(scope='class')
def fixture2():
    print('fixture2')
    return 'fix2'

@pytest.fixture(scope='module')
def fixture3():
    print('fixture3')
    return 'fix3'

@pytest.fixture(scope='function')
def fixture4(fixture1):
    print('fixture4')
    return fixture1 + 'fix4'

@pytest.mark.usefixtures('fixture3')
class TestClass1():
    def test_1(self, fixture1, fixture2):
        print("test1", fixture2)
    def test_2(self, fixture1, fixture2):
        print("test2", fixture1)

def test_3(fixture3):
    print(fixture3)