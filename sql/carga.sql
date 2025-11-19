SET DEFINE OFF

-- =============== ACESSO ===================

INSERT INTO T_NRON_ACESSO VALUES (1, 'FUNCIONARIO', 'Acesso padrão do funcionário');
INSERT INTO T_NRON_ACESSO VALUES (2, 'GESTOR', 'Acesso de gestor');
INSERT INTO T_NRON_ACESSO VALUES (3, 'RH_CLEVEL', 'Acesso estratégico de RH');
INSERT INTO T_NRON_ACESSO VALUES (4, 'OPERACAO', 'Acesso para times operacionais');
INSERT INTO T_NRON_ACESSO VALUES (5, 'COMERCIAL', 'Acesso focado em vendas');
INSERT INTO T_NRON_ACESSO VALUES (6, 'MARKETING', 'Acesso de marketing e comunicação');
INSERT INTO T_NRON_ACESSO VALUES (7, 'DIRETORIA', 'Acesso executivo');
INSERT INTO T_NRON_ACESSO VALUES (8, 'ANALISTA', 'Acesso analítico com relatórios');
INSERT INTO T_NRON_ACESSO VALUES (9, 'TECHLEAD', 'Acesso técnico avançado');
INSERT INTO T_NRON_ACESSO VALUES (10, 'SUPORTE', 'Acesso voltado a suporte');
INSERT INTO T_NRON_ACESSO VALUES (11, 'ESTAGIARIO', 'Acesso limitado para estagiários');
INSERT INTO T_NRON_ACESSO VALUES (12, 'CONSULTOR', 'Acesso para consultores externos');


-- =============== DEPARTAMENTO ===================

INSERT INTO T_NRON_DEPARTAMENTO VALUES (1, 'Tecnologia', 'Área de TI');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (2, 'Recursos Humanos', 'Área de RH');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (3, 'Financeiro', 'Área financeira');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (4, 'Marketing', 'Comunicação e marketing');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (5, 'Comercial', 'Vendas e negócios');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (6, 'Operações', 'Processos operacionais');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (7, 'Jurídico', 'Área jurídica');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (8, 'Logística', 'Distribuição e transporte');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (9, 'Suporte', 'Atendimento interno');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (10, 'Administração', 'Administração geral');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (11, 'Pesquisa & Desenvolvimento', 'Inovação e novos produtos');
INSERT INTO T_NRON_DEPARTAMENTO VALUES (12, 'Experiência do Cliente', 'Customer experience e NPS');


-- =============== USUARIO ===================

