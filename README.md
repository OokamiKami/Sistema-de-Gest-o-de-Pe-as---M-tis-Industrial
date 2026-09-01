# Sistema de Gestão de Peças - Métis Industrial

## 📋 Sobre o Projeto

Sistema desenvolvido em Python para automação do controle de produção e qualidade de peças em uma linha de montagem industrial.

O sistema avalia automaticamente se cada peça está aprovada ou reprovada com base em critérios de qualidade (peso, cor e comprimento), armazena as peças aprovadas em caixas de capacidade limitada (10 peças) e gera relatórios consolidados.

## 🎯 Funcionalidades

| # | Funcionalidade | Descrição |
|---|---|---|
| 1 | Cadastrar peça | Registra peça com ID, peso, cor e comprimento |
| 2 | Cadastrar lote | Cadastra múltiplas peças com as mesmas características |
| 3 | Listar peças | Exibe todas as peças com opção de ordenação |
| 4 | Buscar por ID | Localiza uma peça específica |
| 5 | Remover peça | Remove uma peça cadastrada |
| 6 | Listar caixas | Mostra caixas fechadas com peso e valor |
| 7 | Relatórios | Submenu com relatório padrão e com custos |
| 8 | Configurar valor do grama | Define valor para cálculo de custos |

## ✅ Critérios de Aprovação

| Critério | Padrão |
|---|---|
| Peso | 95g – 105g |
| Cor | Azul ou Verde |
| Comprimento | 10cm – 20cm |

## 🛠️ Tecnologias Utilizadas

- Python 3
- Biblioteca padrão (os, re, datetime)

## ▶️ Como Rodar o Programa

### Pré-requisitos
- Python 3.6 ou superior instalado

### Passos

1. Clone o repositório:
```bash
git clone [https://github.com/OokamiKami/Sistema-de-Gest-o-de-Pe-as---M-tis-Industrial.git]
