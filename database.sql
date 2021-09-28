-- Create Course, Class

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    description text,
    is_retired boolean NOT NULL DEFAULT false
);

CREATE TABLE course_prerequisite (
    id SERIAL PRIMARY KEY,
    course_id integer REFERENCES course(id),
    prerequisite_course_id integer REFERENCES course(id),
    is_active boolean NOT NULL DEFAULT true,
    UNIQUE (course_id, prerequisite_course_id)
);

CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    course_id integer REFERENCES course(id),
    class_id integer UNIQUE,
    max_capacity integer NOT NULL,
    current_capacity integer DEFAULT 0,
    class_start_date text NOT NULL,
    class_end_date text NOT NULL,
    enrolment_start_date text NOT NULL,
    enrolment_end_date text NOT NULL,
    UNIQUE (course_id, class_id)
);


-- Create Learners, Trainers, Administrators

CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE learner (
    id SERIAL PRIMARY KEY,
    email text UNIQUE,
    password text NOT NULL,
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL,
    department_id integer REFERENCES department(id)
);

CREATE TABLE trainer (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES learner(id),
    course_id integer REFERENCES class(id),
    class_id integer REFERENCES class(class_id),
    UNIQUE(user_id, course_id, class_id)
);

CREATE TABLE administrator (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES learner(id)
);


-- Create Enrolment and Learner_Course_Completion

CREATE TABLE enrolment (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES learner(id),
    course_id integer REFERENCES course(id),
    class_id integer REFERENCES class(class_id),
    enrolment_date text NOT NULL,
    is_approved boolean DEFAULT false,
    is_withdrawn boolean DEFAULT false,
    course_progress real DEFAULT '0'::real,
    UNIQUE (user_id, course_id, class_id)
);

CREATE TABLE learner_course_completion (
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  course_id integer REFERENCES course(id),
  class_id integer REFERENCES class(class_id),
  completion_date text NOT NULL,
  UNIQUE (user_id, course_id, class_id)
);


-- Create Lesson, Course_Material, Learner_Progress

CREATE TABLE lesson (
  id SERIAL PRIMARY KEY,
  course_id integer REFERENCES course(id),
  class_id integer REFERENCES class(class_id),
  lesson_id integer UNIQUE,
  lesson_order integer,
  UNIQUE (course_id, class_id, lesson_id)
);

CREATE TABLE learner_lesson_progress (
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  course_id integer REFERENCES course(id),
  class_id integer REFERENCES class(class_id),
  lesson_id integer REFERENCES lesson(lesson_id),
  UNIQUE (user_id, course_id, class_id, lesson_id)
);

/**
TODO: FOR FUTURE

CREATE TABLE course_material (
  id SERIAL PRIMARY KEY,
  course_id integer REFERENCES course(id),
  class_id integer REFERENCES class(class_id),
  lesson_id integer REFERENCES lesson(lesson_id),
);


CREATE TABLE course_material_document (
  id SERIAL PRIMARY KEY,
  document_name text,
  
);


CREATE TABLE course_material_hyperlink (
  id SERIAL PRIMARY KEY,

);
*/


-- Quiz

CREATE TABLE quiz (
  id SERIAL PRIMARY KEY,
  course_id integer REFERENCES course(id),
  class_id integer REFERENCES class(class_id),
  timer integer,
  passing_score_percentage real DEFAULT 0,
  is_graded boolean DEFAULT false,
  UNIQUE (course_id, class_id)
);

CREATE TABLE quiz_ungraded (
  id SERIAL PRIMARY KEY,
  quiz_id integer REFERENCES quiz(id) UNIQUE,
  lesson_id integer REFERENCES lesson(lesson_id)
);

CREATE TABLE quiz_question_type (
  id SERIAL PRIMARY KEY,
  question_type text NOT NULL UNIQUE
);

CREATE TABLE quiz_question (
  id SERIAL PRIMARY KEY,
  quiz_id integer REFERENCES quiz(id) UNIQUE,
  question_type_id integer REFERENCES quiz_question_type(id),
  question_title text NOT NULL
);

CREATE TABLE quiz_question_true_false (
  id SERIAL PRIMARY KEY,
  question_id integer REFERENCES quiz_question(id) UNIQUE,
  answer_true text NOT NULL,
  answer_false text NOT NULL,
  correct_answer boolean NOT NULL
);

CREATE TABLE quiz_question_mcq_answer (
  id SERIAL PRIMARY KEY,
  question_id integer REFERENCES quiz_question(id),
  answer text NOT NULL,
  is_correct boolean NOT NULL
);

CREATE TABLE learner_quiz_attempt (
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  quiz_id integer REFERENCES quiz(id),
  time_start numeric NOT NULL
);

CREATE TABLE learner_quiz_attempt_question_answer (
  id SERIAL PRIMARY KEY,
  learner_quiz_attempt_id integer REFERENCES learner_quiz_attempt,
  question_id integer REFERENCES quiz_question(id),
  answer integer NOT NULL
);


/***
 * INSERT DATABASE CONTENTS
*/

-- DEPARTMENT
INSERT INTO department (name) VALUES ('Human Resource and Admin');
INSERT INTO department (name) VALUES ('Engineers');

-- LEARNERS
INSERT INTO learner (email, password, first_name, last_name, department_id)
  VALUES ('admin@lms.com', 'p@ssword', 'User', 'User', 1);
INSERT INTO learner (email, password, first_name, last_name, department_id)
  VALUES ('engineer1@lms.com', 'p@ssword', 'Engineer 1', 'Loh', 2);
INSERT INTO learner (email, password, first_name, last_name, department_id)
  VALUES ('engineer2@lms.com', 'p@ssword', 'Engineer 2', 'Minh', 2);
INSERT INTO learner (email, password, first_name, middle_name, last_name, department_id)
  VALUES ('karen@lms.com', 'p@ssword', 'Karen', 'J.','See', 2);
INSERT INTO learner (email, password, first_name, last_name, department_id)
  VALUES ('sami@lms.com', 'p@ssword', 'Sam', 'Willows', 2);

-- ADMINS
INSERT INTO administrator(user_id) VALUES (1);

-- COURSES
INSERT INTO course (name)
  VALUES ('AIO Workplace Safety and Health');
INSERT INTO course (name, description)
  VALUES ('Fundamentals of Xerox WorkCentre 7845', 'A beginner guide to Xerox WorkCentre');
INSERT INTO course (name, description)
  VALUES ('Programming for Xerox WorkCentre with Card Access and Integration', 'Now with tools!');
INSERT INTO course (name, description)
  VALUES ('Fundamentals of Electrical Wirings', 'Bzzzt!');

-- COURSE PREREQUISITE
INSERT INTO course_prerequisite (course_id, prerequisite_course_id)
  VALUES (1, 4)