INSERT INTO T_NRON_USUARIO VALUES (1,'Ana Clara','ana.clara@corp.com','HASH001','A',TRUNC(SYSDATE) - 90,1,1);
INSERT INTO T_NRON_USUARIO VALUES (2,'Bruno Silva','bruno.silva@corp.com','HASH002','A',TRUNC(SYSDATE) - 88,9,1);
INSERT INTO T_NRON_USUARIO VALUES (3,'Caio Nunes','caio.nunes@corp.com','HASH003','I',TRUNC(SYSDATE) - 85,1,1);
INSERT INTO T_NRON_USUARIO VALUES (4,'Daniela Costa','daniela.costa@corp.com','HASH004','A',TRUNC(SYSDATE) - 80,2,2);
INSERT INTO T_NRON_USUARIO VALUES (5,'Elaine Freitas','elaine.freitas@corp.com','HASH005','A',TRUNC(SYSDATE) - 78,3,2);
INSERT INTO T_NRON_USUARIO VALUES (6,'Fabio Mendes','fabio.mendes@corp.com','HASH006','I',TRUNC(SYSDATE) - 75,11,2);
INSERT INTO T_NRON_USUARIO VALUES (7,'Gabriela Souza','gabriela.souza@corp.com','HASH007','A',TRUNC(SYSDATE) - 70,5,3);
INSERT INTO T_NRON_USUARIO VALUES (8,'Henrique Prado','henrique.prado@corp.com','HASH008','A',TRUNC(SYSDATE) - 65,7,3);
INSERT INTO T_NRON_USUARIO VALUES (9,'Isabela Tavares','isabela.tavares@corp.com','HASH009','A',TRUNC(SYSDATE) - 60,5,3);
INSERT INTO T_NRON_USUARIO VALUES (10,'Joao Ricardo','joao.ricardo@corp.com','HASH010','A',TRUNC(SYSDATE) - 55,4,4);
INSERT INTO T_NRON_USUARIO VALUES (11,'Karen Dias','karen.dias@corp.com','HASH011','A',TRUNC(SYSDATE) - 50,6,4);
INSERT INTO T_NRON_USUARIO VALUES (12,'Leonardo Braga','leonardo.braga@corp.com','HASH012','I',TRUNC(SYSDATE) - 48,4,4);
INSERT INTO T_NRON_USUARIO VALUES (13,'Marina Lopes','marina.lopes@corp.com','HASH013','A',TRUNC(SYSDATE) - 45,5,5);
INSERT INTO T_NRON_USUARIO VALUES (14,'Natan Silva','natan.silva@corp.com','HASH014','A',TRUNC(SYSDATE) - 42,6,5);
INSERT INTO T_NRON_USUARIO VALUES (15,'Olivia Costa','olivia.costa@corp.com','HASH015','A',TRUNC(SYSDATE) - 40,5,5);
INSERT INTO T_NRON_USUARIO VALUES (16,'Paulo Rezende','paulo.rezende@corp.com','HASH016','A',TRUNC(SYSDATE) - 37,4,6);
INSERT INTO T_NRON_USUARIO VALUES (17,'Queila Andrade','queila.andrade@corp.com','HASH017','A',TRUNC(SYSDATE) - 34,1,6);
INSERT INTO T_NRON_USUARIO VALUES (18,'Rafael Mota','rafael.mota@corp.com','HASH018','I',TRUNC(SYSDATE) - 33,8,6);
INSERT INTO T_NRON_USUARIO VALUES (19,'Sara Diniz','sara.diniz@corp.com','HASH019','A',TRUNC(SYSDATE) - 30,7,7);
INSERT INTO T_NRON_USUARIO VALUES (20,'Thiago Castro','thiago.castro@corp.com','HASH020','A',TRUNC(SYSDATE) - 28,7,7);
INSERT INTO T_NRON_USUARIO VALUES (21,'Ursula Porto','ursula.porto@corp.com','HASH021','A',TRUNC(SYSDATE) - 27,5,7);
INSERT INTO T_NRON_USUARIO VALUES (22,'Vicente Amaral','vicente.amaral@corp.com','HASH022','A',TRUNC(SYSDATE) - 24,8,8);
INSERT INTO T_NRON_USUARIO VALUES (23,'Wesley Teixeira','wesley.teixeira@corp.com','HASH023','A',TRUNC(SYSDATE) - 22,10,8);
INSERT INTO T_NRON_USUARIO VALUES (24,'Ximena Rocha','ximena.rocha@corp.com','HASH024','I',TRUNC(SYSDATE) - 20,4,8);
INSERT INTO T_NRON_USUARIO VALUES (25,'Yago Martins','yago.martins@corp.com','HASH025','A',TRUNC(SYSDATE) - 18,5,9);
INSERT INTO T_NRON_USUARIO VALUES (26,'Zaira Lima','zaira.lima@corp.com','HASH026','A',TRUNC(SYSDATE) - 15,5,9);
INSERT INTO T_NRON_USUARIO VALUES (27,'Arthur Barros','arthur.barros@corp.com','HASH027','A',TRUNC(SYSDATE) - 14,12,9);
INSERT INTO T_NRON_USUARIO VALUES (28,'Bianca Furtado','bianca.furtado@corp.com','HASH028','A',TRUNC(SYSDATE) - 12,4,10);
INSERT INTO T_NRON_USUARIO VALUES (29,'Carlos Pinto','carlos.pinto@corp.com','HASH029','I',TRUNC(SYSDATE) - 10,4,10);
INSERT INTO T_NRON_USUARIO VALUES (30,'Debora Seabra','debora.seabra@corp.com','HASH030','A',TRUNC(SYSDATE) - 9,5,10);
INSERT INTO T_NRON_USUARIO VALUES (31,'Eduardo Pires','eduardo.pires@corp.com','HASH031','A',TRUNC(SYSDATE) - 7,8,11);
INSERT INTO T_NRON_USUARIO VALUES (32,'Fernanda Luz','fernanda.luz@corp.com','HASH032','A',TRUNC(SYSDATE) - 6,9,11);
INSERT INTO T_NRON_USUARIO VALUES (33,'Guilherme Porto','guilherme.porto@corp.com','HASH033','A',TRUNC(SYSDATE) - 5,7,11);
INSERT INTO T_NRON_USUARIO VALUES (34,'Helena Ramos','helena.ramos@corp.com','HASH034','A',TRUNC(SYSDATE) - 4,5,12);
INSERT INTO T_NRON_USUARIO VALUES (35,'Igor Almeida','igor.almeida@corp.com','HASH035','A',TRUNC(SYSDATE) - 3,6,12);
INSERT INTO T_NRON_USUARIO VALUES (36,'Juliana Prado','juliana.prado@corp.com','HASH036','A',TRUNC(SYSDATE) - 2,3,12);


