-- Initialize database schema for DataBreach Monitor

-- Create database if not exists (this might not be needed in Docker)
-- CREATE DATABASE IF NOT EXISTS databreach;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create initial indexes for better performance
-- (Tables will be created by SQLAlchemy migrations)

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE databreach TO databreach;

-- Create a simple health check function
CREATE OR REPLACE FUNCTION health_check()
RETURNS TEXT AS $$
BEGIN
    RETURN 'Database is healthy at ' || NOW();
END;
$$ LANGUAGE plpgsql;