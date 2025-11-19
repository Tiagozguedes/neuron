-- Limpeza das tabelas Neuron (ordem compatível com as FKs).
-- Cada bloco ignora o erro ORA-00942 caso a tabela já tenha sido removida.

SET SERVEROUTPUT ON

DECLARE
  CURSOR c_tabelas IS
    SELECT table_name
      FROM user_tables
     WHERE table_name LIKE 'T_NRON%'
     ORDER BY table_name;
BEGIN
  FOR registro IN c_tabelas LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE "' || registro.table_name || '" CASCADE CONSTRAINTS';
      DBMS_OUTPUT.PUT_LINE('Tabela ' || registro.table_name || ' removida.');
    EXCEPTION
      WHEN OTHERS THEN
        IF SQLCODE = -942 THEN
          DBMS_OUTPUT.PUT_LINE('Tabela ' || registro.table_name || ' já não existe.');
        ELSE
          DBMS_OUTPUT.PUT_LINE('Falha ao remover ' || registro.table_name || ': ' || SQLERRM);
        END IF;
    END;
  END LOOP;
END;
/
