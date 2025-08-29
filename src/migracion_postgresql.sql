-- =====================================================
-- MIGRACIÓN DE PREGUNTAS DE ENTREVISTA
-- =====================================================
-- Generado: 2025-08-29 14:50:36
-- Origen: ../preguntas_entrevista.db
-- Total registros: 40
-- =====================================================

-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS preguntas (
    id SERIAL PRIMARY KEY,
    habilidad VARCHAR(100) NOT NULL,
    pregunta TEXT NOT NULL,
    tipo VARCHAR(50) DEFAULT 'general',
    nivel VARCHAR(50) DEFAULT 'intermedio',
    categoria VARCHAR(50) DEFAULT 'tecnica',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_pregunta UNIQUE(habilidad, pregunta)
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_habilidad ON preguntas(habilidad);
CREATE INDEX IF NOT EXISTS idx_nivel ON preguntas(nivel);
CREATE INDEX IF NOT EXISTS idx_tipo ON preguntas(tipo);
CREATE INDEX IF NOT EXISTS idx_full_search ON preguntas USING gin(to_tsvector('spanish', pregunta));

-- Opcional: Limpiar datos existentes
-- DELETE FROM preguntas;

-- Iniciar transacción para inserción segura
BEGIN;

-- ===============================
-- HABILIDAD: DOCKER
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Docker', 'Explica qué son los volumes en Docker', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Docker', '¿Cuál es la diferencia entre una imagen y un contenedor?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Docker', '¿Cómo manejas las variables de entorno en Docker?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Docker', '¿Qué es Docker Compose y cuándo lo usarías?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Docker', '¿Qué es un Dockerfile y cuáles son sus principales instrucciones?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total Docker: 5 preguntas

-- ===============================
-- HABILIDAD: GIT
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Git', 'Explica qué son las ramas (branches) y cómo las usas', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Git', '¿Cuál es la diferencia entre merge y rebase?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Git', '¿Cómo manejas un repositorio con múltiples colaboradores?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Git', '¿Cómo resuelves conflictos en Git?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Git', '¿Qué comandos usas para deshacer cambios en Git?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total Git: 5 preguntas

-- ===============================
-- HABILIDAD: JAVA
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Java', 'Explica el concepto de polimorfismo en Java', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Java', 'Explica la diferencia entre String, StringBuilder y StringBuffer', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Java', '¿Cuál es la diferencia entre abstract class e interface?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Java', '¿Cómo funciona el Garbage Collector en Java?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Java', '¿Qué son las Collections y cuáles son las más importantes?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total Java: 5 preguntas

-- ===============================
-- HABILIDAD: JAVASCRIPT
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('JavaScript', 'Describe las diferencias entre == y === en JavaScript', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('JavaScript', 'Explica el concepto de closures en JavaScript', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('JavaScript', '¿Cuál es la diferencia entre var, let y const?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('JavaScript', '¿Cómo funciona el hoisting en JavaScript?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('JavaScript', '¿Qué es el Event Loop y cómo funciona?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total JavaScript: 5 preguntas

-- ===============================
-- HABILIDAD: NODE.JS
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Node.js', 'Explica qué son los middlewares en Express', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Node.js', '¿Cuál es la diferencia entre require() e import?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Node.js', '¿Cómo manejas operaciones asíncronas en Node.js?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Node.js', '¿Qué es el Event Loop en Node.js?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Node.js', '¿Qué es npm y cómo gestionas las dependencias?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total Node.js: 5 preguntas

-- ===============================
-- HABILIDAD: PYTHON
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Python', 'Describe la diferencia entre métodos de clase y métodos estáticos', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Python', 'Explica el concepto de decoradores en Python y da un ejemplo', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Python', '¿Cuáles son las diferencias entre listas y tuplas en Python?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Python', '¿Cómo manejas las excepciones en Python?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('Python', '¿Qué son los generadores y cuándo los usarías?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total Python: 5 preguntas

-- ===============================
-- HABILIDAD: REACT
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('React', 'Explica cómo funciona el Virtual DOM', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('React', 'Explica el ciclo de vida de un componente React', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('React', '¿Cuál es la diferencia entre componentes funcionales y de clase?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('React', '¿Cómo manejas el estado en una aplicación React compleja?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('React', '¿Qué son los Hooks y cuáles son los más comunes?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total React: 5 preguntas

-- ===============================
-- HABILIDAD: SQL
-- ===============================

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('SQL', 'Explica la diferencia entre índices clustered y non-clustered', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('SQL', '¿Cuál es la diferencia entre INNER JOIN y LEFT JOIN?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('SQL', '¿Cómo optimizarías una consulta SQL lenta?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('SQL', '¿Qué es la normalización de bases de datos?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES
('SQL', '¿Qué son las transacciones y cuáles son sus propiedades ACID?', 'general', 'intermedio', 'tecnica')
ON CONFLICT (habilidad, pregunta) DO NOTHING;

-- Total SQL: 5 preguntas

-- Confirmar transacción
COMMIT;

-- =====================================================
-- VERIFICACIÓN Y ESTADÍSTICAS
-- =====================================================

-- Contar registros insertados
SELECT COUNT(*) as total_preguntas FROM preguntas;

-- Preguntas por habilidad
SELECT habilidad, COUNT(*) as total
FROM preguntas
GROUP BY habilidad
ORDER BY total DESC;

-- Preguntas por nivel
SELECT nivel, COUNT(*) as total
FROM preguntas
GROUP BY nivel
ORDER BY total DESC;

-- Total de INSERT statements generados: 40
-- Archivo generado: 2025-08-29 14:50:36
