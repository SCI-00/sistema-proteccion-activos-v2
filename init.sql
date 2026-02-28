-- SQL de inicialización
-- Ejecutar después de que las tablas se creen automáticamente

-- Crear organización
INSERT INTO organizaciones (nombre, tipo) 
VALUES ('SCI DE OCCIDENTE', 'Consultoria')
ON CONFLICT DO NOTHING;

-- Crear primer usuario administrador
-- Email: delatorrev0@gmail.com
-- Password: admin123
-- El hash es generado por bcrypt
INSERT INTO usuarios (nombre, email, password_hash, rol, organizacion_id, activo)
VALUES (
    'Victor Manuel De La Torre',
    'delatorrev0@gmail.com',
    '$2b$12$LQv3c1yduCZedY.dQ.1YLOaJOo1BEKfpSr.ZhXkXqM8jKFWgXBr.C',
    'Administrador',
    1,
    true
)
ON CONFLICT (email) DO NOTHING;
