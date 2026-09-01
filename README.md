# Sistema de Gestão de Peças - Métis Industrial

## 📋 Sobre o Projeto

Sistema desenvolvido em Python para automação do controle de produção e qualidade de peças em uma linha de montagem industrial.

O sistema avalia automaticamente se cada peça está aprovada ou reprovada com base em critérios de qualidade (peso, cor e comprimento), armazena as peças aprovadas em caixas de capacidade limitada (10 peças) e gera relatórios consolidados.

O nome **Métis** faz referência à deusa grega da sabedoria e planejamento, refletindo o propósito da ferramenta: organizar, planejar e executar o controle de qualidade com inteligência e eficiência.

---

## 🎯 Funcionalidades

| # | Funcionalidade | Descrição |
|---|---|---|
| 1 | Cadastrar peça (individual) | Registra uma peça com ID, peso, cor e comprimento |
| 2 | Cadastrar lote | Cadastra múltiplas peças com as mesmas características |
| 3 | Listar peças | Exibe todas as peças com opção de ordenação |
| 4 | Buscar por ID | Localiza uma peça específica pelo identificador |
| 5 | Remover peça | Remove uma peça cadastrada do sistema |
| 6 | Listar caixas | Mostra caixas fechadas com peso total e valor |
| 7 | Relatórios | Submenu com relatório padrão e com custos |
| 8 | Configurar valor do grama | Define valor para cálculo de custos |

---

## ✅ Critérios de Aprovação

| Critério | Padrão | Observação |
|---|---|---|
| Peso | 95g – 105g | Fora deste intervalo = reprovada |
| Cor | Azul ou Verde | Outras cores = reprovada |
| Comprimento | 10cm – 20cm | Fora deste intervalo = reprovada |

### Motivos de Reprovação

- Peso fora do padrão (95-105g)
- Cor não permitida (azul ou verde)
- Comprimento fora do padrão (10-20cm)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.6 ou superior
- Biblioteca padrão:
  - `os` - limpeza de tela
  - `re` - validação de caracteres especiais
  - `datetime` - registro de data/hora

---

## ▶️ Como Rodar o Programa

### Pré-requisitos

- Python 3.6 ou superior instalado
- Git (para clonar o repositório)

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/OokamiKami/Sistema-de-Gest-o-de-Pe-as---M-tis-Industrial.git
```

2. **Acesse a pasta do projeto:**
```bash
cd NOME_DO_REPOSITORIO
```

3. **Execute o programa:**
```bash
python sistema_pecas.py
```

### Execução sem Git

Se você não tiver o Git instalado:

1. Baixe o arquivo `sistema_pecas.py`
2. Abra o terminal na pasta onde o arquivo está salvo
3. Execute:
```bash
python sistema_pecas.py
```

---

## 📝 Exemplo de Uso

### Cadastro de Peça Individual

**Entrada:**
```
Peso da peça (g): 100
Cor da peça: azul
Comprimento da peça (cm): 15
```

**Saída:**
```
✓ Peça P0001 APROVADA! Adicionada à caixa.
Peças na caixa atual: 1/10
Data/Hora: 01/09/2026 14:30:15
```

---

### Cadastro de Peça Reprovada

**Entrada:**
```
Peso da peça (g): 110
Cor da peça: vermelho
Comprimento da peça (cm): 18
```

**Saída:**
```
✗ Peça P0002 REPROVADA!
  Motivo(s): Peso fora do padrão (95-105g); Cor não permitida (azul ou verde) - Valor informado: 'vermelho'
Peças na caixa atual: 1/10
Data/Hora: 01/09/2026 14:32:20
```

---

### Cadastro de Lote

**Entrada:**
```
Quantas peças deseja cadastrar no lote? 5
Peso padrão das peças (g): 100
Cor padrão das peças: azul
Comprimento padrão das peças (cm): 15
```

**Saída:**
```
▶ Cadastrando 5 peças...
----------------------------------------
  ✓ P0003 - APROVADA
  ✓ P0004 - APROVADA
  ✓ P0005 - APROVADA
  ✓ P0006 - APROVADA
  ✓ P0007 - APROVADA
----------------------------------------
▶ RESUMO DO LOTE:
  Total: 5
  Aprovadas: 5
  Reprovadas: 0
  Caixa atual: 6/10
```

---

### ID Duplicado

**Entrada (cadastrar peça com ID já existente):**
```
Deseja informar o ID manualmente ou gerar automaticamente?
1. Gerar ID automaticamente
2. Informar ID manualmente
Escolha (1/2): 2
Digite o ID da peça: P0001
```

**Saída:**
```
⚠️ ID P0001 JÁ ESTÁ CADASTRADO!

Dados da peça existente:
----------------------------------------
  ID: P0001
  Peso: 100g
  Cor: azul
  Comprimento: 15cm
  Status: ✓ APROVADA
  Data/Hora: 01/09/2026 14:30:15
----------------------------------------

