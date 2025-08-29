
from Member import Member, GoldMemberGrade, SilverMemberGrade, NormalMemberGrade, GradeGetter, \
    Attendance, AttendanceData, AttendanceDataReader, MemberManager


def test_gold_member_grade_init():
    grade = GoldMemberGrade()
    assert grade.get_name() == 'GOLD'

def test_silver_member_grade_init():
    grade = SilverMemberGrade()
    assert grade.get_name() == 'SILVER'

def test_normal_member_grade_init():
    grade = NormalMemberGrade()
    assert grade.get_name() == 'NORMAL'

def test_member_init():
    member = Member('test_name')
    assert member.get_name() == 'test_name'

def test_member_grade_getter():
    assert GradeGetter.get(51).get_name() == 'GOLD'
    assert GradeGetter.get(50).get_name() == 'GOLD'
    assert GradeGetter.get(49).get_name() == 'SILVER'
    assert GradeGetter.get(30).get_name() == 'SILVER'
    assert GradeGetter.get(29).get_name() == 'NORMAL'

def test_attendance_check_weekday():
    assert Attendance.check_weekday(Attendance.MONDAY) == True
    assert Attendance.check_weekday(Attendance.TUESDAY) == True
    assert Attendance.check_weekday(Attendance.WEDNESDAY) == True
    assert Attendance.check_weekday(Attendance.THURSDAY) == True
    assert Attendance.check_weekday(Attendance.FRIDAY) == True
    assert Attendance.check_weekday(Attendance.SUNDAY) == False
    assert Attendance.check_weekday(Attendance.SATURDAY) == False

def test_attendance_check_weekend():
    assert Attendance.check_weekend(Attendance.MONDAY) == False
    assert Attendance.check_weekend(Attendance.TUESDAY) == False
    assert Attendance.check_weekend(Attendance.WEDNESDAY) == False
    assert Attendance.check_weekend(Attendance.THURSDAY) == False
    assert Attendance.check_weekend(Attendance.FRIDAY) == False
    assert Attendance.check_weekend(Attendance.SATURDAY) == True
    assert Attendance.check_weekend(Attendance.SUNDAY) == True


def test_attendance_data_add(mocker):
    attendance = AttendanceData()
    attendance.add('')
    attendance.add(Attendance.MONDAY)
    attendance.add(Attendance.SATURDAY)
    assert attendance.get_training_count() == 0
    assert attendance.get_weekend_count() == 1
    assert attendance.get_point() == 3
    mocker.patch.object(AttendanceData, 'get_training_count', return_value=10)
    assert attendance.get_point() == 13
    mocker.patch.object(AttendanceData, 'get_match_count', return_value=10)
    assert attendance.get_point() == 23

def test_member_point():
    member = Member('test_name')
    member.attend(Attendance.MONDAY)
    assert member.get_point() == 1
    member.attend(Attendance.SUNDAY)
    assert member.get_point() == 3
    member.attend(Attendance.WEDNESDAY)
    assert member.get_point() == 6

def test_member_grade():
    member = Member('test_name')
    member.attend(Attendance.MONDAY)
    assert isinstance(member.get_grade(), NormalMemberGrade)
    assert member.get_grade_name() == 'NORMAL'

def test_member_weekend_count():
    member = Member('test_name')
    assert member.get_weekend_count() == 0
    member.attend(Attendance.MONDAY)
    assert member.get_weekend_count() == 0
    member.attend(Attendance.SATURDAY)
    assert member.get_weekend_count() == 1
    member.attend(Attendance.SUNDAY)
    assert member.get_weekend_count() == 2

def test_member_training_count():
    member = Member('test_name')
    assert member.get_training_count() == 0
    member.attend(Attendance.MONDAY)
    assert member.get_training_count() == 0
    member.attend(Attendance.SATURDAY)
    assert member.get_training_count() == 0
    member.attend(Attendance.SUNDAY)
    assert member.get_training_count() == 0
    member.attend(Attendance.WEDNESDAY)
    assert member.get_training_count() == 1

def test_member_is_normal_grade():
    member = Member('test_name')
    assert member.is_normal_grade() is True
    for _ in range(10):
        member.attend(Attendance.MONDAY)
    assert member.is_normal_grade() is True
    for _ in range(10):
        member.attend(Attendance.SUNDAY)
    assert member.is_normal_grade() is False

def test_member_manager_init():
    manager = MemberManager()
    manager.print_all()
    assert manager.get_member_count() == 0

    manager.update_member_data([
        ('person_0', Attendance.MONDAY),
        ('person_1', Attendance.MONDAY),
        ('person_0', Attendance.SUNDAY)
    ])
    manager.print_all()
    assert manager.get_member_count() == 2

    manager.update_member_data([
        (f'person_{i}', Attendance.MONDAY)
        for i in range(MemberManager.MAX_MEMBER + 1)
    ])
    manager.print_all()
    assert manager.get_member_count() == MemberManager.MAX_MEMBER

def test_attendance_data_reader(tmp_path):
    file_path = tmp_path / 'attendance_data.txt'
    file_path.write_text('test_name monday\n\n\ntest_name sunday')
    data = AttendanceDataReader.read(str(file_path))
    assert len(data) == 2
    data = AttendanceDataReader.read('attendance_weekday_501.txt')
    assert len(data) == 0
    data = AttendanceDataReader.read('attendance_weekday_500.txt')
    assert len(data) == 500
