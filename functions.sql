-- 1. Кестені құру
CREATE TABLE IF NOT EXISTS phonebook1 (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    phone_number VARCHAR(255)
);

-- 2. Тесттік деректер
INSERT INTO phonebook1 (username, phone_number)
VALUES
  ('Tomiris', '123456789'),
  ('John Doe', '987654321'),
  ('Alice Smith', '5556667787');

-- 3. Іздеу функциясы: аты не телефон нөмірі бойынша
CREATE OR REPLACE FUNCTION search_records(pattern TEXT)
RETURNS TABLE(user_id INT, username VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.user_id, p.username, p.phone_number
    FROM phonebook1 p
    WHERE p.username ILIKE '%' || pattern || '%'
       OR p.phone_number LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 4. Жаңа қолданушы қосу немесе жаңарту (бар болса)
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook1 WHERE username = p_name) THEN
        UPDATE phonebook1
        SET phone_number = p_phone
        WHERE username = p_name;
    ELSE
        INSERT INTO phonebook1 (username, phone_number)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 5. Бірнеше қолданушыны қосу (тізім арқылы), телефон дұрыстығын тексеру
CREATE OR REPLACE PROCEDURE insert_multiple_users(user_list TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    entry TEXT;
    name TEXT;
    phone TEXT;
    incorrect_data TEXT[] := ARRAY[]::TEXT[];
BEGIN
    FOREACH entry IN ARRAY user_list
    LOOP
        name := split_part(entry, ',', 1);
        phone := split_part(entry, ',', 2);

        -- Телефон нөмірін тексеру
        IF phone ~ '^\+?[0-9]{10,15}$' THEN
            CALL insert_or_update_user(name, phone);
        ELSE
            incorrect_data := array_append(incorrect_data, entry);
        END IF;
    END LOOP;

    -- Қате деректер жайлы хабарлау
    IF array_length(incorrect_data, 1) > 0 THEN
        RAISE NOTICE 'Қате деректер: %', incorrect_data;
    END IF;
END;
$$;

-- 6. Пайдаланушыларды limit және offset арқылы көру (pagination)
CREATE OR REPLACE FUNCTION get_users_paginated(limit_count INT, offset_count INT)
RETURNS TABLE(user_id INT, username TEXT, phone_number TEXT)
LANGUAGE SQL
AS $$
    SELECT p.user_id, p.username, p.phone_number
    FROM phonebook1 p
    ORDER BY p.user_id
    LIMIT limit_count OFFSET offset_count;
$$;

-- 7. Аты немесе телефон арқылы қолданушыны жою
CREATE OR REPLACE PROCEDURE delete_user_by_name_or_phone(input TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF input ~ '^\D+$' THEN
        DELETE FROM phonebook1
        WHERE username = input;
    ELSIF input ~ '^\+?[0-9]{10,15}$' THEN
        DELETE FROM phonebook1
        WHERE phone_number = input;
    ELSE
        RAISE NOTICE 'Қате енгізілген дерек!';
    END IF;
END;
$$;

-- 🔹 Тесттер:
-- Іздеу:
SELECT * FROM search_records('Tom');

-- Қосу немесе жаңарту:
CALL insert_or_update_user('Naruto Uzumaki', '87001234567');

-- Бірнеше қолданушы:
CALL insert_multiple_users(ARRAY['Sasuke Uchiha,87001112233', 'Sakura Haruno,invalidphone']);

-- Пагинация:
SELECT * FROM get_users_paginated(2, 0);

-- Жою:
CALL delete_user_by_name_or_phone('Naruto Uzumaki');
