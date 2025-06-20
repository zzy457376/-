-- 出品公司
INSERT INTO Production_Company (production_company_id, name, city) VALUES
(1, '德间书店', '东京'),
(2, '中影集团', '北京'),
(3, 'Columbia Pictures', '洛杉矶');

-- 电影
INSERT INTO Movie (movie_id, title, release_year, duration, synopsis, production_company_id) VALUES
(1, '千与千寻', 2001, 125, '少女千寻误入神灵世界，为救父母而展开冒险。', 1),
(2, '十面埋伏', 2004, 119, '江湖义军与朝廷势力间的爱恨纠葛。', 2),
(3, '肖申克的救赎', 1994, 142, '银行家安迪在监狱中寻找自由与希望。', 3);

-- 导演
INSERT INTO Director (director_id, name, dob) VALUES
(1, '宫崎骏', '1941-01-05'),
(2, '张艺谋', '1950-11-14'),
(3, 'Frank Darabont', '1959-01-28');

-- 电影与导演关系
INSERT INTO Movie_Director (movie_id, director_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- 演员
INSERT INTO Actor (actor_id, name, dob) VALUES
(1, '柊瑠美', '1987-06-01'),
(2, '金城武', '1973-10-11'),
(3, '刘德华', '1961-09-27'),
(4, 'Tim Robbins', '1958-10-16'),
(5, 'Morgan Freeman', '1937-06-01');

-- 角色
INSERT INTO Role (role_id, role_name, actor_id, movie_id) VALUES
(1, '千寻', 1, 1),
(2, '刘捕头', 2, 2),
(3, '金捕头', 3, 2),
(4, 'Andy Dufresne', 4, 3),
(5, 'Red', 5, 3);

-- 类型
INSERT INTO Genre (genre_id, name) VALUES
(1, '动画'),
(2, '剧情'),
(3, '犯罪'),
(4, '武侠');

-- 电影与类型关系
INSERT INTO Movie_Genre (movie_id, genre_id) VALUES
(1, 1),
(2, 4),
(3, 2),
(3, 3);

-- 旁白
INSERT INTO Narration (narration_id, content, actor_id, movie_id) VALUES
(1, '这是一个神奇的世界。', 1, 1),
(2, '江湖恩怨再起。', 2, 2),
(3, 'Hope is a good thing, maybe the best of things.', 5, 3);

