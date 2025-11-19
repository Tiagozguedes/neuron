-- Consulta 1: Listar usuários ativos ordenados por nome

SELECT ID_USUARIO, NOME, EM_USUARIO, STT_USUARIO
FROM T_NRON_USUARIO
WHERE STT_USUARIO = 'A'
ORDER BY NOME;

-- OBJETIVO: Para uma visão rápida de quais usuários estão ativos na plataforma, útil para gestão e acompanhamento de acessos.


-- Consulta 2: Listar registros de emoções com usuário e descrição da emoção
SELECT U.NOME AS USUARIO,
       E.NM_EMOCAO AS EMOCAO,
       R.INT_REGIST_EMOCAO AS INTENSIDADE,
       R.DS_REGIST_EMOCAO AS DESCRICAO,
       R.DT_REGIST_EMOCAO AS DATA
FROM T_NRON_REGIST_EMOCAO R
JOIN T_NRON_EMOCAO E ON R.ID_EMOCAO = E.ID_EMOCAO
JOIN T_NRON_RESP_FORMULARIO RESP ON RESP.ID_REGIST_EMOCAO = R.ID_REGIST_EMOCAO
JOIN T_NRON_USUARIO U ON U.ID_USUARIO = RESP.ID_USUARIO
ORDER BY R.DT_REGIST_EMOCAO DESC;

-- OBJETIVO: Essa consulta une usuário, registro e emoção para obter informações detalhadas de cada registro de emoção, útil para análise individual de bem-estar. 


-- Consulta 3 : Calcular média de intensidade das emoções por categoria
SELECT C.NOME_CATG_EMOCAO AS CATEGORIA, AVG(R.INT_REGIST_EMOCAO) AS MEDIA_INTENSIDADE
FROM T_NRON_REGIST_EMOCAO R
JOIN T_NRON_EMOCAO E ON R.ID_EMOCAO = E.ID_EMOCAO
JOIN T_NRON_CATG_EMOCAO C ON E.ID_CATG_EMOCAO = C.ID_CATG_EMOCAO
GROUP BY C.NOME_CATG_EMOCAO
ORDER BY MEDIA_INTENSIDADE DESC;

-- OBJETIVO: Identificar qual categoria de emoção tem maior intensidade média, ajudando a tomar decisões sobre ações de saúde mental ou clima organizacional.


-- Consulta 4: Categorias de emoção com média de intensidade maior que 60
SELECT C.NOME_CATG_EMOCAO AS CATEGORIA,
       COUNT(R.ID_REGIST_EMOCAO) AS TOTAL_REGISTROS,
       AVG(R.INT_REGIST_EMOCAO) AS MEDIA_INTENSIDADE
FROM T_NRON_REGIST_EMOCAO R
JOIN T_NRON_EMOCAO E ON R.ID_EMOCAO = E.ID_EMOCAO
JOIN T_NRON_CATG_EMOCAO C ON E.ID_CATG_EMOCAO = C.ID_CATG_EMOCAO
GROUP BY C.NOME_CATG_EMOCAO
HAVING AVG(R.INT_REGIST_EMOCAO) > 60
ORDER BY MEDIA_INTENSIDADE DESC;

-- OBJETIVO : Identificar categorias de emoções mais intensas, permitindo que gestores ou IA priorizem intervenções ou análises.
