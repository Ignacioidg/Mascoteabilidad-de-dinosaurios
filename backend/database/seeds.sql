-- ====================================================================
-- PROYECTO: DinoMascota Dashboard
-- MATERIA: Bases de Datos Aplicada - UAI
-- SCRIPT: DML - Inserción de Datos Iniciales (Seeds)
-- ====================================================================

-- 1. Usuarios con contraseña hasheada en SHA-256 con Salt (cuentas verificadas)
INSERT INTO usuarios (username, email, password_hash, salt, nombre_completo, rol, verificado) VALUES
('admin', 'admin@dinomascota.uai', 'sha256$763a3ab98401a0653422e6059cd2b987$2a4e99d6672b011037745f7c5f34316b82a6758f0b05fc471cfdaeca11c901f1', '763a3ab98401a0653422e6059cd2b987', 'Administrador General', 'administrador', 1),
('profesor', 'profesor@uai.edu.ar', 'sha256$8f91a2b3c4d5e6f7a8b9c0d1e2f3a4b5$e155f44c9b165909d996c822209ed63ec8eee6fb0c7759b9e57877b3dbcb6ecd', '8f91a2b3c4d5e6f7a8b9c0d1e2f3a4b5', 'Prof. Titular BD Aplicada', 'docente', 1),
('alumno', 'alumno@alumnos.uai.edu.ar', 'sha256$1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d$967b67ca0cda726aca713104867123bd5a69248835d53b4b139f346f2de26cdb', '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d', 'Estudiante de Sistemas', 'alumno', 1);

-- 2. Períodos Geológicos
INSERT INTO periodos (id_periodo, nombre, era, millones_anios_inicio, millones_anios_fin, clima_predominante, descripcion) VALUES
(1, 'Triásico', 'Mesozoico', 251.9, 201.3, 'Cálido y árido, con vastos desiertos y veranos intensos', 'Aparición de los primeros dinosaurios pequeños y ágiles.'),
(2, 'Jurásico', 'Mesozoico', 201.3, 145.0, 'Cálido y húmedo, con densos bosques de coníferas y helechos', 'Época dorada de los grandes saurópodos y depredadores emblemáticos.'),
(3, 'Cretácico', 'Mesozoico', 145.0, 66.0, 'Templado a cálido, diversificación de plantas con flor', 'Mayor diversidad morfológica y desarrollo de dinosaurios emplumados.');

-- 3. Hábitats
INSERT INTO habitats (id_habitat, nombre, tipo_terreno, superficie_minima_m2, clima, dificultad_adaptacion) VALUES
(1, 'Bosque Templado', 'Arbolado denso con abundante follaje', 150, 'Templado', 'Baja'),
(2, 'Llanura Abierta', 'Praderas y pastizales extensos', 1200, 'Templado-Cálido', 'Baja'),
(3, 'Pantano Húmedo', 'Tierras anegadas, ciénagas y aguas poco profundas', 600, 'Húmedo Tropical', 'Media'),
(4, 'Litoral Costero', 'Playas, acantilados y estuarios marítimos', 400, 'Marítimo Húmedo', 'Media'),
(5, 'Cañón Árido', 'Terreno rocoso con vegetación xerófila', 250, 'Árido y Seco', 'Alta'),
(6, 'Valle Fluvial', 'Riberas de ríos caudalosos y deltas fértiles', 800, 'Subtropical', 'Baja');

-- 4. Dietas
INSERT INTO dietas (id_dieta, tipo, consumo_diario_kg, costo_mensual_usd, nivel_peligro_alimentacion) VALUES
(1, 'Herbívoro Estricto', 45.0, 350.00, 'Bajo'),
(2, 'Carnívoro Depredador', 25.0, 1800.00, 'Mortal'),
(3, 'Piscívoro Especializado', 12.0, 600.00, 'Medio'),
(4, 'Insectívoro / Frugívoro', 1.5, 90.00, 'Bajo'),
(5, 'Omnívoro Adaptable', 8.0, 280.00, 'Medio');

