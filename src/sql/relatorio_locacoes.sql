select L.DATA_DEVOLUCAO
     , L.DATA_LOCACAO
     , L.CPF
     , L.PLACA
     , L.NOME_MODELO
     , L.NOME_MARCA
     , C.CPF as CLIENTES
     , M.NOME_MODELO as MODELOS
     , M.NOME_MARCA as MODELOS
     , MC.NOME_MARCA as MARCAS
  from LOCACOES L
  inner join CLIENTES C
  on L.CPF = C.CPF
  inner join MODELOS M
  on L.NOME_MODELO = M.NOME_MODELO 
  inner join MARCAS MC
  on L.NOME_MARCA = MC.NOME_MARCA
  order by L.CPF, L.PLACA