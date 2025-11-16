# 🏭 Sistema de Controle de Qualidade Industrial

## 📋 Descrição do Projeto

Sistema de automação digital desenvolvido em Python para auxiliar no controle de produção e qualidade de peças fabricadas em linha de montagem. O sistema substitui o processo manual de inspeção, reduzindo atrasos, falhas de conferência e custos operacionais.

## ⚙️ Funcionalidades

### ✨ Principais Recursos

1. **Cadastro de Peças**: Registro de peças com ID automático, peso, cor e comprimento
2. **Inspeção Automatizada**: Validação automática baseada em critérios de qualidade
3. **Gestão de Armazenamento**: Organização automática em caixas com capacidade controlada
4. **Listagens Detalhadas**: Visualização de peças aprovadas, reprovadas e caixas fechadas
5. **Remoção de Peças**: Exclusão de peças com atualização automática do sistema
6. **Processamento em Lote**: Importação e processamento de múltiplas peças via arquivo CSV
7. **Relatórios Consolidados**: Estatísticas completas de produção e eficiência

### 📏 Critérios de Qualidade

Uma peça é **APROVADA** quando atende a TODOS os critérios:

- ✅ **Peso**: entre 95g e 105g
- ✅ **Cor**: azul ou verde
- ✅ **Comprimento**: entre 10cm e 20cm

Se qualquer critério não for atendido, a peça é **REPROVADA** com registro detalhado do motivo.

### 📦 Sistema de Armazenamento

- Cada caixa armazena até **10 peças aprovadas**
- Fechamento automático ao atingir capacidade máxima
- Criação automática de novas caixas conforme necessário
- Reabertura de caixas ao remover peças

## 🚀 Como Executar o Programa

### Passo a Passo para Execução

1. Salve o código em um arquivo chamado `sistema_qualidade.py`

2. Abra o terminal/prompt de comando na pasta do arquivo

3. Execute o comando:
```bash
python sistema_qualidade.py
```
ou
```bash
python3 sistema_qualidade.py
```

🏭 SISTEMA DE CONTROLE DE QUALIDADE INDUSTRIAL


📋 MENU PRINCIPAL:

  1. Cadastrar nova peça
  2. Listar peças aprovadas/reprovadas
  3. Remover peça cadastrada
  4. Listar caixas fechadas
  5. Gerar relatório final
  6. Processamento em lote
  0. Sair do sistema


```

### Descrição das Opções

| Opção | Função | Descrição |
|-------|--------|-----------|
| **1** | Cadastrar nova peça | Insere uma nova peça no sistema com inspeção automática |
| **2** | Listar peças | Exibe peças aprovadas, reprovadas ou todas |
| **3** | Remover peça | Remove uma peça específica pelo ID |
| **4** | Listar caixas fechadas | Mostra todas as caixas que atingiram capacidade máxima |
| **5** | Gerar relatório | Cria relatório completo de produção e qualidade |
| **6** | Processamento em lote | Carrega um arquivo csv de sua escolha e faz o processamento em lote de várias peças, sem necessidade de cadastro manual de uma a uma. |
| **0** | Sair | Encerra o sistema |

## 💡 Exemplos de Uso

### Exemplo 1: Cadastrando uma Peça Aprovada

**Entrada:**
```
Escolha uma opção: 1

Peso da peça (g): 100
Cor da peça: azul
Comprimento da peça (cm): 15
```

**Saída:**
```

✅ PEÇA APROVADA!

Peça #1 - Peso: 100g, Cor: azul, Comprimento: 15cm
Status: APROVADA
Armazenada na Caixa #1

```

### Exemplo 2: Cadastrando uma Peça Reprovada

**Entrada:**
```
Escolha uma opção: 1

Peso da peça (g): 110
Cor da peça: vermelho
Comprimento da peça (cm): 8
```

**Saída:**
```

❌ PEÇA REPROVADA!

Peça #2 - Peso: 110g, Cor: vermelho, Comprimento: 8cm
Status: REPROVADA

Motivos da reprovação:
  • Peso fora do padrão (110g - esperado: 95g a 105g)
  • Cor inválida (vermelho - esperado: azul ou verde)
  • Comprimento fora do padrão (8cm - esperado: 10cm a 20cm)