-- 5. Dinosaurios (52 especies completas con URLs de imágenes Wikimedia y datos analíticos)
INSERT INTO dinosaurios (
    nombre, especie, altura_m, longitud_m, peso_kg, velocidad_kmh, agresividad_1_10, 
    inteligencia_1_10, esperanza_vida_anios, espacio_requerido_m2, indice_mascotabilidad, 
    id_periodo, id_habitat, id_dieta, imagen_emoji, imagen_url, observaciones
) VALUES
-- =========================================================================
-- TRIÁSICO (id_periodo = 1) - 14 Especies
-- =========================================================================
('Herrerasaurus', 'Herrerasaurus ischigualastensis', 1.5, 3.0, 250.0, 40.0, 8, 5, 20, 300, 22, 1, 5, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/6/67/Herrerasaurus_use_V2.webp/revision/latest/scale-to-width-down/800?cb=20250615193754', 'Uno de los primeros carnívoros; temperamento impredecible y mordida fuerte.'),
('Eoraptor', 'Eoraptor lunensis', 0.4, 1.0, 10.0, 35.0, 3, 6, 12, 40, 82, 1, 1, 5, '🦎', 'https://static.wikia.nocookie.net/jurassicpark/images/2/23/JPI_Eoraptor.png/revision/latest?cb=20200807195328', 'Tamaño de un perro faldero; adaptable, come semillas e insectos, excelente mascota de jardín.'),
('Plateosaurus', 'Plateosaurus trossingensis', 3.2, 8.0, 4000.0, 20.0, 4, 3, 45, 1500, 35, 1, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/3/39/JPI_Plateosaurus.png/revision/latest?cb=20200825062347', 'Herbívoro dócil pero su inmenso peso puede aplastar la cochera familiar.'),
('Coelophysis', 'Coelophysis bauri', 0.9, 2.5, 25.0, 50.0, 6, 7, 15, 120, 58, 1, 5, 5, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/6/61/JPI_Coelophysis.png/revision/latest/scale-to-width-down/800?cb=20250614115940', 'Muy veloz y curioso; requiere adiestramiento estricto pero es leal.'),
('Marasuchus', 'Marasuchus lilloensis', 0.2, 0.4, 1.2, 28.0, 2, 4, 8, 15, 91, 1, 1, 4, '🦎', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1c/Marasuchus.JPG/330px-Marasuchus.JPG?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail', 'Minúsculo reptil ágil; se alimenta de grillos y frutas, ideal para departamentos amplios.'),
('Staurikosaurus', 'Staurikosaurus pricei', 0.8, 2.0, 30.0, 45.0, 7, 5, 14, 150, 42, 1, 5, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/5/57/JPI_Staurikosaurus.png/revision/latest?cb=20200905040302', 'Depredador ágil del Triásico superior; no apto para convivir con niños ni perros.'),
('Riojasaurus', 'Riojasaurus incertus', 3.0, 10.0, 4500.0, 15.0, 3, 3, 40, 1600, 34, 1, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/e/e6/JPI_Riojasaurus.png/revision/latest?cb=20200819025816', 'Gran prosaurópodo argentino; come abundante forraje, lento pero requiere campo abierto.'),
('Lesothosaurus', 'Lesothosaurus diagnosticus', 0.4, 1.0, 8.0, 38.0, 2, 5, 10, 35, 87, 1, 5, 1, '🦎', 'https://static.wikia.nocookie.net/jurassicpark/images/8/80/JPI_Lesothosaurus.png/revision/latest?cb=20200811172227', 'Herbívoro diminuto, tímido y muy veloz; adora comer lechuga y brotes de jardín.'),
('Mussaurus', 'Mussaurus patagonicus', 0.8, 3.0, 120.0, 22.0, 2, 4, 25, 200, 76, 1, 6, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/0/02/JPI_Mussaurus.png/revision/latest?cb=20200629055247', 'El lagarto ratón; sus crías caben en la palma de la mano, muy tierno y sociable.'),
('Melanorosaurus', 'Melanorosaurus readi', 3.5, 8.0, 3800.0, 18.0, 3, 3, 42, 1400, 36, 1, 2, 1, '🦕', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d0/Melanorosaurus_readi_steveoc.jpg/330px-Melanorosaurus_readi_steveoc.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail', 'Prosaurópodo pesado; tranquilo pero genera problemas de tránsito si sale a pasear.'),
('Pisanosaurus', 'Pisanosaurus mertii', 0.3, 0.9, 5.0, 32.0, 2, 5, 9, 25, 89, 1, 1, 1, '🦎', 'https://static.wikia.nocookie.net/jurassicpark/images/c/ca/JPI_Pisanosaurus.png/revision/latest?cb=20200825044625', 'Herbívoro primitivo pequeño y silencioso; no ladra, no muerde y come césped cortado.'),
('Chindesaurus', 'Chindesaurus bryansmalli', 1.0, 2.4, 50.0, 40.0, 7, 6, 16, 180, 41, 1, 5, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/a/a5/JPI_Chindesaurus.png/revision/latest/scale-to-width-down/800?cb=20250727200323', 'Cazador solitario del desierto triásico; territorial y desconfiado con extraños.'),
('Liliensternus', 'Liliensternus liliensterni', 2.0, 5.1, 130.0, 45.0, 8, 6, 20, 350, 28, 1, 6, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/a/a9/JPI_Liliensternus.png/revision/latest?cb=20200811173423', 'Therópodo estilizado de gran agilidad; mordida rápida y caza nocturna.'),
('Gojirasaurus', 'Gojirasaurus quayi', 2.2, 5.5, 200.0, 38.0, 8, 5, 22, 450, 21, 1, 4, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/6/6d/JPI_Gojirasaurus.webp/revision/latest/scale-to-width-down/800?cb=20260911211854', 'Nombrado en honor a Godzilla; depredador costero de gran apetito y fuerte rugido.'),

-- =========================================================================
-- JURÁSICO (id_periodo = 2) - 18 Especies
-- =========================================================================
('Brachiosaurus', 'Brachiosaurus altithorax', 13.0, 26.0, 35000.0, 15.0, 1, 2, 80, 5000, 18, 2, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/0/00/JWFKBrachiosaurusRender.png/revision/latest?cb=20180427201052', 'Sumamente pacífico, pero comerá toda la arboleda vecinal y bloqueará el tráfico.'),
('Dilophosaurus', 'Dilophosaurus wetherilli', 2.0, 7.0, 400.0, 38.0, 8, 7, 25, 450, 20, 2, 1, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/a/a7/Dilophosaurus_Open_Frills.png/revision/latest/scale-to-width-down/800?cb=20240214114411', 'Territorial y cazador veloz; no escupe veneno real pero muerde severamente.'),
('Stegosaurus', 'Stegosaurus stenops', 4.0, 9.0, 5000.0, 12.0, 3, 2, 50, 1800, 48, 2, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/8/8f/Jurassic_world_fallen_kingdom_stegosaurus_v4_by_sonichedgehog2-dco06sh.png/revision/latest/scale-to-width-down/800?cb=20180928221819', 'Tranquilo y herbívoro, pero su cola con púas (thagomizer) requiere señalización vial.'),
('Allosaurus', 'Allosaurus fragilis', 3.5, 9.5, 2000.0, 42.0, 9, 8, 30, 1200, 8, 2, 1, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/b/bb/AlloRenderDominion.png/revision/latest?cb=20240817200513', 'Súper depredador jurásico; riesgo extremo de comerse a sus propios dueños.'),
('Compsognathus', 'Compsognathus longipes', 0.3, 0.8, 2.5, 40.0, 4, 6, 10, 25, 88, 2, 1, 4, '🦎', 'https://static.wikia.nocookie.net/jurassicpark/images/8/87/Compy_JWR.jpg/revision/latest?cb=20260316020859', 'Del tamaño de una gallina; juguetón, caza roedores e insectos domésticos.'),
('Archaeopteryx', 'Archaeopteryx lithographica', 0.3, 0.5, 0.9, 30.0, 1, 7, 12, 20, 94, 2, 1, 4, '🦜', 'https://static.wikia.nocookie.net/jurassicpark/images/a/a5/JPI_Archaeopteryx.png/revision/latest?cb=20200724230203', 'Fascinante criatura emplumada; dócil, puede posarse en el hombro como un loro exótico.'),
('Camarasaurus', 'Camarasaurus supremus', 7.5, 15.0, 18000.0, 14.0, 2, 2, 60, 3000, 26, 2, 6, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/b/bb/JPI_Camarasaurus.png/revision/latest?cb=20200728000757', 'Saurópodo mediano muy dócil; mantenimiento prohibitivo en forraje.'),
('Ceratosaurus', 'Ceratosaurus nasicornis', 2.2, 6.0, 1000.0, 35.0, 8, 6, 22, 600, 15, 2, 6, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/0/0f/Cerato-sa-urus.webp/revision/latest/scale-to-width-down/800?cb=20220520171342', 'Con cuerno distintivo en el hocico; altamente agresivo cerca del agua.'),
('Diplodocus', 'Diplodocus carnegii', 5.0, 25.0, 15000.0, 18.0, 2, 3, 70, 3500, 25, 2, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/5/59/JPI_Diplodocus.png/revision/latest?cb=20200803185027', 'Cuello y cola larguísimos; apacible pero barre muebles enteros con la cola.'),
('Apatosaurus', 'Apatosaurus ajax', 6.0, 22.0, 22000.0, 16.0, 2, 2, 65, 3800, 23, 2, 3, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/1/13/JWFKApatosaurusRender.png/revision/latest?cb=20180427200403', 'Robusto y dócil como un buey gigante; adora bañarse en el barro.'),
('Kentrosaurus', 'Kentrosaurus aethiopicus', 2.0, 4.5, 1200.0, 16.0, 4, 3, 35, 600, 56, 2, 1, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/2/2c/Kentrosaurus_render.png/revision/latest/scale-to-width-down/800?cb=20240531111723', 'Pariente espinoso del estegosaurio; tamaño manejable pero espinas filosas en los hombros.'),
('Dryosaurus', 'Dryosaurus altus', 1.5, 3.0, 80.0, 45.0, 2, 6, 18, 150, 78, 2, 1, 1, '🦘', 'https://static.wikia.nocookie.net/jurassicpark/images/6/6a/JPI_Dryosaurus.png/revision/latest?cb=20200805063705', 'Bípedo ágil parecido a un canguro herbívoro; no causa daños y es muy juguetón.'),
('Megalosaurus', 'Megalosaurus bucklandii', 3.0, 8.0, 1400.0, 32.0, 9, 6, 25, 800, 12, 2, 4, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/6/63/JPI_Megalosaurus.png/revision/latest?cb=20200817213120', 'El primer dinosaurio nombrado por la ciencia; cazador costero implacable.'),
('Scelidosaurus', 'Scelidosaurus harrisonii', 1.2, 3.8, 300.0, 20.0, 3, 4, 25, 250, 68, 2, 4, 1, '🐢', 'https://static.wikia.nocookie.net/jurassicpark/images/9/90/JPI_Scelidosaurus.png/revision/latest?cb=20200902051507', 'Acorazado temprano costero; excelente mascota guardiana, come algas y pasto.'),
('Cryolophosaurus', 'Cryolophosaurus ellioti', 2.8, 6.5, 600.0, 36.0, 8, 7, 24, 500, 19, 2, 5, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/f/fc/JPI_Cryolophosaurus.png/revision/latest?cb=20200614061821', 'El dinosaurio con cresta estilo Elvis; agresivo y adaptado al frío montañoso.'),
('Torvosaurus', 'Torvosaurus tanneri', 3.5, 10.0, 3000.0, 30.0, 9, 7, 28, 1500, 7, 2, 6, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/d/de/JPI_Torvosaurus.png/revision/latest?cb=20200806225926', 'Depredador gigante con brazos musculosos; incompatible con cualquier hogar.'),
('Mamenchisaurus', 'Mamenchisaurus constructus', 6.0, 26.0, 25000.0, 12.0, 1, 2, 75, 4500, 19, 2, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/9/9f/Jurassic_park_mamenchisaurus_render_1_by_tsilvadino_de76dfk-pre.png/revision/latest/scale-to-width-down/800?cb=20210529023603', 'Posee el cuello más largo de la historia; mirará a través del balcón de un cuarto piso.'),
('Yi qi', 'Yi qi', 0.25, 0.4, 0.4, 32.0, 1, 7, 10, 15, 96, 2, 1, 4, '🦇', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/Yi_qi_fossil.jpg/330px-Yi_qi_fossil.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail', 'Increíble dinosaurio con alas membranosas de murciélago; vuela por la habitación y come polillas.'),

-- =========================================================================
-- CRETÁCICO (id_periodo = 3) - 20 Especies
-- =========================================================================
('Tyrannosaurus rex', 'Tyrannosaurus rex', 4.0, 12.5, 8500.0, 27.0, 10, 8, 30, 3500, 6, 3, 2, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/0/02/Ember_new_render.png/revision/latest/scale-to-width-down/800?cb=20251006213308', 'El rey indiscutido; fuerza de mordida demoledora, incompatible con la vida urbana.'),
('Triceratops', 'Triceratops horridus', 3.0, 8.5, 7000.0, 32.0, 5, 4, 40, 2000, 45, 3, 2, 1, '🦏', 'https://static.wikia.nocookie.net/jurassicpark/images/5/52/Jurassic_world_fallen_kingdom_triceratops_by_sonichedgehog2-dc9dwcu.png/revision/latest?cb=20180427200649', 'Fiel y robusto como un rinoceronte leal; requiere gran patio y cuidado con las embestidas.'),
('Velociraptor', 'Velociraptor mongoliensis', 0.6, 1.8, 15.0, 55.0, 8, 9, 18, 80, 49, 3, 5, 2, '🦅', 'https://static.wikia.nocookie.net/jurassicpark/images/e/e8/Velociraptor_Rebirth.webp/revision/latest/scale-to-width-down/762?cb=20250602211821', 'Muy inteligente y emplumado; abre picaportes pero no debe quedarse solo con niños.'),
('Microraptor', 'Microraptor gui', 0.25, 0.77, 1.0, 30.0, 2, 7, 11, 20, 95, 3, 1, 4, '🦜', 'https://static.wikia.nocookie.net/jurassicpark/images/e/ec/JWA_PressKit_Microraptor.webp/revision/latest?cb=20220912223259', 'Cuatro alas emplumadas, come bichos, planea por la sala; la mejor mascota voladora.'),
('Ankylosaurus', 'Ankylosaurus magniventris', 1.7, 8.0, 6000.0, 10.0, 2, 2, 45, 1500, 52, 3, 2, 1, '🐢', 'https://static.wikia.nocookie.net/jurassicpark/images/c/cc/JWFKAnkylosaurusRender.png/revision/latest?cb=20180427200330', 'Tanque viviente súper pacífico; excelente podadora de césped si no mueves su mazo caudal.'),
('Spinosaurus', 'Spinosaurus aegyptiacus', 5.0, 15.0, 9000.0, 22.0, 9, 7, 35, 4000, 9, 3, 3, 3, '🐊', 'https://static.wikia.nocookie.net/jurassicpark/images/9/9b/Pleaseuseinspino.png/revision/latest/scale-to-width-down/800?cb=20150219013731', 'Colosal amante del agua; vaciará la pileta olímpica y se comerá los peces del acuario.'),
('Pachycephalosaurus', 'Pachycephalosaurus wyomingensis', 1.8, 4.5, 450.0, 24.0, 6, 3, 22, 500, 38, 3, 1, 5, '🐏', 'https://static.wikia.nocookie.net/jurassicpark/images/e/ee/Jurassic_park_pachycephalosaurus_by_camo_flauge-dcfu6qx.png/revision/latest/scale-to-width-down/667?cb=20180709072242', 'Propenso a cabezazos contra portones y paredes cuando se frustra.'),
('Parasaurolophus', 'Parasaurolophus walkeri', 2.8, 9.5, 3000.0, 25.0, 2, 4, 35, 1200, 63, 3, 6, 1, '🎺', 'https://static.wikia.nocookie.net/jurassicpark/images/d/d1/JWD_Parasaurolophus.png/revision/latest/scale-to-width-down/800?cb=20220618082154', 'Produce hermosos sonidos de trompeta con su cresta; muy cariñoso y gregario.'),
('Oviraptor', 'Oviraptor philoceratops', 1.0, 1.6, 35.0, 42.0, 4, 8, 16, 100, 71, 3, 5, 5, '🪶', 'https://static.wikia.nocookie.net/jurassicpark/images/a/a7/Oviraptor_render.png/revision/latest/scale-to-width-down/773?cb=20240531110441', 'Excelente incubador, curioso, come frutas y huevos; requiere juguetes interactivos.'),
('Baryonyx', 'Baryonyx walkeri', 2.5, 7.5, 1700.0, 30.0, 7, 6, 25, 800, 24, 3, 3, 3, '🎣', 'https://static.wikia.nocookie.net/jurassicpark/images/8/8a/1440x651_0012_baryonyx.png/revision/latest?cb=20190703043626', 'Garra gigante para pescar; si le tienes una laguna privada con truchas se calma.'),
('Carnotaurus', 'Carnotaurus sastrei', 3.0, 7.8, 1500.0, 50.0, 9, 6, 22, 900, 14, 3, 2, 2, '🐂', 'https://static.wikia.nocookie.net/jurassicpark/images/b/b9/Jurassic_world_carnotaurus_updated_by_sonichedgehog2-dc377dl.png/revision/latest?cb=20180427200251', 'El toro carnívoro patagónico; brazos diminutos pero aceleración extrema como un bólido.'),
('Argentinosaurus', 'Argentinosaurus huinculensis', 18.0, 35.0, 75000.0, 10.0, 1, 2, 90, 8000, 10, 3, 2, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/f/f3/JPI_Argentinosaurus.png/revision/latest?cb=20200704003634', 'El ser vivo terrestre más pesado; un paso en falso demolerá la cuadra entera.'),
('Giganotosaurus', 'Giganotosaurus carolinii', 4.2, 13.0, 8200.0, 32.0, 10, 7, 30, 3600, 5, 3, 5, 2, '🦖', 'https://static.wikia.nocookie.net/jurassicpark/images/1/1c/Giganotasaurus_Jurassic_World_Dominion.png/revision/latest/scale-to-width-down/800?cb=20220615052318', 'Superdepredador gigante de Neuquén; más largo que el T-Rex y con apetito voraz.'),
('Therizinosaurus', 'Therizinosaurus cheloniformis', 4.5, 10.0, 5000.0, 18.0, 4, 5, 35, 1800, 40, 3, 1, 1, '✂️', 'https://static.wikia.nocookie.net/jurassicpark/images/7/7f/JWD_Therizinosaurus.png/revision/latest/scale-to-width-down/800?cb=20250805163424', 'Garras guadaña de 1 metro; las usa para cortar ramas altas, podador de árboles temible.'),
('Pachyrhinosaurus', 'Pachyrhinosaurus canadensis', 2.5, 6.0, 3000.0, 26.0, 3, 4, 35, 1000, 59, 3, 6, 1, '🦏', 'https://static.wikia.nocookie.net/jurassicpark/images/0/0c/Pachyrhinosaurus_HD.png/revision/latest/scale-to-width-down/800?cb=20240730162623', 'Divertida protuberancia chata en la nariz; empuja objetos pesados y es dócil en manada.'),
('Iguanodon', 'Iguanodon bernissartensis', 3.2, 10.0, 3500.0, 24.0, 2, 5, 38, 1200, 65, 3, 1, 1, '👍', 'https://static.wikia.nocookie.net/jurassicpark/images/c/c6/Iguanodon_render.png/revision/latest/scale-to-width-down/800?cb=20240531104621', 'Famoso por su pulgar en púa; muy amistoso, saluda levantando sus patas delanteras.'),
('Deinonychus', 'Deinonychus antirrhopus', 1.5, 3.4, 75.0, 48.0, 8, 8, 20, 250, 33, 3, 1, 2, '🦅', 'https://static.wikia.nocookie.net/jurassicpark/images/3/38/JPI_Deinonychus.png/revision/latest/scale-to-width-down/800?cb=20250525103834', 'Garra terrible en forma de hoz; ágil, inteligente pero peligroso para personas inexpertas.'),
('Maiasaura', 'Maiasaura peeblesorum', 2.8, 9.0, 2500.0, 28.0, 2, 6, 32, 1100, 72, 3, 2, 1, '🤱', 'https://static.wikia.nocookie.net/jurassicpark/images/2/20/JPI_Maiasaura.png/revision/latest?cb=20200815160308', 'La buena madre reptil; extraordinariamente maternal, cuida y protege a los miembros del hogar.'),
('Gallimimus', 'Gallimimus bullatus', 2.0, 6.0, 450.0, 60.0, 3, 7, 24, 600, 64, 3, 2, 5, '🦤', 'https://static.wikia.nocookie.net/jurassicpark/images/9/9e/GebaRender.png/revision/latest?cb=20251224164022', 'Parecido a un avestruz gigante; come plantas, huevos y frutas, corre más rápido que un auto.'),
('Amargasaurus', 'Amargasaurus cazaui', 3.0, 10.0, 2800.0, 20.0, 2, 4, 35, 1000, 62, 3, 6, 1, '🦕', 'https://static.wikia.nocookie.net/jurassicpark/images/0/06/JPI_Amargasaurus.png/revision/latest?cb=20200704053644', 'Doble fila de espinas en el cuello; bello y exótico, se alimenta tranquilamente a la orilla del río.');
