-- migrations/001_add_user_id_column.sql

-- Agregar columna user_id a la tabla conversation
ALTER TABLE conversation
ADD COLUMN user_id TEXT;
