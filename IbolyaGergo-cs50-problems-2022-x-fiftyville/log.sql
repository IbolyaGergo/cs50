-- Keep a log of any SQL queries you execute as you solve the mystery.
-- id = 295, 10:15am, 3 witness, bakery
-- Looking for interviews, where bakery is mentioned
--SELECT transcript FROM interviews WHERE transcript LIKE "%bakery%";

--SELECT * FROM bakery_security_logsWHERE license_plateIN (SELECT license_plate FROM bakery_security_logs
--WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26 AND activity = "exit") AND activity = "entrance";

-- SELECT *FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8;
-- id = 36 from Fiftyville REgional to LaGuardia NYCity
-- SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw");
-- earliest flight tomorrow on 29th of July, other person purchase the ticket
SELECT name
FROM people
WHERE passport_number IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36)
AND
-- whitin 10 minutes the thie drove away, security footage from bakery parking lot around 10:15am
    license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26 AND activity = "exit")
AND
-- earlier that morning, thief by ATM on Leggett Street
    id IN
        (SELECT person_id
        FROM bank_accounts
        WHERE account_number IN
            (SELECT account_number
            FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"))
-- after the thief left, call < 1 min
AND
    phone_number IN
        (SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)

        ;