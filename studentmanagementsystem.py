
import json
import os

file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "students.json"
)

data_loaded = True
students = {}

def calculate_grade(percentage):
    if percentage >= 85:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 45:
        return "C"
    elif percentage >= 30:
        return "D"
    else:
        return "Fail"

def validate_student_data(data):
    if not isinstance(data, dict):
        return False

    required_fields = [
        "Student ID",
        "Student Name",
        "Branch",
        "Total Marks",
        "Percentage",
        "Total Fee",
        "Paid Fee",
        "Due Fee",
        "Grade"
    ]

    validated_students = {}

    try:
        for sid, details in data.items():
            student_id = int(sid)

            if student_id in validated_students:
                return False

            if student_id <= 0 or not isinstance(details, dict):
                return False

            if not all(field in details for field in required_fields):
                return False

            if isinstance(details["Student ID"], bool):
                return False

            if not isinstance(details["Student ID"], int):
                return False

            if details["Student ID"] != student_id:
                return False

            if not isinstance(details["Student Name"], str) or not details["Student Name"].strip():
                return False

            if not isinstance(details["Branch"], str) or not details["Branch"].strip():
                return False

            total_marks = details["Total Marks"]
            percentage = details["Percentage"]
            total_fee = details["Total Fee"]
            paid_fee = details["Paid Fee"]
            due_fee = details["Due Fee"]
            grade = details["Grade"]

            if isinstance(total_marks, bool) or not isinstance(total_marks, int):
                return False

            if not 0 <= total_marks <= 500:
                return False

            if isinstance(percentage, bool) or not isinstance(percentage, (int, float)):
                return False

            if percentage != total_marks / 5:
                return False

            for fee in [total_fee, paid_fee, due_fee]:
                if isinstance(fee, bool) or not isinstance(fee, int):
                    return False
                if fee < 0:
                    return False

            if paid_fee > total_fee:
                return False

            if due_fee != total_fee - paid_fee:
                return False

            if not isinstance(grade, str):
                return False

            if grade != calculate_grade(percentage):
                return False

            validated_students[student_id] = details

    except (ValueError, TypeError, KeyError):
        return False

    return validated_students

if os.path.exists(file_path):
    try:
        with open(file_path, "r") as file:
            loaded_data = json.load(file)

        validated_data = validate_student_data(loaded_data)

        if validated_data is False:
            raise ValueError("Invalid student records!")

        students = validated_data

    except (OSError, json.JSONDecodeError, ValueError, TypeError):
        print("Error loading student data! Please check students.json.")
        students = {}
        data_loaded = False

def save_students():
    if not data_loaded:
        print("Cannot save! Please fix the student data file first.")
        return False

    try:
        with open(file_path, "w") as file:
            json.dump(students, file, indent=4)

        return True

    except OSError:
        print("Error saving student data! Please check the file.")
        return False

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a whole number.")

def get_student_id():
    while True:
        sid = get_integer("Enter Student ID: ")

        if sid > 0:
            return sid

        print("Student ID must be a positive number!")

