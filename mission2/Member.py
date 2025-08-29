
import os
from abc import ABC, abstractmethod


class AbstractMemberGrade(ABC): #  pragma: no cover
    @abstractmethod
    def get_name(self) -> str:
        pass


class GoldMemberGrade(AbstractMemberGrade):
    def get_name(self) -> str:
        return 'GOLD'


class SilverMemberGrade(AbstractMemberGrade):
    def get_name(self) -> str:
        return 'SILVER'


class NormalMemberGrade(AbstractMemberGrade):
    def get_name(self) -> str:
        return 'NORMAL'


class GradeGetter:
    @staticmethod
    def get(point: int) -> AbstractMemberGrade:
        if point >= 50:
            return GoldMemberGrade()
        elif point >= 30:
            return SilverMemberGrade()
        else:
            return NormalMemberGrade()


class Attendance:
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    @staticmethod
    def check_weekday(day):
        if day in [
            Attendance.MONDAY, Attendance.TUESDAY, Attendance.WEDNESDAY,
            Attendance.THURSDAY, Attendance.FRIDAY
        ]:
            return True
        else:
            return False

    @staticmethod
    def check_weekend(day):
        if day in [
            Attendance.SATURDAY, Attendance.SUNDAY
        ]:
            return True
        else:
            return False

class AttendanceData:
    TRAINING_POINT = 3
    WEEKEND_POINT = 2
    NORMAL_POINT = 1

    def __init__(self):
        self._count = {
            Attendance.MONDAY: 0,
            Attendance.TUESDAY: 0,
            Attendance.WEDNESDAY: 0,
            Attendance.THURSDAY: 0,
            Attendance.FRIDAY: 0,
            Attendance.SATURDAY: 0,
            Attendance.SUNDAY: 0
        }
        self._weekend_count = 0
        self._training_days = [
            Attendance.WEDNESDAY
        ]
        self._match_days = [
            Attendance.SATURDAY,
            Attendance.SUNDAY
        ]

    def add(self, day: str) -> None:
        if day not in self._count:
            return
        self._count[day] += 1
        if Attendance.check_weekend(day):
            self._weekend_count += 1

    def get_point(self) -> int:
        point = 0

        for day, count in self._count.items():
            if day in self._training_days:
                point += count * AttendanceData.TRAINING_POINT
            elif Attendance.check_weekend(day):
                point += count * AttendanceData.WEEKEND_POINT
            else:
                point += count * AttendanceData.NORMAL_POINT

        point += self._get_bonus_point()
        return point

    def _get_bonus_point(self) -> int:
        bonus_point = 0

        if self.get_training_count() >= 10:
            bonus_point += 10
        if self.get_match_count() >= 10:
            bonus_point += 10

        return bonus_point

    def get_weekend_count(self) -> int:
        return self._weekend_count

    def get_training_count(self) -> int:
        count = 0
        for training_day in self._training_days:
            count += self._count[training_day]

        return count

    def get_match_count(self) -> int:
        count = 0
        for match_day in self._match_days:
            count += self._count[match_day]

        return count

class Member:
    def __init__(self, name: str):
        self._name: str = name
        self._grade: AbstractMemberGrade = NormalMemberGrade()
        self._attendance: AttendanceData = AttendanceData()

    def get_name(self) -> str:
        return self._name

    def get_point(self) -> int:
        return self._attendance.get_point()

    def get_grade(self) -> AbstractMemberGrade:
        self._update_grade()
        return self._grade

    def get_grade_name(self) -> str:
        return self.get_grade().get_name()

    def attend(self, day: str) -> None:
        self._attendance.add(day)

    def get_weekend_count(self) -> int:
        return self._attendance.get_weekend_count()

    def get_training_count(self) -> int:
        return self._attendance.get_training_count()

    def _update_grade(self) -> None:
        self._grade = GradeGetter.get(self.get_point())

    def is_normal_grade(self) -> bool:
        if isinstance(self.get_grade(), NormalMemberGrade):
            return True
        else:
            return False


class MemberManager:
    MAX_MEMBER = 100

    def __init__(self, attendance_data: list = None):
        self._members_id: dict = {}
        self._members: list[Member] = []
        self.update_member_data(attendance_data or [])

    def update_member_data(self, attendance_data: list) -> None:
        self._members_id.clear()
        self._members.clear()
        self._members.append(Member(name=''))
        member_count = 0

        for member_name, day in attendance_data:
            if member_name not in self._members_id:
                if member_count >= MemberManager.MAX_MEMBER:
                    break
                member_count += 1
                self._members_id[member_name] = member_count
                self._members.append(Member(name=member_name))

            member_id = self._members_id[member_name]
            member = self._members[member_id]
            member.attend(day)

    def get_member_count(self) -> int:
        return len(self._members_id.keys())

    def print_all(self) -> None:
        self.print_members_grade()
        self.print_removed_members()

    def print_members_grade(self) -> None:
        if self._is_empty():
            return

        for member in self._members[1:]:
            name = member.get_name()
            point = member.get_point()
            grade = member.get_grade_name()
            print(f'NAME : {name}, POINT : {point}, GRADE : {grade}')

    def print_removed_members(self) -> None:
        print('\nRemoved player')
        print('==============')
        if self._is_empty():
            return

        for member in self._members[1:]:
            if self._should_be_removed(member):
                print(member.get_name())

    def _should_be_removed(self, member: Member) -> bool:
        if (member.is_normal_grade() and
                member.get_weekend_count() == 0 and
                member.get_training_count() == 0):
            return True
        else:
            return False

    def _is_empty(self):
        if self.get_member_count() == 0:
            return True
        else:
            return False


class AttendanceDataReader:
    @staticmethod
    def read(file_path: str) -> list:
        read_data = list()
        try:
            with open(file_path, encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    split_data = line.strip().split()
                    if not len(split_data) == 2:
                        continue
                    member_name, attendance_day = split_data
                    read_data.append((member_name, attendance_day))
            return read_data

        except FileNotFoundError:
            print('파일을 찾을 수 없습니다.')
            return []