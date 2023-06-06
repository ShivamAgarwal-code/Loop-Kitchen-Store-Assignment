-- DROP TABLE IF REQUIRED -- ---- 
----------------------------------------------- --
DROP TABLE IF EXISTS LK_STORE_STATUS;
DROP TABLE IF EXISTS LK_MENU_HOURS;
DROP TABLE IF EXISTS LK_STORE_TIMEZONES;
------------------------------------------------- --
-- TABLES CREATION -- --
------------------------------------------------- --
CREATE TABLE LK_STORE_STATUS (
    store_id INTEGER NOT NULL,
    timestamp_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK (status = 'active' OR status = 'inactive')
);
------------------------------------------------- --

CREATE TABLE LK_MENU_HOURS (
    store_id INTEGER NOT NULL,
    day INTEGER NOT NULL CHECK (day >= 0 AND day <= 6),
    start_time_local TEXT DEFAULT '00:00:00' NOT NULL,
    end_time_local TEXT DEFAULT '23:59:59' NOT NULL
);
------------------------------------------------- --

CREATE TABLE LK_STORE_TIMEZONES (
    store_id INTEGER PRIMARY KEY,
    timezone_str TEXT DEFAULT 'America/Chicago' NOT NULL
);
------------------------------------------------- --
-- INSERTION FOR STORE 1 BEGINS
------------------------------------------------- --

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 12:09:39.388884 UTC',
    'active'
)


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 01:09:39.388884 UTC',
    'inactive'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 02:09:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 03:09:39.388884 UTC',
    'active'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 17:45:39.388884 UTC',
    'active'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 17:50:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 17:55:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 14:45:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 15:01:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 15:15:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 15:30:39.388884 UTC',
    'active'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 19:55:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-01 16:55:39.388884 UTC',
    'active'
);



INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-03 09:54:20.850779 UTC',
    'active'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-03 09:55:20.850779 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.41953794191982E+018,
    '2023-06-03 09:57:20.850779 UTC',
    'inactive'
);
------------------------------------------------- --

INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    0,
    '00:00:00',
    '00:10:00'
);
INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    1,
    '12:00:00',
    '22:00:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    2,
    '12:00:00',
    '22:00:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    3,
    '17:00:00',
    '23:59:00'
);



INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    4,
    '13:00:00',
    '21:59:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    5,
    '00:00:00',
    '23:59:00'
);


INSERT INTO LK_MENU_HOURS VALUES(
    8.41953794191982E+018,
    6,
    '00:00:00',
    '22:00:00'
);

------------------------------------------------- --

INSERT INTO LK_STORE_TIMEZONES VALUES (
    8.41953794191982E+018,
    'Asia/Beirut'
);
------------------------------------------------- --

------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------

-- INSERTION FOR STORE 2 --------------------------- --

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 12:09:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 01:09:39.388884 UTC',
    'inactive'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 02:09:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 03:09:39.388884 UTC',
    'active'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 17:45:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 17:50:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 17:55:39.388884 UTC',
    'active'
);




INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 14:45:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 15:01:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 15:15:39.388884 UTC',
    'inactive'
);

INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-01 15:30:39.388884 UTC',
    'active'
);


INSERT INTO LK_STORE_STATUS VALUES(
    8.37746568845657E+018,
    '2023-06-02 13:45:39.388884 UTC',
    'active'
);

------------------------------------------------- --

INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    0,
    '00:00:00',
    '00:10:00'
);
INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    1,
    '00:00:00',
    '22:00:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    2,
    '00:00:00',
    '22:00:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    3,
    '00:00:00',
    '23:59:00'
);



INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    4,
    '00:00:00',
    '21:59:00'
);

INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    5,
    '00:00:00',
    '23:59:00'
);


INSERT INTO LK_MENU_HOURS VALUES(
    8.37746568845657E+018,
    6,
    '00:00:00',
    '22:00:00'
);

------------------------------------------------- --

INSERT INTO LK_STORE_TIMEZONES VALUES (
    8.37746568845657E+018,
    'America/Los_Angeles'
);
------------------------------------------------- --


