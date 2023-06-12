import pytest

from create_students import generate_group_name, courses_description, generate_full_name, create_groups,\
    create_courses, create_students


def test_generate_group_name():
    result = generate_group_name()
    letters = result[:2]
    hyphen = result[2]
    number = result[3:]
    
    assert len(result) == 5
    assert letters.isalpha()
    assert hyphen == "-"
    assert number.isnumeric()
    

@pytest.mark.parametrize("course", ["Mathematics", "Computer Science", "English"])
def test_courses_description(course):
    result = courses_description()
    
    assert course in result


def test_generate_full_name():
    result = generate_full_name()
    
    assert type(result) == str
    assert len(result.split()) == 2


def test_create_groups():
    result = create_groups()
    
    assert len(result) == 10 # 10 is default parameter


def test_create_groups_typeerror():
    with pytest.raises(TypeError):
        create_groups("some string")


def test_create_courses():
    result = create_courses()
    
    assert type(result) == list
    

def test_create_students():
    result = create_students()
    
    assert len(result) == 200 # 200 is default parameter


def test_create_students_typeerror():
    with pytest.raises(TypeError):
        create_courses([])