```

### Exemplo 3: Listando Peças Aprovadas

**Entrada:**
```
Escolha uma opção: 2

Escolha uma opção:
  1. Listar peças aprovadas
  2. Listar peças reprovadas
  3. Listar todas as peças

Opção: 1
```

**Saída:**
```

✅ PEÇAS APROVADAS


Total: 3 peça(s)

• Peça #1 - Peso: 100g, Cor: azul, Comprimento: 15cm
  Status: APROVADA | Caixa: #1
• Peça #3 - Peso: 98g, Cor: verde, Comprimento: 12cm
  Status: APROVADA | Caixa: #1
• Peça #5 - Peso: 102g, Cor: azul, Comprimento: 18cm
  Status: APROVADA | Caixa: #1

```

### Exemplo 4: Removendo uma Peça

**Entrada:**
```
Escolha uma opção: 3

Digite o ID da peça a ser removida: 2

📦 Peça encontrada:
   Peça #2 - Peso: 110g, Cor: vermelho, Comprimento: 8cm
   Status: REPROVADA

Confirma a remoção? (S/N): S
```

**Saída:**
```
✅ Peça removida com sucesso
```

### Exemplo 5: Listando Caixas Fechadas

**Entrada:**
```
Escolha uma opção: 4
```

**Saída:**
```

📦 CAIXAS FECHADAS


Total de caixas fechadas: 1

📦 Caixa #1 - 10/10 peças - Status: FECHADA
   Conteúdo: 10 peças
   IDs das peças: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19


```

### Exemplo 6: Relatório Final Completo

**Entrada:**
```
Escolha uma opção: 5
```

**Saída:**
```

RELATÓRIO CONSOLIDADO DE PRODUÇÃO E QUALIDADE


📊 ESTATÍSTICAS GERAIS:
   Total de peças processadas: 20
   Peças aprovadas: 14 (70.0%)
   Peças reprovadas: 6 (30.0%)

❌ ANÁLISE DE REPROVAÇÕES:
   • Peso: 2 ocorrência(s)
   • Cor: 2 ocorrência(s)
   • Comprimento: 2 ocorrência(s)

   Detalhamento das peças reprovadas:
   • Peça #15 - Peso: 90g, Cor: azul, Comprimento: 15cm
     └─ Peso fora do padrão (90g - esperado: 95g a 105g)
   • Peça #16 - Peso: 110g, Cor: verde, Comprimento: 14cm
     └─ Peso fora do padrão (110g - esperado: 95g a 105g)
   ...

📦 ARMAZENAMENTO:
   Caixas utilizadas: 2
   Caixas fechadas: 1
   • Caixa #1 - 10/10 peças - Status: FECHADA
     └─ Peças: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
   • Caixa #2 - 4/10 peças - Status: ABERTA
     └─ Peças: 11, 12, 13, 14

✨ EFICIÊNCIA DA LINHA: 70.0%


## 🏗️ Arquitetura do Sistema

### Estrutura de Classes

```
Sistema de Produção
├── Peca
│   ├── Atributos: id, peso, cor, comprimento, aprovada, motivos_reprovacao
│   └── Métodos: __init__, __str__
│
├── ControleQualidade
│   ├── Critérios: PESO_MIN, PESO_MAX, CORES_VALIDAS, etc.
│   └── Métodos: inspecionar_peca()
│
├── Caixa
│   ├── Atributos: numero, pecas, fechada
│   └── Métodos: adicionar_peca(), remover_peca(), fechar(), etc.
│
└── SistemaProducao
    ├── Atributos: pecas_aprovadas, pecas_reprovadas, caixas
    └── Métodos: cadastrar_peca(), remover_peca(), gerar_relatorio(), etc.
```

## 📊 Fluxo de Funcionamento

```
┌─────────────────────┐
│  Cadastrar Peça     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Inspeção Automática │
│  (ControleQualidade)│
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐ ┌──────────┐
│APROVADA │ │REPROVADA │
└────┬────┘ └────┬─────┘
     │           │
     ▼           ▼
┌─────────┐ ┌──────────────┐
│ Caixa   │ │Lista Reprov. │
└─────────┘ └──────────────┘
```