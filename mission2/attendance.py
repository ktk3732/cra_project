from Member import AttendanceDataReader, MemberManager


if __name__ == '__main__':
    attendance_data = AttendanceDataReader.read('attendance_weekday_500.txt')
    manager = MemberManager(attendance_data)
    manager.print_all()
