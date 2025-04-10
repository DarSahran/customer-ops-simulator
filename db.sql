show databases;
drop database customer_ops_simulator;
create DATABASE customer_ops_simulator;

USE customer_ops_simulator;

CREATE TABLE customers (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    industry VARCHAR(100),
    priority_level ENUM('High', 'Medium', 'Low'),
    active BOOLEAN,
    created_at DATETIME
);

CREATE TABLE rules (
    id CHAR(36) PRIMARY KEY,
    customer_id CHAR(36),
    rule_name VARCHAR(100),
    rule_type VARCHAR(100),
    frequency ENUM('hourly', 'daily'),
    status ENUM('active', 'inactive'),
    last_run DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE execution_logs (
    id CHAR(36) PRIMARY KEY,
    rule_id CHAR(36),
    customer_id CHAR(36),
    status ENUM('success', 'failure'),
    output_summary TEXT,
    executed_at DATETIME,
    FOREIGN KEY (rule_id) REFERENCES rules(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE tickets (
    id CHAR(36) PRIMARY KEY,
    customer_id CHAR(36),
    related_rule_id CHAR(36),
    issue_summary TEXT,
    status ENUM('open', 'in_progress', 'resolved'),
    created_at DATETIME,
    resolved_at DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (related_rule_id) REFERENCES rules(id)
);



select * from customers;
select * from rules;
select * from execution_logs;
select * from tickets;



