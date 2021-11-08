-- Create Course, Class

CREATE TABLE course
(
  id SERIAL PRIMARY KEY,
  name text NOT NULL,
  description text,
  is_retired boolean NOT NULL DEFAULT false
);

CREATE TABLE course_prerequisite
(
  id SERIAL PRIMARY KEY,
  course_id integer REFERENCES course(id),
  prerequisite_course_id integer REFERENCES course(id),
  is_active boolean NOT NULL DEFAULT true,
  UNIQUE (course_id, prerequisite_course_id)
);

CREATE TABLE class
(
  id SERIAL PRIMARY KEY,
  course_id integer REFERENCES course(id),
  class_id integer NOT NULL,
  max_capacity integer NOT NULL,
  class_start_date text NOT NULL,
  class_end_date text NOT NULL,
  enrolment_start_date text NOT NULL,
  enrolment_end_date text NOT NULL,
  UNIQUE (course_id, class_id)
);


-- Create Learners, Trainers, Administrators

CREATE TABLE department
(
  id SERIAL PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE learner
(
  id SERIAL PRIMARY KEY,
  email text UNIQUE,
  password text NOT NULL,
  first_name text NOT NULL,
  middle_name text,
  last_name text NOT NULL,
  department_id integer REFERENCES department(id)
);

CREATE TABLE trainer
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  class_id integer REFERENCES class(id),
  UNIQUE(user_id, class_id)
);

CREATE TABLE administrator
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id)
);

create TABLE login_session
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  token text NOT NULL,
  creation_date text NOT NULL,
  expiry_date text NOT NULL
);


-- Create Enrolment and Learner_Course_Completion

CREATE TABLE enrolment
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  class_id integer REFERENCES class(id),
  enrolment_date text NOT NULL,
  is_approved boolean DEFAULT false,
  is_withdrawn boolean DEFAULT false,
  course_progress real DEFAULT '0',
  UNIQUE (user_id, class_id)
);

CREATE TABLE learner_course_completion
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  class_id integer REFERENCES class(id),
  completion_date text NOT NULL,
  UNIQUE (user_id, class_id)
);


-- Create Lesson, Course_Material, Learner_Progress

CREATE TABLE lesson
(
  id SERIAL PRIMARY KEY,
  class_id integer REFERENCES class(id),
  lesson_id integer UNIQUE,
  lesson_order integer,
  UNIQUE (class_id, lesson_id)
);

CREATE TABLE learner_lesson_progress
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  class_id integer REFERENCES class(id),
  lesson_id integer REFERENCES lesson(lesson_id),
  UNIQUE (user_id, class_id, lesson_id)
);

/**
TODO: FOR FUTURE

CREATE TABLE course_material (
  id SERIAL PRIMARY KEY,
  class_id integer REFERENCES class(id),
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
CREATE TABLE question
(
  id SERIAL PRIMARY KEY,
  question text NOT NULL,
  choices text NOT NULL,
  answer text NOT NULL
); 

CREATE TABLE quiz
(
  id SERIAL PRIMARY KEY,
  class_id integer REFERENCES class(id),
  timer integer,
  passing_score_percentage real DEFAULT 0,
  is_graded boolean DEFAULT false
);

CREATE TABLE quiz_ungraded
(
  id SERIAL PRIMARY KEY,
  quiz_id integer REFERENCES quiz(id) UNIQUE,
  lesson_id integer REFERENCES lesson(lesson_id)
);

CREATE TABLE quiz_question_type
(
  id SERIAL PRIMARY KEY,
  question_type text NOT NULL UNIQUE
);

CREATE TABLE quiz_question
(
  id SERIAL PRIMARY KEY,
  quiz_id integer REFERENCES quiz(id) UNIQUE,
  question_type_id integer REFERENCES quiz_question_type(id),
  question_title text NOT NULL
);

CREATE TABLE quiz_question_true_false
(
  id SERIAL PRIMARY KEY,
  question_id integer REFERENCES quiz_question(id) UNIQUE,
  answer_true text NOT NULL,
  answer_false text NOT NULL,
  correct_answer boolean NOT NULL
);

CREATE TABLE quiz_question_mcq_answer
(
  id SERIAL PRIMARY KEY,
  question_id integer REFERENCES quiz_question(id),
  answer text NOT NULL,
  is_correct boolean NOT NULL
);

CREATE TABLE learner_quiz_attempt
(
  id SERIAL PRIMARY KEY,
  user_id integer REFERENCES learner(id),
  quiz_id integer REFERENCES quiz(id),
  time_start numeric NOT NULL
);

CREATE TABLE learner_quiz_attempt_question_answer
(
  id SERIAL PRIMARY KEY,
  learner_quiz_attempt_id integer REFERENCES learner_quiz_attempt,
  question_id integer REFERENCES quiz_question(id),
  answer integer NOT NULL
);


/***
 * INSERT DATABASE CONTENTS
*/

