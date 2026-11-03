# Student Design Verification Report

## Original requirements
A university offers courses.
Each course has multiple sections.
Each section belongs to one course and is taught by one course.
Each course can teach multiple sections.
Students may enroll in multiple sections and each section may have multiple students.
An enrollment records a grade.
Assume each student enrolls in a given section at most once.

## Assumptions (verify with stakeholder)
- Section has a globally unique section_id.
- Enrollment grade must be added as a relationship attribute manually in this starter version.

## Clarification questions
- What grade values are permitted?
- Can a section have multiple instructors in exceptional cases?

## Mapping warnings
- Section -> Course: confirm FK optionality and participation; generated FK is nullable
- Section -> Instructor: confirm FK optionality and participation; generated FK is nullable

## Student verification checklist
- [ ] All entities and attributes match the original requirements.
- [ ] Cardinality and participation are supported by explicit business rules.
- [ ] Every primary key is a genuine unique identifier.
- [ ] Foreign keys, junction tables, and relationship attributes are correct.
- [ ] For each claimed 3NF relation, list FDs and candidate keys and justify 3NF.
- [ ] Test DDL in Oracle; do not treat successful execution as semantic proof.
- [ ] Document at least three possible errors, limitations, or design decisions.

## Important limitations
The agent does not prove 3NF or infer functional dependencies reliably from prose.
One-to-one relationships require manual mapping. Participation/optional constraints require manual review.
Mermaid and SQL are candidate artifacts, not verified business designs.
