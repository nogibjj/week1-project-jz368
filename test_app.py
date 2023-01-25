from app import checkweekday
def test_checkweekday():
    # future
    assert checkweekday(2023, 3, 8)==3
    assert checkweekday(2025, 1, 1)==3
    assert checkweekday(2026, 8, 22)==6
    assert checkweekday(2027, 10, 1)==5

    # past
    assert checkweekday(1998, 8, 22)==6
    assert checkweekday(2008, 8, 17)==0

    # now 
    assert checkweekday(2023, 1, 24)==2
test_checkweekday()