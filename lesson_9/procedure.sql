CREATE TABLE dq_dg.data_quality_checks_log (
    id SERIAL PRIMARY KEY,
    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    entity_name VARCHAR(255) NOT NULL,
    issue_found BOOLEAN DEFAULT FALSE,
    issue_description TEXT,
    alert_sent BOOLEAN DEFAULT FALSE
);

CREATE OR REPLACE PROCEDURE dq_dg.run_data_quality_checks()
LANGUAGE plpgsql
AS $$
DECLARE
    issue_count INTEGER;
    issue_desc TEXT;
BEGIN
    -- 1. Проверка: customer_id в transactions, которых нет в customers
    WITH trn AS (
        SELECT customer_id, COUNT(1)
        FROM dq_dg.transactions
        WHERE customer_id IS NOT NULL
        GROUP BY customer_id
    ),
    cus AS (
        SELECT id FROM dq_dg.customers
    )
    SELECT COUNT(1) INTO issue_count
    FROM trn t
    LEFT JOIN cus c ON c.id = t.customer_id
    WHERE c.id IS NULL;

    IF issue_count > 0 THEN
        issue_desc := 'Найдены transaction с customer_id, отсутствующим в customers. Количество: ' || issue_count;
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.customer_id references customers.id', TRUE, issue_desc);
    ELSE
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.customer_id references customers.id', FALSE, NULL);
    END IF;

    -- 2. Проверка: cheque_sum >= 500000 (аномально большие чеки)
    SELECT COUNT(1) INTO issue_count
    FROM dq_dg.transactions
    WHERE cheque_sum >= 500000;

    IF issue_count > 0 THEN
        issue_desc := 'Обнаружены чеки на сумму >= 500000. Количество: ' || issue_count;
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.cheque_sum >= 500000', TRUE, issue_desc);
    ELSE
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.cheque_sum >= 500000', FALSE, NULL);
    END IF;

    -- 3. Проверка: расхождение суммы в транзакции и детализации
    WITH td AS (
        SELECT td.id, SUM(td.qnty * p.price) AS ch_sum_td
        FROM dq_dg.transactions_details td
        JOIN dq_dg.products p ON p.id = td.art_id
        GROUP BY td.id
    )
    SELECT COUNT(1) INTO issue_count
    FROM dq_dg.transactions t
    JOIN td ON t.id = td.id
    WHERE td.ch_sum_td <> t.cheque_sum;

    IF issue_count > 0 THEN
        issue_desc := 'Несоответствие cheque_sum в transactions и сумме в transactions_details. Количество: ' || issue_count;
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.cheque_sum vs transactions_details', TRUE, issue_desc);
    ELSE
        INSERT INTO dq_dg.data_quality_checks_log (entity_name, issue_found, issue_description)
        VALUES ('transactions.cheque_sum vs transactions_details', FALSE, NULL);
    END IF;

    COMMIT;
END;
$$;

call dq_dg.run_data_quality_checks()