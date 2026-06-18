# Base de Conhecimento: Análise Prática State of Data Brasil

## 1. O que já foi executado na base do projeto

[cite_start]O pipeline inicial já consolidou e pré-processou as bases de dados da pesquisa State of Data Brasil[cite: 9]. [cite_start]Foram importados em massa 4 arquivos CSV (referentes aos anos de 2021 a 2024) utilizando a função `map_dfr` do pacote `purrr`[cite: 37, 38, 39, 40, 72].

## 2. Limpeza e Tratamento

- [cite_start]Uma coluna `ano_pesquisa` foi extraída a partir do nome dos arquivos utilizando Expressões Regulares (`str_extract`)[cite: 137, 138, 161].
- [cite_start]Registros duplicados foram tratados utilizando a função `distinct()` do pacote `dplyr`[cite: 229, 238].
- [cite_start]Os dados consolidados finais (17.419 registros) foram exportados para o formato Apache Parquet usando `arrow::write_parquet` para otimização de leitura[cite: 234, 251, 255].

## 3. O Desafio Prático (Trabalho Final)

[cite_start]O trabalho atua com dados desestruturados e exige a formulação de perguntas de negócio[cite: 287]. [cite_start]Um exemplo prático demonstrado foi o cruzamento (Join) do custo da Cesta Básica Nacional (dados do DIEESE 2024) com os salários da área de dados por capital[cite: 295, 303, 315]. [cite_start]A análise revelou qual cidade oferece o melhor poder de compra, provando que o maior salário nominal nem sempre compensa o custo de vida local[cite: 338].

## 4. Novas Estratégias de Extração de Dados (Python)

Como parte da evolução do projeto, as seguintes abordagens foram implementadas para garantir maior estabilidade na extração de dados:
- **FipeZAP (Custo de Moradia):** Em vez de scraping via HTML/BeautifulSoup (que se tornou instável devido à renderização via JavaScript), os dados agora são baixados e lidos diretamente da planilha oficial usando `pandas` (`pd.read_excel`).
- **State of Data Brasil:** Os dados brutos da pesquisa agora podem ser baixados automaticamente através da biblioteca oficial do Kaggle (`kaggle`), garantindo reprodutibilidade e dispensando acesso manual pelo navegador.