-- =============== CATEGORIA EMOCAO  ===================

INSERT INTO T_NRON_CATG_EMOCAO VALUES (1, 'POSITIVA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (2, 'NEGATIVA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (3, 'NEUTRA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (4, 'ANSIOSA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (5, 'SERENA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (6, 'ENTUSIASTA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (7, 'MOTIVACIONAL');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (8, 'DESGASTE');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (9, 'OTIMISTA');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (10, 'RESILIENTE');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (11, 'TENSO');
INSERT INTO T_NRON_CATG_EMOCAO VALUES (12, 'GRATIDAO');


-- =============== EMOCAO ===================

INSERT INTO T_NRON_EMOCAO VALUES (1, 'Feliz', '#FFF000', 1);
INSERT INTO T_NRON_EMOCAO VALUES (2, 'Triste', '#0000FF', 2);
INSERT INTO T_NRON_EMOCAO VALUES (3, 'Ansioso', '#FF6600', 4);
INSERT INTO T_NRON_EMOCAO VALUES (4, 'Calmo', '#00FFAA', 5);
INSERT INTO T_NRON_EMOCAO VALUES (5, 'Motivado', '#FFD700', 7);
INSERT INTO T_NRON_EMOCAO VALUES (6, 'Desanimado', '#5555FF', 8);
INSERT INTO T_NRON_EMOCAO VALUES (7, 'Neutro', '#CCCCCC', 3);
INSERT INTO T_NRON_EMOCAO VALUES (8, 'Empolgado', '#FFAA00', 6);
INSERT INTO T_NRON_EMOCAO VALUES (9, 'Cansado', '#8888AA', 8);
INSERT INTO T_NRON_EMOCAO VALUES (10, 'Esperançoso', '#88FF88', 9);
INSERT INTO T_NRON_EMOCAO VALUES (11, 'Estressado', '#FF3333', 11);
INSERT INTO T_NRON_EMOCAO VALUES (12, 'Sereno', '#66FFCC', 5);
INSERT INTO T_NRON_EMOCAO VALUES (13, 'Grato', '#FFE4B5', 12);
INSERT INTO T_NRON_EMOCAO VALUES (14, 'Frustrado', '#993366', 2);
INSERT INTO T_NRON_EMOCAO VALUES (15, 'Animado', '#FFBB33', 6);
INSERT INTO T_NRON_EMOCAO VALUES (16, 'Confiante', '#B0FFB0', 9);
INSERT INTO T_NRON_EMOCAO VALUES (17, 'Irritado', '#FF4444', 11);
INSERT INTO T_NRON_EMOCAO VALUES (18, 'Sobrecarregado', '#9999CC', 8);
INSERT INTO T_NRON_EMOCAO VALUES (19, 'Orgulhoso', '#FFFACD', 1);
INSERT INTO T_NRON_EMOCAO VALUES (20, 'Aliviado', '#CCFFEE', 5);
INSERT INTO T_NRON_EMOCAO VALUES (21, 'Curioso', '#FFEE99', 6);
INSERT INTO T_NRON_EMOCAO VALUES (22, 'Inseguro', '#9966CC', 2);
INSERT INTO T_NRON_EMOCAO VALUES (23, 'Inspirado', '#FFE066', 7);
INSERT INTO T_NRON_EMOCAO VALUES (24, 'Apreensivo', '#FF9966', 4);


-- =============== REGISTRO EMOCAO ===================

INSERT INTO T_NRON_REGIST_EMOCAO VALUES (1, 62.00, 'Registro emocional do colaborador Ana Clara', SYSDATE - 1/24, 1);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (2, 69.00, 'Registro emocional do colaborador Bruno Silva', SYSDATE - 2/24, 8);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (3, 76.00, 'Registro emocional do colaborador Caio Nunes', SYSDATE - 3/24, 11);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (4, 83.00, 'Registro emocional do colaborador Daniela Costa', SYSDATE - 4/24, 4);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (5, 90.00, 'Registro emocional do colaborador Elaine Freitas', SYSDATE - 5/24, 10);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (6, 97.00, 'Registro emocional do colaborador Fabio Mendes', SYSDATE - 6/24, 18);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (7, 59.00, 'Registro emocional do colaborador Gabriela Souza', SYSDATE - 7/24, 5);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (8, 66.00, 'Registro emocional do colaborador Henrique Prado', SYSDATE - 8/24, 24);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (9, 73.00, 'Registro emocional do colaborador Isabela Tavares', SYSDATE - 9/24, 2);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (10, 80.00, 'Registro emocional do colaborador Joao Ricardo', SYSDATE - 10/24, 15);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (11, 87.00, 'Registro emocional do colaborador Karen Dias', SYSDATE - 11/24, 13);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (12, 94.00, 'Registro emocional do colaborador Leonardo Braga', SYSDATE - 12/24, 17);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (13, 56.00, 'Registro emocional do colaborador Marina Lopes', SYSDATE - 13/24, 9);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (14, 63.00, 'Registro emocional do colaborador Natan Silva', SYSDATE - 14/24, 16);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (15, 70.00, 'Registro emocional do colaborador Olivia Costa', SYSDATE - 15/24, 6);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (16, 77.00, 'Registro emocional do colaborador Paulo Rezende', SYSDATE - 16/24, 20);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (17, 84.00, 'Registro emocional do colaborador Queila Andrade', SYSDATE - 17/24, 14);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (18, 91.00, 'Registro emocional do colaborador Rafael Mota', SYSDATE - 18/24, 23);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (19, 98.00, 'Registro emocional do colaborador Sara Diniz', SYSDATE - 19/24, 3);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (20, 60.00, 'Registro emocional do colaborador Thiago Castro', SYSDATE - 20/24, 21);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (21, 67.00, 'Registro emocional do colaborador Ursula Porto', SYSDATE - 21/24, 12);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (22, 74.00, 'Registro emocional do colaborador Vicente Amaral', SYSDATE - 22/24, 19);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (23, 81.00, 'Registro emocional do colaborador Wesley Teixeira', SYSDATE - 23/24, 22);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (24, 88.00, 'Registro emocional do colaborador Ximena Rocha', SYSDATE - 24/24, 7);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (25, 95.00, 'Registro emocional do colaborador Yago Martins', SYSDATE - 25/24, 1);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (26, 57.00, 'Registro emocional do colaborador Zaira Lima', SYSDATE - 26/24, 8);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (27, 64.00, 'Registro emocional do colaborador Arthur Barros', SYSDATE - 27/24, 11);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (28, 71.00, 'Registro emocional do colaborador Bianca Furtado', SYSDATE - 28/24, 4);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (29, 78.00, 'Registro emocional do colaborador Carlos Pinto', SYSDATE - 29/24, 10);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (30, 85.00, 'Registro emocional do colaborador Debora Seabra', SYSDATE - 30/24, 18);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (31, 92.00, 'Registro emocional do colaborador Eduardo Pires', SYSDATE - 31/24, 5);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (32, 99.00, 'Registro emocional do colaborador Fernanda Luz', SYSDATE - 32/24, 24);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (33, 61.00, 'Registro emocional do colaborador Guilherme Porto', SYSDATE - 33/24, 2);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (34, 68.00, 'Registro emocional do colaborador Helena Ramos', SYSDATE - 34/24, 15);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (35, 75.00, 'Registro emocional do colaborador Igor Almeida', SYSDATE - 35/24, 13);
INSERT INTO T_NRON_REGIST_EMOCAO VALUES (36, 82.00, 'Registro emocional do colaborador Juliana Prado', SYSDATE - 36/24, 17);


-- =============== RESPOSTA FORMULARIO  ===================

INSERT INTO T_NRON_RESP_FORMULARIO VALUES (1, SYSDATE - 1/24, 63.00, 56.00, 23.00, 'Check-in automatico do colaborador Ana Clara', 66.00, 86.00, 'Heuristica-Local v1', SYSDATE - 1/24, 1, 1);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (2, SYSDATE - 2/24, 68.00, 60.00, 26.00, 'Check-in automatico do colaborador Bruno Silva', 72.00, 87.00, 'Heuristica-Local v1', SYSDATE - 2/24, 2, 2);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (3, SYSDATE - 3/24, 73.00, 64.00, 29.00, 'Check-in automatico do colaborador Caio Nunes', 78.00, 88.00, 'Heuristica-Local v1', SYSDATE - 3/24, 3, 3);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (4, SYSDATE - 4/24, 78.00, 68.00, 32.00, 'Check-in automatico do colaborador Daniela Costa', 84.00, 89.00, 'Heuristica-Local v1', SYSDATE - 4/24, 4, 4);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (5, SYSDATE - 5/24, 83.00, 72.00, 35.00, 'Check-in automatico do colaborador Elaine Freitas', 90.00, 90.00, 'Heuristica-Local v1', SYSDATE - 5/24, 5, 5);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (6, SYSDATE - 6/24, 88.00, 76.00, 38.00, 'Check-in automatico do colaborador Fabio Mendes', 61.00, 91.00, 'Heuristica-Local v1', SYSDATE - 6/24, 6, 6);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (7, SYSDATE - 7/24, 58.00, 80.00, 41.00, 'Check-in automatico do colaborador Gabriela Souza', 67.00, 92.00, 'Heuristica-Local v1', SYSDATE - 7/24, 7, 7);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (8, SYSDATE - 8/24, 63.00, 84.00, 44.00, 'Check-in automatico do colaborador Henrique Prado', 73.00, 93.00, 'Heuristica-Local v1', SYSDATE - 8/24, 8, 8);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (9, SYSDATE - 9/24, 68.00, 88.00, 47.00, 'Check-in automatico do colaborador Isabela Tavares', 79.00, 94.00, 'Heuristica-Local v1', SYSDATE - 9/24, 9, 9);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (10, SYSDATE - 10/24, 73.00, 52.00, 50.00, 'Check-in automatico do colaborador Joao Ricardo', 85.00, 85.00, 'Heuristica-Local v1', SYSDATE - 10/24, 10, 10);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (11, SYSDATE - 11/24, 78.00, 56.00, 53.00, 'Check-in automatico do colaborador Karen Dias', 91.00, 86.00, 'Heuristica-Local v1', SYSDATE - 11/24, 11, 11);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (12, SYSDATE - 12/24, 83.00, 60.00, 56.00, 'Check-in automatico do colaborador Leonardo Braga', 62.00, 87.00, 'Heuristica-Local v1', SYSDATE - 12/24, 12, 12);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (13, SYSDATE - 13/24, 88.00, 64.00, 59.00, 'Check-in automatico do colaborador Marina Lopes', 68.00, 88.00, 'Heuristica-Local v1', SYSDATE - 13/24, 13, 13);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (14, SYSDATE - 14/24, 58.00, 68.00, 62.00, 'Check-in automatico do colaborador Natan Silva', 74.00, 89.00, 'Heuristica-Local v1', SYSDATE - 14/24, 14, 14);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (15, SYSDATE - 15/24, 63.00, 72.00, 65.00, 'Check-in automatico do colaborador Olivia Costa', 80.00, 90.00, 'Heuristica-Local v1', SYSDATE - 15/24, 15, 15);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (16, SYSDATE - 16/24, 68.00, 76.00, 68.00, 'Check-in automatico do colaborador Paulo Rezende', 86.00, 91.00, 'Heuristica-Local v1', SYSDATE - 16/24, 16, 16);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (17, SYSDATE - 17/24, 73.00, 80.00, 71.00, 'Check-in automatico do colaborador Queila Andrade', 92.00, 92.00, 'Heuristica-Local v1', SYSDATE - 17/24, 17, 17);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (18, SYSDATE - 18/24, 78.00, 84.00, 74.00, 'Check-in automatico do colaborador Rafael Mota', 63.00, 93.00, 'Heuristica-Local v1', SYSDATE - 18/24, 18, 18);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (19, SYSDATE - 19/24, 83.00, 88.00, 22.00, 'Check-in automatico do colaborador Sara Diniz', 69.00, 94.00, 'Heuristica-Local v1', SYSDATE - 19/24, 19, 19);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (20, SYSDATE - 20/24, 88.00, 52.00, 25.00, 'Check-in automatico do colaborador Thiago Castro', 75.00, 85.00, 'Heuristica-Local v1', SYSDATE - 20/24, 20, 20);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (21, SYSDATE - 21/24, 58.00, 56.00, 28.00, 'Check-in automatico do colaborador Ursula Porto', 81.00, 86.00, 'Heuristica-Local v1', SYSDATE - 21/24, 21, 21);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (22, SYSDATE - 22/24, 63.00, 60.00, 31.00, 'Check-in automatico do colaborador Vicente Amaral', 87.00, 87.00, 'Heuristica-Local v1', SYSDATE - 22/24, 22, 22);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (23, SYSDATE - 23/24, 68.00, 64.00, 34.00, 'Check-in automatico do colaborador Wesley Teixeira', 93.00, 88.00, 'Heuristica-Local v1', SYSDATE - 23/24, 23, 23);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (24, SYSDATE - 24/24, 73.00, 68.00, 37.00, 'Check-in automatico do colaborador Ximena Rocha', 64.00, 89.00, 'Heuristica-Local v1', SYSDATE - 24/24, 24, 24);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (25, SYSDATE - 25/24, 78.00, 72.00, 40.00, 'Check-in automatico do colaborador Yago Martins', 70.00, 90.00, 'Heuristica-Local v1', SYSDATE - 25/24, 25, 25);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (26, SYSDATE - 26/24, 83.00, 76.00, 43.00, 'Check-in automatico do colaborador Zaira Lima', 76.00, 91.00, 'Heuristica-Local v1', SYSDATE - 26/24, 26, 26);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (27, SYSDATE - 27/24, 88.00, 80.00, 46.00, 'Check-in automatico do colaborador Arthur Barros', 82.00, 92.00, 'Heuristica-Local v1', SYSDATE - 27/24, 27, 27);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (28, SYSDATE - 28/24, 58.00, 84.00, 49.00, 'Check-in automatico do colaborador Bianca Furtado', 88.00, 93.00, 'Heuristica-Local v1', SYSDATE - 28/24, 28, 28);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (29, SYSDATE - 29/24, 63.00, 88.00, 52.00, 'Check-in automatico do colaborador Carlos Pinto', 94.00, 94.00, 'Heuristica-Local v1', SYSDATE - 29/24, 29, 29);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (30, SYSDATE - 30/24, 68.00, 52.00, 55.00, 'Check-in automatico do colaborador Debora Seabra', 65.00, 85.00, 'Heuristica-Local v1', SYSDATE - 30/24, 30, 30);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (31, SYSDATE - 31/24, 73.00, 56.00, 58.00, 'Check-in automatico do colaborador Eduardo Pires', 71.00, 86.00, 'Heuristica-Local v1', SYSDATE - 31/24, 31, 31);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (32, SYSDATE - 32/24, 78.00, 60.00, 61.00, 'Check-in automatico do colaborador Fernanda Luz', 77.00, 87.00, 'Heuristica-Local v1', SYSDATE - 32/24, 32, 32);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (33, SYSDATE - 33/24, 83.00, 64.00, 64.00, 'Check-in automatico do colaborador Guilherme Porto', 83.00, 88.00, 'Heuristica-Local v1', SYSDATE - 33/24, 33, 33);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (34, SYSDATE - 34/24, 88.00, 68.00, 67.00, 'Check-in automatico do colaborador Helena Ramos', 89.00, 89.00, 'Heuristica-Local v1', SYSDATE - 34/24, 34, 34);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (35, SYSDATE - 35/24, 58.00, 72.00, 70.00, 'Check-in automatico do colaborador Igor Almeida', 60.00, 90.00, 'Heuristica-Local v1', SYSDATE - 35/24, 35, 35);
INSERT INTO T_NRON_RESP_FORMULARIO VALUES (36, SYSDATE - 36/24, 63.00, 76.00, 73.00, 'Check-in automatico do colaborador Juliana Prado', 66.00, 91.00, 'Heuristica-Local v1', SYSDATE - 36/24, 36, 36);

COMMIT;
