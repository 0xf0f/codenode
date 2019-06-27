from quicktest import TestList
# import TestClass here


testclass_tests = TestList('TestClass tests')


# @testclass_tests.test
# def test___delattr__(instance):
#     pass
# 

# @testclass_tests.test
# def test___dir__(instance):
#     pass
# 

# @testclass_tests.test
# def test___eq__(instance):
#     pass
# 

# @testclass_tests.test
# def test___format__(instance):
#     pass
# 

# @testclass_tests.test
# def test___ge__(instance):
#     pass
# 

# @testclass_tests.test
# def test___getattribute__(instance):
#     pass
# 

# @testclass_tests.test
# def test___gt__(instance):
#     pass
# 

# @testclass_tests.test
# def test___hash__(instance):
#     pass
# 

# @testclass_tests.test
# def test___init__(instance):
#     pass
# 

# @testclass_tests.test
# def test___init_subclass__(instance):
#     pass
# 

# @testclass_tests.test
# def test___le__(instance):
#     pass
# 

# @testclass_tests.test
# def test___lt__(instance):
#     pass
# 

# @testclass_tests.test
# def test___ne__(instance):
#     pass
# 

# @testclass_tests.test
# def test___new__(instance):
#     pass
# 

# @testclass_tests.test
# def test___reduce__(instance):
#     pass
# 

# @testclass_tests.test
# def test___reduce_ex__(instance):
#     pass
# 

# @testclass_tests.test
# def test___repr__(instance):
#     pass
# 

# @testclass_tests.test
# def test___setattr__(instance):
#     pass
# 

# @testclass_tests.test
# def test___sizeof__(instance):
#     pass
# 

# @testclass_tests.test
# def test___str__(instance):
#     pass
# 

# @testclass_tests.test
# def test___subclasshook__(instance):
#     pass
# 

# @testclass_tests.test
# def test_test_method(instance):
#     pass
# 

def run_tests():
    instance = TestClass()
    testclass_tests.run(instance)
