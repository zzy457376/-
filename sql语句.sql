-- 创建出品公司表
CREATE TABLE Production_Company (
    production_company_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL
);

-- 创建电影表
CREATE TABLE Movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    duration INT,  -- 时长，单位为分钟
    synopsis TEXT,
    production_company_id INT,
    FOREIGN KEY (production_company_id) REFERENCES Production_Company(production_company_id) ON DELETE SET NULL
);

-- 创建导演表
CREATE TABLE Director (
    director_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE
);

-- 创建演员表
CREATE TABLE Actor (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE
);

-- 创建电影类别表
CREATE TABLE Genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- 创建电影与类别的关联表（多对多关系）
CREATE TABLE Movie_Genre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id) ON DELETE CASCADE
);

-- 创建电影与导演的关联表（多对多关系）
CREATE TABLE Movie_Director (
    movie_id INT,
    director_id INT,
    PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (director_id) REFERENCES Director(director_id) ON DELETE CASCADE
);

-- 创建角色表（多对多关系，通过电影与演员的关系）
CREATE TABLE Role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL,
    actor_id INT,
    movie_id INT,
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);

-- 创建旁白表（一对多关系，电影与旁白）
CREATE TABLE Narration (
    narration_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    actor_id INT,
    movie_id INT,
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id) ON DELETE SET NULL,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);