def get_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty!")

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====\n")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Students")
    print("4. Fee Details")
    print("5. Update Student")
    print("6. Academic Details")
    print("7. Exit")

    choice = get_integer("Enter your choice: ")

    if choice == 1:
        if not data_loaded:
            print("Cannot add students until students.json is fixed.")
            continue

        sid = get_student_id()

        if sid in students:
            print("Student ID already exists!")

        else:
            name = get_text("Enter student name: ")
            branch = get_text("Enter branch name: ")

            marks = []
            for i in range(1, 6):
                while True:
                    mark = get_integer(f"Enter subject {i} marks: ")
                    if 0 <= mark <= 100:
                        marks.append(mark)
                        break
                    print("Invalid marks! Enter marks between 0 and 100.")
            
            total_fee = get_integer("Enter total fee: ")
            paid_fee = get_integer("Enter paid fee: ")
            if total_fee < 0 or paid_fee < 0 or paid_fee > total_fee:
                print("Invalid fee details!")
            else:
                total_marks = sum(marks)
                percentage = total_marks / 5
                due_fee = total_fee - paid_fee
                grade = calculate_grade(percentage)

                students[sid] = {
                    "Student ID": sid,
                    "Student Name": name,
                    "Branch": branch,
                    "Total Marks": total_marks,
                    "Percentage": percentage,
                    "Total Fee": total_fee,
                    "Paid Fee": paid_fee,
                    "Due Fee": due_fee,
                    "Grade": grade
                }

                if save_students():
                    print("Student added successfully!")
                    print("Total Marks:", total_marks)
                    print("Percentage:", percentage)
                    print("Due Fee:", due_fee)
                    print("Grade:", grade)
                else:
                    del students[sid]
                    print("Student was not added because saving failed.")

    elif choice == 2:
        if not students:
            print("No students available!")

        else:
            print("\n===== STUDENT DETAILS =====")

            for sid, details in students.items():
                print("\n----------------------------")

                for key, value in details.items():
                    print(key + ":", value)

    elif choice == 3:
        sid = get_student_id()

        if sid in students:
            print("Student Found!")
            print("Student Name:", students[sid]["Student Name"])
            print("Branch:", students[sid]["Branch"])
            print("Total Marks:", students[sid]["Total Marks"])
            print("Percentage:", students[sid]["Percentage"])
            print("Due Fee:", students[sid]["Due Fee"])
            print("Grade:", students[sid]["Grade"])

        else:
            print("Student not found!")

    elif choice == 4:
        sid = get_student_id()

        if sid in students:
            print("Student found!")
            print("\n===== STUDENT FEE DETAILS =====")
            print("1. Total Fee")
            print("2. Paid Fee")
            print("3. Due Fee")

            fee_choice = get_integer("Enter your choice: ")

            if fee_choice == 1:
                print("Total Fee:", students[sid]["Total Fee"])

            elif fee_choice == 2:
                print("Paid Fee:", students[sid]["Paid Fee"])

            elif fee_choice == 3:
                print("Due Fee:", students[sid]["Due Fee"])

            else:
                print("Invalid choice!")

        else:
            print("Student not found!")

    elif choice == 5:
        sid = get_student_id()

        if sid in students:
            while True:
                print("\n===== UPDATE STUDENT DETAILS =====")
                print("1. Update Name")
                print("2. Update Branch")
                print("3. Update Total Marks")
                print("4. Update Fee Details")
                print("5. Finish Updating")

                update_choice = get_integer("Enter your choice: ")

                if update_choice == 1:
                    new_name = get_text("Enter the new name: ")
                    old_name = students[sid]["Student Name"]

                    students[sid]["Student Name"] = new_name

                    if save_students():
                        print("Name updated successfully!")
                    else:
                        students[sid]["Student Name"] = old_name
                        print("Name update cancelled!")

                elif update_choice == 2:
                    new_branch = get_text("Enter the new branch: ")
                    old_branch = students[sid]["Branch"]

                    students[sid]["Branch"] = new_branch

                    if save_students():
                        print("Branch updated successfully!")
                    else:
                        students[sid]["Branch"] = old_branch
                        print("Branch update cancelled!")

                elif update_choice == 3:
                    new_marks = get_integer("Enter new total marks: ")

                    if 0 <= new_marks <= 500:
                        old_marks = students[sid]["Total Marks"]
                        old_percentage = students[sid]["Percentage"]
                        old_grade = students[sid]["Grade"]

                        new_percentage = new_marks / 5
                        new_grade = calculate_grade(new_percentage)

                        students[sid]["Total Marks"] = new_marks
                        students[sid]["Percentage"] = new_percentage
                        students[sid]["Grade"] = new_grade

                        if save_students():
                            print("Marks, percentage and grade updated!")
                        else:
                            students[sid]["Total Marks"] = old_marks
                            students[sid]["Percentage"] = old_percentage
                            students[sid]["Grade"] = old_grade
                            print("Marks update cancelled!")

                    else:
                        print("Invalid marks! Enter a value from 0 to 500.")

                elif update_choice == 4:
                    new_total_fee = get_integer("Enter new total fee: ")
                    new_paid_fee = get_integer("Enter new paid fee: ")

                    if (new_total_fee >= 0 and
                            new_paid_fee >= 0 and
                            new_paid_fee <= new_total_fee):

                        old_total_fee = students[sid]["Total Fee"]
                        old_paid_fee = students[sid]["Paid Fee"]
                        old_due_fee = students[sid]["Due Fee"]

                        students[sid]["Total Fee"] = new_total_fee
                        students[sid]["Paid Fee"] = new_paid_fee
                        students[sid]["Due Fee"] = new_total_fee - new_paid_fee

                        if save_students():
                            print("Fee details updated successfully!")
                        else:
                            students[sid]["Total Fee"] = old_total_fee
                            students[sid]["Paid Fee"] = old_paid_fee
                            students[sid]["Due Fee"] = old_due_fee
                            print("Fee update cancelled!")
                    else:
                        print("Invalid fee details! Please check the amounts.")

                elif update_choice == 5:
                    print("Finished updating student details!")
                    break

                else:
                    print("Invalid choice!")

        else:
            print("Student ID does not exist!")

    elif choice == 6:
        sid = get_student_id()

        if sid in students:
            print("Student Found!")
            print("Student Name:", students[sid]["Student Name"])
            print("Total Marks:", students[sid]["Total Marks"])
            print("Percentage:", students[sid]["Percentage"])
            print("Grade:", students[sid]["Grade"])

        else:
            print("Student not found!")

    elif choice == 7:
        print("Thank you for using the Student Management System!")
        print("Have a great day!")
        break

    else:
        print("Invalid choice! Please select a number from 1 to 7.")
