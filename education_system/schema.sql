-- 角色表
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 用户表
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    real_name TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    contact TEXT,
    status INTEGER DEFAULT 1,  -- 1表示启用，0表示禁用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

-- 专业表
DROP TABLE IF EXISTS majors;
CREATE TABLE majors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    college TEXT NOT NULL,
    duration INTEGER DEFAULT 4
);

-- 教师表
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    id TEXT PRIMARY KEY,  -- 工号
    name TEXT NOT NULL,
    gender TEXT,
    college TEXT,
    title TEXT,
    contact TEXT,
    status TEXT DEFAULT '在职',  -- 教师状态：在职/离职/退休/停职
    user_id INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 班级表
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    major_id INTEGER,
    grade_year INTEGER,
    advisor_id TEXT,
    FOREIGN KEY (major_id) REFERENCES majors (id),
    FOREIGN KEY (advisor_id) REFERENCES teachers (id)
);

-- 学生表
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id TEXT PRIMARY KEY,  -- 学号
    name TEXT NOT NULL,
    gender TEXT,
    birth_date DATE,
    id_card TEXT UNIQUE,
    hometown TEXT,
    enrollment_date DATE,
    major_id INTEGER,
    class_id INTEGER,
    phone TEXT,
    email TEXT,
    address TEXT,
    photo_path TEXT,
    status TEXT DEFAULT '在读',
    user_id INTEGER UNIQUE,
    FOREIGN KEY (major_id) REFERENCES majors (id),
    FOREIGN KEY (class_id) REFERENCES classes (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 课程表
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    course_type TEXT DEFAULT '选修',
    credits REAL NOT NULL,
    hours INTEGER NOT NULL,
    college TEXT,
    description TEXT
);

-- 开课信息表
DROP TABLE IF EXISTS offered_courses;
CREATE TABLE offered_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    academic_year TEXT NOT NULL,
    semester TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    schedule TEXT,
    location TEXT,
    capacity INTEGER DEFAULT 60,
    selected_count INTEGER DEFAULT 0,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
);

-- 选课记录表
DROP TABLE IF EXISTS course_selections;
CREATE TABLE course_selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    offered_course_id INTEGER NOT NULL,
    selection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT '已选',
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (offered_course_id) REFERENCES offered_courses (id)
);

-- 成绩表
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    offered_course_id INTEGER NOT NULL,
    regular_grade REAL,
    exam_grade REAL,
    final_grade REAL,
    gpa REAL,
    input_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_teacher_id TEXT,
    status TEXT DEFAULT '未审核',
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (offered_course_id) REFERENCES offered_courses (id),
    FOREIGN KEY (input_teacher_id) REFERENCES teachers (id)
);

-- 学费表
DROP TABLE IF EXISTS tuitions;
CREATE TABLE tuitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    academic_year TEXT NOT NULL,
    amount REAL NOT NULL,
    paid_amount REAL DEFAULT 0,
    status TEXT DEFAULT '未缴费',
    deadline DATE,
    FOREIGN KEY (student_id) REFERENCES students (id)
);

-- 支付记录表
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tuition_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method TEXT,
    transaction_id TEXT,
    FOREIGN KEY (tuition_id) REFERENCES tuitions (id)
);

-- 注册申请表
DROP TABLE IF EXISTS registration_applications;
CREATE TABLE registration_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_type TEXT NOT NULL,  -- 'student' 或 'teacher'
    name TEXT NOT NULL,
    gender TEXT,
    id_number TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    emergency_contact TEXT,
    emergency_phone TEXT,
    
    -- 学生特有字段
    major_id INTEGER,
    class_id INTEGER,
    high_school TEXT,
    exam_score TEXT,
    guardian_name TEXT,
    guardian_phone TEXT,
    
    -- 教师特有字段
    education_level TEXT,
    graduate_school TEXT,
    major_field TEXT,
    title TEXT,
    department TEXT,
    work_experience TEXT,
    specialties TEXT,
    
    -- 通用字段
    special_notes TEXT,
    status TEXT DEFAULT '待审核',  -- 待审核/已通过/已拒绝
    application_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_time TIMESTAMP,
    reviewer_id TEXT,
    review_comments TEXT,
    
    FOREIGN KEY (major_id) REFERENCES majors (id),
    FOREIGN KEY (class_id) REFERENCES classes (id),
    FOREIGN KEY (reviewer_id) REFERENCES users (username)
);

-- 申请审核记录表
DROP TABLE IF EXISTS application_reviews;
CREATE TABLE application_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    reviewer_id TEXT NOT NULL,
    review_action TEXT NOT NULL,  -- 'approve', 'reject', 'request_info'
    review_comments TEXT,
    review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (application_id) REFERENCES registration_applications (id),
    FOREIGN KEY (reviewer_id) REFERENCES users (username)
);
