USE sqli_lab;

INSERT INTO users (username, password, email) VALUES
('administrator', 'p4ssw0rd@4dm1nFLAG4', 'admin@sqli.lab'),
('carlos', 'c4rl0s_pw', 'carlos@sqli.lab'),
('wiener', 'w13n3r_pw', 'wiener@sqli.lab');

INSERT INTO products (name, category, price) VALUES
('Red Mug', 'Gifts', 9.99),
('Blue Mug', 'Gifts', 9.99),
('Sticker Pack', 'Gifts', 2.49),
('Laptop Sleeve', 'Accessories', 19.90),
('USB-C Cable', 'Accessories', 7.50),
('Hardcover Notebook', 'Office', 12.00),
('Desk Lamp', 'Office', 24.00);

INSERT INTO tracking (tracking_id) VALUES
('abc123'),
('welcome_back'),
('track-001');
