
# Database Design

## Overview

The Manufacturing Data Platform uses PostgreSQL
as its operational database and initial data source.

The database contains five reference tables.

## Tables

### production_lines

Stores manufacturing production lines.

Primary Key: line_id

Unique business key: line_code

### machines

Stores machine information and their
production line assignments.

Primary Key: machine_id

Foreign Key: line_id

### products

Stores product information and ideal cycle times.

Primary Key: product_id

### shifts

Stores factory shift definitions.

Primary Key: shift_id

### operators

Stores operator information.

Primary Key: operator_id

## Relationships

- One production line can contain multiple machines.
- Every machine belongs to one production line.
- Products are independent reference entities.
- Shifts are independent reference entities.
- Operators are independent reference entities.

## Data Integrity

The database uses:

- Primary keys
- Foreign keys
- Unique constraints
- Not null constraints
- Check constraints
- Indexes

## Technology

- PostgreSQL 16
- Docker Compose
- Python 3
- Psycopg 3