-- DEPARTMENT
INSERT INTO department
  (name)
VALUES
  ('Human Resource and Admin');
INSERT INTO department
  (name)
VALUES
  ('Engineers');

-- LEARNERS
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('admin@lms.com', 'p@ssword', 'Phris', 'Coskitt', 1);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('engineer1@lms.com', 'p@ssword', 'Engineer 1', 'Loh', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('engineer2@lms.com', 'p@ssword', 'Engineer 2', 'Minh', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('engineer3@lms.com', 'p@ssword', 'Engineer 3', 'Loo', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('engineer4@lms.com', 'p@ssword', 'Engineer 4', 'Minh', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('engineer5@lms.com', 'p@ssword', 'Engineer 5', 'Loo', 2);
INSERT INTO learner
  (email, password, first_name, middle_name, last_name, department_id)
VALUES
  ('karen@lms.com', 'p@ssword', 'Karen', 'J.', 'See', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('sami@lms.com', 'p@ssword', 'Sam', 'Willows', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('fred@lms.com', 'p@ssword', 'Fred', 'Weasley', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('george@lms.com', 'p@ssword', 'George', 'Weasley', 2);
INSERT INTO learner
  (email, password, first_name, last_name, department_id)
VALUES
  ('mariah@lms.com', 'p@ssword', 'Mariah', 'Carey', 2);


-- ADMINS
INSERT INTO administrator
  (user_id)
VALUES
  (1);

-- COURSES
INSERT INTO course
  (name, description)
VALUES
  ('Introduction to Programming', 'This course is intended for any student who wishes to gain some programming fundamentals, also known as the building blocks of Information Systems. The course introduces students to fundamental programming concepts and constructs, explains the process of developing a basic software application, and explains the basic concepts of object orientation. The student will experience the implementation of a basic software application. Python, a widely-used, high-level, general-purpose and interactive programming language, is used as the vehicle of exploration in this course.');
INSERT INTO course
  (name, description)
VALUES
  ('Information Systems and Innovation', 'In this course, you will get an overview of fundamental business concepts with an emphasis on the challenges and opportunities that arise from technology and how information systems can be used to create business value and innovations.');
INSERT INTO course
  (name, description)
VALUES
  ('Data Management', 'This course will cover fundamentals of relational database theory, important data management concepts such as data modelling, database design, database implementation in current business information systems, and some basic concepts related to unstructured data.');
INSERT INTO course
  (name, description)
VALUES
  ('Web Application Development I', 'In this course, students be equipped with the knowledge and skill to develop a database-driven web application. PHP will be used as the vehicle of exploration. Other related topics like HTTP, HTML, CSS, Javascript will be covered as well. Students will learn the concepts gradually in the 13 weeks of the semester while building a web application of medium complexity.');
INSERT INTO course
  (name, description)
VALUES
  ('Interaction Design and Prototyping', 'This course introduces fundamental human-computer interaction principles and techniques for designing usable interactive systems. Topics include common methods for gathering user requirements, basic UI and graphics programming techniques, and common evaluation techniques. Hands-on experience with UI prototyping tools will be provided and students will complete a UI design and prototyping project as part of this course.');
INSERT INTO course
  (name, description)
VALUES
  ('Web Application Development II', 'This course is designed to equip students with knowledge and skills to develop well-styled and responsive web applications that provide rich user experiences. Combining with the skills learnt in IS113 course, which focuses on developing database-driven web applications with basic web designs, after this course, the students will be equipped with full stack web development skills, who can build both front-end and back-end software.');
INSERT INTO course
  (name, description)
VALUES
  ('Enterprise Solution Development', 'With the emergence of new technologies and evolution of existing ones, organizations are changing the way they build enterprise solutions. Rather than build monolithic applications, the current emphasis is on building solutions by leveraging existing functionality exposed as services (a.k.a API). This approach to composing solutions using services follows the Service Oriented Architecture (SOA) paradigm, where applications are structured as a collection of loosely coupled services. In this course students will learn how to design and implement enterprise solutions using SOA using enterprise tools. The course will cover topics such as cloud computing, SOA, Enterprise Service Bus (ESB), XML, web services and micro-services architecture.');
INSERT INTO course
  (name, description)
VALUES
  ('Enterprise Solution Management', 'This course explores the elements in the IT ecosystem that is required to support enterprise systems. It is divided into three main areas: maintenance, change and disaster prevention and recovery. Using common tools in the industry for ticketing, automated testing and DevOps, students are given hands-on experience as well as the understanding for robust delivery, efficient change and deep resilience. Teams will be given their own  system environment to maintain and protect. Real world use cases and examples are given to highlight the importance and complexity of managing applications in the enterprise.');
INSERT INTO course
  (name, description)
VALUES
  ('Digital Business - Technologies and Transformation', 'Organizations can develop competitive edge through exploitation of digital technologies namely cloud computing, big data and analytics, mobile networks, social media, and the Internet of Things. By effectively leveraging these technologies they can go beyond boosting efficiency and drive new business models, develop new revenue streams, or drive other material changes that lead to an increase in the top or bottom lines. A number of companies such as Amazon, Netflix, Uber, GE, Nike etc. have successfully managed to transform their business to digital business.');

-- COURSE PREREQUISITE
INSERT INTO course_prerequisite
  (course_id, prerequisite_course_id)
VALUES
  (4, 1);
INSERT INTO course_prerequisite
  (course_id, prerequisite_course_id)
VALUES
  (6, 4);
INSERT INTO course_prerequisite
  (course_id, prerequisite_course_id)
VALUES
  (7, 6);
INSERT INTO course_prerequisite
  (course_id, prerequisite_course_id)
VALUES
  (8, 6);
INSERT INTO course_prerequisite
  (course_id, prerequisite_course_id)
VALUES
  (9, 6);

-- CLASS
-- populate course for trainers
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    1,
    1,
    20,
    '2021-10-05T16:00:00.000Z',
    '2021-10-12T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-05T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    2,
    1,
    20,
    '2021-10-07T16:00:00.000Z',
    '2021-10-06T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-05T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    3,
    1,
    20,
    '2021-10-07T16:00:00.000Z',
    '2021-10-06T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-05T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    4,
    1,
    20,
    '2021-10-07T16:00:00.000Z',
    '2021-10-06T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-05T04:00:00.000Z'
  );

INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    5,
    1,
    20,
    '2021-10-07T16:00:00.000Z',
    '2021-10-06T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-05T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    6,
    3,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-10-21T04:00:00.000Z'
  );

-- classes for course_id 1
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    1,
    2,
    20,
    '2021-11-01T16:00:00.000Z',
    '2021-11-12T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-08T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    1,
    3,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-08T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    1,
    4,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-15T04:00:00.000Z'
  );

-- classes for course_id 2
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    2,
    2,
    20,
    '2021-11-01T16:00:00.000Z',
    '2021-11-12T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-08T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    2,
    3,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-08T04:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    2,
    4,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-15T04:00:00.000Z'
  );

-- classes for course_id 4
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    4,
    2,
    20,
    '2021-11-01T16:00:00.000Z',
    '2021-11-12T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-01T08:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    4,
    3,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-01T08:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    4,
    4,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-14T08:00:00.000Z'
  );

-- classes for course_id 3
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    3,
    2,
    20,
    '2021-11-01T16:00:00.000Z',
    '2021-11-12T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-01T08:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    3,
    3,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-01T08:00:00.000Z'
  );
INSERT INTO class
  (course_id, class_id, max_capacity, class_start_date, class_end_date, enrolment_start_date, enrolment_end_date)
VALUES
  (
    3,
    4,
    20,
    '2021-10-22T16:00:00.000Z',
    '2021-11-05T16:00:00.000Z',
    '2021-10-04T00:00:00.000Z',
    '2021-11-14T08:00:00.000Z'
  );

-- TRAINER
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 1);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 2);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 3);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 4);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 5);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 6);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 7);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 8);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 9);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 10);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 11);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 12);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 13);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 14);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 15);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 16);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 17);
INSERT INTO trainer
  (user_id, class_id)
VALUES
  (2 , 18);


-- Enrolment
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (5, 7, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (6, 7, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (7, 7, '2021-10-04T01:00:00.000Z', false, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (8, 7, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (9, 7, '2021-10-04T01:00:00.000Z', false, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (5, 11, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (6, 11, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (7, 11, '2021-10-04T01:00:00.000Z', false, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (5, 14, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (6, 14, '2021-10-04T01:00:00.000Z', true, false, 0);
INSERT INTO enrolment
  (user_id, class_id, enrolment_date, is_approved, is_withdrawn, course_progress)
VALUES
  (7, 14, '2021-10-04T01:00:00.000Z', false, false, 0);


-- Learner_Course_Completion
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 1, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 2, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 3, '2021-10-12T11:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 4, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 5, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (2, 6, '2021-10-12T11:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 1, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 2, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 3, '2021-10-12T11:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 4, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 5, '2021-10-11T12:00:00.000Z');
INSERT INTO learner_course_completion
  (user_id, class_id, completion_date)
VALUES
  (3, 6, '2021-10-12T11:00:00.000Z');