O que deseja fazer?
1. Gerar ID automaticamente
2. Voltar ao menu inicial
Escolha (1/2):
```

---

### Listagem de Peças com Ordenação

**Entrada (menu):**
```
Opção 3 → Ordenar por: 2 (Peso crescente)
```

**Saída:**
```
▶ PEÇAS APROVADAS (18)
----------------------------------------
  P0010 | 95g | azul | 12cm | 01/09/2026 14:35:00
  P0001 | 100g | azul | 15cm | 01/09/2026 14:30:15
  P0003 | 100g | azul | 15cm | 01/09/2026 14:33:10
  P0015 | 105g | verde | 18cm | 01/09/2026 14:40:00

▶ PEÇAS REPROVADAS (7)
----------------------------------------
  P0002 | 110g | vermelho | 18cm | 01/09/2026 14:32:20
    Motivo: Peso fora do padrão (95-105g); Cor não permitida (azul ou verde) - Valor informado: 'vermelho'
```

---

### Buscar Peça por ID

**Entrada (menu):**
```
Opção 4 → Digite o ID da peça: P0001
```

**Saída:**
```
========================================
  ID: P0001
  Peso: 100g
  Cor: azul
  Comprimento: 15cm
  Status: ✓ APROVADA
  Data/Hora: 01/09/2026 14:30:15
========================================
```

---

### Remover Peça

**Entrada (menu):**
```
Opção 5 → Número da peça a remover: 1
```

**Saída:**
```
✓ Peça P0001 removida com sucesso!
  Peça também removida da caixa atual (0/10)
```

---

### Relatório Padrão (sem custos)

**Entrada (menu):**
```
Opção 7 → Opção 1 (Relatório Padrão)
```

**Saída:**
```
============================================================
RELATÓRIO FINAL - SISTEMA DE PEÇAS
============================================================
Data/Hora: 01/09/2026 15:00:00
============================================================

RESUMO GERAL
----------------------------------------
Total de peças processadas: 25
▶ Peças APROVADAS: 18 (72.0%)
▶ Peças REPROVADAS: 7 (28.0%)

DETALHAMENTO POR COR
----------------------------------------
▶ Aprovadas - Cor AZUL: 10
▶ Aprovadas - Cor VERDE: 8

ARMAZENAMENTO
----------------------------------------
▶ Caixas fechadas: 1
▶ Caixa atual: 8/10 peças

MOTIVOS DE REPROVAÇÃO
----------------------------------------
  Peso fora do padrão (95-105g): 3 peça(s) (42.9% das reprovações)
  Cor não permitida (azul ou verde): 4 peça(s) (57.1% das reprovações)

LISTA COMPLETA DE PEÇAS
----------------------------------------
  P0001 | 100g | azul | 15cm | APROVADA | 01/09/2026 14:30:15
  P0002 | 110g | vermelho | 18cm | REPROVADA | Motivo: Peso fora do padrão (95-105g); Cor não permitida (azul ou verde) - Valor informado: 'vermelho' | 01/09/2026 14:32:20
  P0003 | 100g | azul | 15cm | APROVADA | 01/09/2026 14:33:10
  ...

============================================================
FIM DO RELATÓRIO
============================================================
```

---

### Relatório com Custos (funcionalidade extra)

**Pré-requisito:** Configurar valor do grama (Opção 8)

**Entrada:**
```
Opção 8 → Valor do grama: 0.75
Opção 7 → Opção 3 (Relatório com Custos)
```

**Saída:**
```
============================================================
RELATÓRIO COM CUSTOS - SISTEMA DE PEÇAS
============================================================
Data/Hora: 01/09/2026 15:05:00
Valor do grama: R$ 0,75
============================================================

RESUMO GERAL
----------------------------------------
Total de peças processadas: 25
  Peso total: 2450.0g
▶ Peças APROVADAS: 18 (72.0%)
  Peso total aprovado: 1850.0g
▶ Peças REPROVADAS: 7 (28.0%)
  Peso total reprovado: 600.0g

CUSTOS
----------------------------------------
▶ Custo TOTAL das peças: R$ 1.837,50
▶ Custo das APROVADAS: R$ 1.387,50
▶ Custo das REPROVADAS (DESCARTE): R$ 450,00

DETALHAMENTO POR COR
----------------------------------------
▶ Aprovadas - Cor AZUL: 10 (40.0% do total)
  Peso total: 1000.0g
  Custo: R$ 750,00
▶ Aprovadas - Cor VERDE: 8 (32.0% do total)
  Peso total: 850.0g
  Custo: R$ 637,50

ARMAZENAMENTO
----------------------------------------
▶ Caixas fechadas: 1
  Peso total em caixas: 1000.0g
  Valor total em caixas: R$ 750,00
▶ Caixa atual: 8/10 peças
  Peso atual: 850.0g
  Valor atual: R$ 637,50

