id_from_name = {}
max_id = 0

MEMBER_CAPACITY = 100
MAX_DAY = 7
GOLD_GRADE_CUT = 50
SILVER_GRADE_CUT = 30

attendance_count = [[0] * MAX_DAY for _ in range(MEMBER_CAPACITY)]
points = [0] * MEMBER_CAPACITY
grade = [0] * MEMBER_CAPACITY
name_from_id = [''] * MEMBER_CAPACITY
weekend_count = [0] * MEMBER_CAPACITY


MONDAY = 'monday'
TUESDAY = 'tuesday'
WEDNESDAY = 'wednesday'
THURSDAY = 'thursday'
FRIDAY = 'friday'
SATURDAY = 'saturday'
SUNDAY = 'sunday'
DAY_INDEX = 'day_index'
DAY_POINT = 'day_point'
DAY_WEEKEND = 'day_weekend'


GRADE_GOLD = 'GOLD'
GRADE_SILVER = 'SILVER'
GRADE_NORMAL = 'NORMAL'
GRADE_INDEX = 'grade_index'

GRADE_INFO = {
    GRADE_GOLD: {
        GRADE_INDEX: 1
    },
    GRADE_SILVER: {
        GRADE_INDEX: 2
    },
    GRADE_NORMAL: {
        GRADE_INDEX: 0
    }
}


DAY_INFO = {
    MONDAY: {
        DAY_INDEX: 0,
        DAY_POINT: 1,
        DAY_WEEKEND: False,
    },
    TUESDAY: {
        DAY_INDEX: 1,
        DAY_POINT: 1,
        DAY_WEEKEND: False,
    },
    WEDNESDAY: {
        DAY_INDEX: 2,
        DAY_POINT: 3,
        DAY_WEEKEND: False,
    },
    THURSDAY: {
        DAY_INDEX: 3,
        DAY_POINT: 1,
        DAY_WEEKEND: False,
    },
    FRIDAY: {
        DAY_INDEX: 4,
        DAY_POINT: 1,
        DAY_WEEKEND: False,
    },
    SATURDAY: {
        DAY_INDEX: 5,
        DAY_POINT: 2,
        DAY_WEEKEND: True,
    },
    SUNDAY: {
        DAY_INDEX: 6,
        DAY_POINT: 2,
        DAY_WEEKEND: True,
    },
}


def process_attendance_data(member_name: str, day: str) -> None:
    global max_id

    if member_name not in id_from_name:
        max_id += 1
        id_from_name[member_name] = max_id
        name_from_id[max_id] = member_name

    member_id = id_from_name[member_name]
    
    day_info = DAY_INFO.get(day, None)
    if day_info is None:
        return

    attendance_count[member_id][day_info[DAY_INDEX]] += 1
    points[member_id] += day_info[DAY_POINT]

    if day_info[DAY_WEEKEND]:
        weekend_count[member_id] += 1


def check_should_remove(member_id: int) -> bool:
    if grade[member_id] not in (1, 2) and weekend_count[member_id] == 0 and \
        attendance_count[member_id][DAY_INFO[WEDNESDAY][DAY_INDEX]] == 0:
        return True
    return False


def get_training_attendance_count(member_id: int) -> int:
    return attendance_count[member_id][DAY_INFO[WEDNESDAY][DAY_INDEX]]


def get_match_attendance_count(member_id: int) -> int:
    saturday_count = attendance_count[member_id][DAY_INFO[SATURDAY][DAY_INDEX]]
    sunday_count = attendance_count[member_id][DAY_INFO[SUNDAY][DAY_INDEX]]
    return saturday_count + sunday_count

def get_bonus_point(member_id: int) -> int:
    bonus_point = 0

    if get_training_attendance_count(member_id) >= 10:
        bonus_point += 10
    if get_match_attendance_count(member_id) >= 10:
        bonus_point += 10

    return bonus_point


def get_attendance_data_from_file() -> bool:
    try:
        with open('attendance_weekday_500.txt', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if not line:
                    break
                split_data = line.strip().split()
                if not len(split_data) == 2:
                    continue
                member_name, attendance_day = split_data
                process_attendance_data(member_name, attendance_day)
        return False

    except FileNotFoundError:
        print('파일을 찾을 수 없습니다.')
        return True


def update_members_grade() -> None:
    for member_id in range(1, max_id + 1):
        points[member_id] += get_bonus_point(member_id)

        if points[member_id] >= GOLD_GRADE_CUT:
            grade[member_id] = GRADE_INFO[GRADE_GOLD][GRADE_INDEX]
        elif points[member_id] >= SILVER_GRADE_CUT:
            grade[member_id] = GRADE_INFO[GRADE_SILVER][GRADE_INDEX]
        else:
            grade[member_id] = GRADE_INFO[GRADE_NORMAL][GRADE_INDEX]


def print_members_grade() -> None:
    for member_id in range(1, max_id + 1):
        print(f'NAME : {name_from_id[member_id]}, POINT : {points[member_id]}, GRADE : ', end='')
        if grade[member_id] == 1:
            print('GOLD')
        elif grade[member_id] == 2:
            print('SILVER')
        else:
            print('NORMAL')


def print_removed_member() -> None:
    print('\nRemoved player')
    print('==============')
    for member_id in range(1, max_id + 1):
        if check_should_remove(member_id):
            print(name_from_id[member_id])


if __name__ == '__main__':
    err = get_attendance_data_from_file()
    if err:
        exit(1)
    update_members_grade()
    print_members_grade()
    print_removed_member()