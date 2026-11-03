-- Candidate Oracle DDL; review keys, business rules, and optionality before use.

CREATE TABLE Student (
    student_id NUMBER(10) NOT NULL,
    full_name VARCHAR2(255) NOT NULL,
    CONSTRAINT pk_Student PRIMARY KEY (student_id)
);

CREATE TABLE Course (
    course_id NUMBER(10) NOT NULL,
    title VARCHAR2(255) NOT NULL,
    CONSTRAINT pk_Course PRIMARY KEY (course_id)
);

CREATE TABLE Section (
    section_id NUMBER(10) NOT NULL,
    term VARCHAR2(255) NOT NULL,
    course_course_id NUMBER(10),
    instructor_instructor_id NUMBER(10),
    CONSTRAINT pk_Section PRIMARY KEY (section_id)
);

CREATE TABLE Instructor (
    instructor_id NUMBER(10) NOT NULL,
    full_name VARCHAR2(255) NOT NULL,
    CONSTRAINT pk_Instructor PRIMARY KEY (instructor_id)
);

CREATE TABLE Student_Section (
    student_student_id NUMBER(10) NOT NULL,
    section_section_id NUMBER(10) NOT NULL,
    CONSTRAINT pk_Student_Section PRIMARY KEY (student_student_id, section_section_id)
);

ALTER TABLE Section ADD CONSTRAINT fk_Section_1 FOREIGN KEY (course_course_id) REFERENCES Course (course_id);
ALTER TABLE Section ADD CONSTRAINT fk_Section_2 FOREIGN KEY (instructor_instructor_id) REFERENCES Instructor (instructor_id);
ALTER TABLE Student_Section ADD CONSTRAINT fk_Student_Section_1 FOREIGN KEY (student_student_id) REFERENCES Student (student_id);
ALTER TABLE Student_Section ADD CONSTRAINT fk_Student_Section_2 FOREIGN KEY (section_section_id) REFERENCES Section (section_id);