MOTIVOS DE REPROVAÇÃO
----------------------------------------
  Peso fora do padrão (95-105g): 3 peça(s) (42.9% das reprovações)
  Cor não permitida (azul ou verde): 4 peça(s) (57.1% das reprovações)

LISTA COMPLETA DE PEÇAS
----------------------------------------
  P0001 | 100g | azul | 15cm | APROVADA | 01/09/2026 14:30:15
  P0002 | 110g | vermelho | 18cm | REPROVADA | Motivo: Peso fora do padrão (95-105g); Cor não permitida (azul ou verde) - Valor informado: 'vermelho' | 01/09/2026 14:32:20
  ...

============================================================
FIM DO RELATÓRIO
============================================================
```

---

### Exportação de Relatório para TXT

**Entrada (menu):**
```
Opção 7 → Opção 2 (Relatório Padrão - Exportar TXT)
```

**Saída:**
```
✓ Relatório exportado com sucesso!
  Arquivo: relatorio_padrao_20260901_150500.txt
  Local: C:\Users\SeuUsuario\Documents\projeto\
```

O arquivo gerado pode ser aberto em qualquer editor de texto.

---

### Listar Caixas Fechadas

**Entrada (menu):**
```
Opção 6
```

**Saída:**
```
▶ CAIXA 1 (10 peças) - Peso total: 1000.0g
  Valor da caixa: R$ 750,00
----------------------------------------
  P0001 | azul | 100g | 15cm
  P0003 | azul | 100g | 15cm
  P0004 | azul | 100g | 15cm
  P0005 | azul | 100g | 15cm
  P0006 | azul | 100g | 15cm
  P0007 | azul | 100g | 15cm
  P0008 | verde | 98g | 12cm
  P0009 | verde | 98g | 12cm
  P0010 | verde | 98g | 12cm
  P0011 | verde | 98g | 12cm

▶ Caixa atual: 8/10 peças - Peso: 850.0g
  Valor atual: R$ 637,50
```

---

### Configurar Valor do Grama

**Entrada (menu):**
```
Opção 8 → Digite o valor do grama (em R$): 0,75
```

**Saída:**
```
✓ Valor do grama configurado para: R$ 0,75
```

---

## 📁 Estrutura do Código

```
sistema_pecas.py
│
├── ESTRUTURA DE DADOS
│   ├── pecas (lista de dicionários)
│   ├── caixa_atual (lista)
│   ├── caixas_fechadas (lista de listas)
│   ├── contador_id (int)
│   ├── valor_grama (float)
│   └── valor_grama_configurado (bool)
│
├── FUNÇÕES AUXILIARES
│   ├── limpar_tela()
│   ├── obter_data_hora_atual()
│   ├── validar_cor()
│   ├── normalizar_cor()
│   ├── gerar_id_automatico()
│   ├── buscar_peca_por_id()
│   ├── avaliar_peca()
│   ├── adicionar_a_caixa()
│   ├── calcular_peso_total()
│   ├── calcular_custo_pecas()
│   └── formatar_moeda()
│
├── FUNÇÕES DE CONFIGURAÇÃO
│   └── configurar_valor_grama()
│
├── FUNÇÕES DE RELATÓRIO
│   ├── gerar_relatorio_padrao()
│   └── gerar_relatorio_com_custos()
│
├── FUNÇÕES PRINCIPAIS
│   ├── cadastrar_peca()
│   ├── cadastrar_lote()
│   ├── listar_pecas()
│   ├── buscar_peca()
│   ├── remover_peca()
│   ├── listar_caixas()
│   └── menu_relatorios()
│
└── FUNÇÃO PRINCIPAL
    └── main()
```

---

## 🔧 Boas Práticas Aplicadas

| Prática | Aplicação no código |
|---|---|
| Modularização | Funções separadas por responsabilidade |
| Validação de entrada | Tratamento de erros com try/except |
| Documentação | Docstrings em todas as funções |
| Organização | Código estruturado em seções |
| Experiência do usuário | Menu interativo com feedback claro |
| Tratamento de dados | Validação de caracteres especiais |
| Separação de responsabilidades | Relatório padrão e com custos separados |

---

## 🚀 Possíveis Expansões

O sistema pode ser expandido para um cenário industrial real com:

- **Sensores IoT:** Coleta automática de peso, cor e comprimento
- **Inteligência Artificial:** Classificação avançada de defeitos
- **Banco de Dados:** Armazenamento em SQL para histórico
- **API REST:** Integração com sistemas ERP
- **Dashboard Web:** Visualização em tempo real
- **Leitura de Código de Barras:** Identificação rápida das peças

---

## 👥 Desenvolvido por

**Nome:** Thayna Ingryd Rodrigues

**Curso:** Inteligência Artificial e Automação Digital

**Disciplina:** Algoritmos e Lógica de Programação

**Semestre:** 1º Semestre

---

## 📄 Licença

Este projeto é de uso acadêmico e não possui licença para uso comercial.

---

**Métis Industrial** - Automação e Controle de Qualidade
```
