"""
Sistema de Gestão de Peças - Automação Industrial
Versão 5.0 - Com relatório padrão e relatório com custos separados
"""

import os
import re
from datetime import datetime

# ==================== ESTRUTURA DE DADOS ====================

pecas = []              # Lista de todas as peças cadastradas
caixa_atual = []        # Caixa atual (máx 10 peças)
caixas_fechadas = []    # Lista de caixas já fechadas
contador_id = 1         # Contador para IDs automáticos
valor_grama = 0.0       # Valor do grama (configurável)
valor_grama_configurado = False  # Flag para saber se foi configurado

# ==================== FUNÇÕES AUXILIARES ====================

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_data_hora_atual():
    """Retorna a data e hora atual formatada"""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def validar_cor(cor):
    """Remove caracteres especiais e normaliza a cor"""
    cor_limpa = re.sub(r'[^a-zA-Záéíóúâêôãõç\s]', '', cor)
    return cor_limpa.strip().lower()

def normalizar_cor(cor):
    """Normaliza a cor para comparação"""
    return validar_cor(cor)

def gerar_id_automatico():
    """Gera um ID automático no formato P0001"""
    global contador_id
    id_gerado = f"P{contador_id:04d}"
    contador_id += 1
    return id_gerado

def buscar_peca_por_id(id_busca):
    """Busca uma peça pelo ID"""
    for p in pecas:
        if p["id"] == id_busca:
            return p
    return None

def avaliar_peca(peso, cor, comprimento):
    """Avalia se a peça está aprovada ou reprovada"""
    motivos = []
    cor_normalizada = normalizar_cor(cor)
    
    if not (95 <= peso <= 105):
        motivos.append("Peso fora do padrão (95-105g)")
    
    if cor_normalizada not in ["azul", "verde"]:
        motivos.append(f"Cor não permitida (azul ou verde) - Valor informado: '{cor}'")
    
    if not (10 <= comprimento <= 20):
        motivos.append("Comprimento fora do padrão (10-20cm)")
    
    if motivos:
        return False, "; ".join(motivos)
    else:
        return True, ""

def adicionar_a_caixa(peca):
    """Adiciona uma peça aprovada à caixa atual"""
    global caixa_atual, caixas_fechadas
    
    caixa_atual.append(peca)
    
    if len(caixa_atual) == 10:
        caixas_fechadas.append(caixa_atual.copy())
        caixa_atual = []
        print("✓ Caixa fechada com 10 peças! Nova caixa iniciada.")

def calcular_peso_total(lista_pecas):
    """Calcula o peso total de uma lista de peças"""
    return sum(p["peso"] for p in lista_pecas)

def calcular_custo_pecas(lista_pecas, valor_g):
    """Calcula o custo total de uma lista de peças"""
    peso_total = calcular_peso_total(lista_pecas)
    return peso_total * valor_g

def formatar_moeda(valor):
    """Formata um valor como moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==================== FUNÇÕES DE CONFIGURAÇÃO ====================

def configurar_valor_grama():
    """Configura o valor do grama no sistema"""
    global valor_grama, valor_grama_configurado
    
    limpar_tela()
    print("\n" + "="*50)
    print("CONFIGURAR VALOR DO GRAMA")
    print("="*50)
    
    if valor_grama_configurado:
        print(f"\nValor atual do grama: {formatar_moeda(valor_grama)}")
        print("\nDeseja alterar o valor?")
        print("1. Sim")
        print("2. Não (manter atual)")
        opcao = input("Escolha (1/2): ").strip()
        if opcao != "1":
            print("\n✓ Valor mantido.")
            input("Pressione Enter para continuar...")
            return
    
    try:
        novo_valor = float(input("\nDigite o valor do grama (em R$): ").replace(",", "."))
        if novo_valor < 0:
            print("✗ O valor não pode ser negativo!")
        else:
            valor_grama = novo_valor
            valor_grama_configurado = True
            print(f"\n✓ Valor do grama configurado para: {formatar_moeda(valor_grama)}")
    except ValueError:
        print("\n✗ Erro: Digite um valor numérico válido!")
    
    input("\nPressione Enter para continuar...")

# ==================== FUNÇÕES DE RELATÓRIO ====================

def gerar_relatorio_padrao(para_arquivo=False):
    """
    Gera o relatório padrão (sem custos) - versão original do trabalho
    """
    if not pecas:
        msg = "Nenhuma peça cadastrada."
        if para_arquivo:
            return msg
        print(msg)
        return msg
    
    total_pecas = len(pecas)
    total_aprovadas = sum(1 for p in pecas if p["aprovada"])
    total_reprovadas = total_pecas - total_aprovadas
    
    aprovadas_azul = sum(1 for p in pecas if p["aprovada"] and normalizar_cor(p["cor"]) == "azul")
    aprovadas_verde = sum(1 for p in pecas if p["aprovada"] and normalizar_cor(p["cor"]) == "verde")
    
    total_caixas = len(caixas_fechadas)
    
    perc_aprovadas = (total_aprovadas / total_pecas) * 100 if total_pecas > 0 else 0
    perc_reprovadas = (total_reprovadas / total_pecas) * 100 if total_pecas > 0 else 0
    
    motivos = {}
    for p in pecas:
        if not p["aprovada"]:
            for motivo in p["motivo"].split("; "):
                motivos[motivo] = motivos.get(motivo, 0) + 1
    
    linhas = []
    linhas.append("="*60)
    linhas.append("RELATÓRIO FINAL - SISTEMA DE PEÇAS")
    linhas.append("="*60)
    linhas.append(f"Data/Hora: {obter_data_hora_atual()}")
    linhas.append("="*60)
    linhas.append("")
    
    linhas.append("RESUMO GERAL")
    linhas.append("-"*40)
    linhas.append(f"Total de peças processadas: {total_pecas}")
    linhas.append(f"▶ Peças APROVADAS: {total_aprovadas} ({perc_aprovadas:.1f}%)")
    linhas.append(f"▶ Peças REPROVADAS: {total_reprovadas} ({perc_reprovadas:.1f}%)")
    linhas.append("")
    
    linhas.append("DETALHAMENTO POR COR")
    linhas.append("-"*40)
    linhas.append(f"▶ Aprovadas - Cor AZUL: {aprovadas_azul}")
    linhas.append(f"▶ Aprovadas - Cor VERDE: {aprovadas_verde}")
    linhas.append("")
    
    linhas.append("ARMAZENAMENTO")
    linhas.append("-"*40)
    linhas.append(f"▶ Caixas fechadas: {total_caixas}")
    linhas.append(f"▶ Caixa atual: {len(caixa_atual)}/10 peças")
    linhas.append("")
    
    if motivos:
        linhas.append("MOTIVOS DE REPROVAÇÃO")
        linhas.append("-"*40)
        for motivo, qtd in motivos.items():
            perc_motivo = (qtd / total_reprovadas) * 100 if total_reprovadas > 0 else 0
            linhas.append(f"  {motivo}: {qtd} peça(s) ({perc_motivo:.1f}% das reprovações)")
        linhas.append("")
    
    linhas.append("LISTA COMPLETA DE PEÇAS")
    linhas.append("-"*40)
    for p in pecas:
        status = "APROVADA" if p["aprovada"] else "REPROVADA"
        linha = f"  {p['id']} | {p['peso']}g | {p['cor']} | {p['comprimento']}cm | {status}"
        if not p["aprovada"]:
            linha += f" | Motivo: {p['motivo']}"
        linha += f" | {p['data_hora']}"
        linhas.append(linha)
    
    linhas.append("")
    linhas.append("="*60)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("="*60)
    
    texto = "\n".join(linhas)
    
    if not para_arquivo:
        print(texto)
    
    return texto

def gerar_relatorio_com_custos(para_arquivo=False):
    """
    Gera o relatório com custos (funcionalidade extra)
    """
    if not pecas:
        msg = "Nenhuma peça cadastrada."
        if para_arquivo:
            return msg
        print(msg)
        return msg
    
    if not valor_grama_configurado:
        msg = "⚠️ Valor do grama não configurado! Configure primeiro (Opção 9)."
        if para_arquivo:
            return msg
        print(msg)
        return msg
    
    total_pecas = len(pecas)
    total_aprovadas = sum(1 for p in pecas if p["aprovada"])
    total_reprovadas = total_pecas - total_aprovadas
    
    aprovadas_azul = [p for p in pecas if p["aprovada"] and normalizar_cor(p["cor"]) == "azul"]
    aprovadas_verde = [p for p in pecas if p["aprovada"] and normalizar_cor(p["cor"]) == "verde"]
    reprovadas = [p for p in pecas if not p["aprovada"]]
    
    peso_total_geral = calcular_peso_total(pecas)
    peso_aprovadas = calcular_peso_total([p for p in pecas if p["aprovada"]])
    peso_reprovadas = calcular_peso_total(reprovadas)
    peso_azul = calcular_peso_total(aprovadas_azul)
    peso_verde = calcular_peso_total(aprovadas_verde)
    
    motivos = {}
    for p in reprovadas:
        for motivo in p["motivo"].split("; "):
            motivos[motivo] = motivos.get(motivo, 0) + 1
    
    total_caixas = len(caixas_fechadas)
    peso_caixas = calcular_peso_total([p for caixa in caixas_fechadas for p in caixa])
    
    custos = {}
    custos["total"] = calcular_custo_pecas(pecas, valor_grama)
    custos["aprovadas"] = calcular_custo_pecas([p for p in pecas if p["aprovada"]], valor_grama)
    custos["reprovadas"] = calcular_custo_pecas(reprovadas, valor_grama)
    custos["azul"] = calcular_custo_pecas(aprovadas_azul, valor_grama)
    custos["verde"] = calcular_custo_pecas(aprovadas_verde, valor_grama)
    custos["caixas"] = calcular_custo_pecas([p for caixa in caixas_fechadas for p in caixa], valor_grama)
    custos["descarte"] = custos["reprovadas"]
    
    perc_aprovadas = (total_aprovadas / total_pecas) * 100 if total_pecas > 0 else 0
    perc_reprovadas = (total_reprovadas / total_pecas) * 100 if total_pecas > 0 else 0
    perc_azul = (len(aprovadas_azul) / total_pecas) * 100 if total_pecas > 0 else 0
    perc_verde = (len(aprovadas_verde) / total_pecas) * 100 if total_pecas > 0 else 0
    
    linhas = []
    linhas.append("="*60)
    linhas.append("RELATÓRIO COM CUSTOS - SISTEMA DE PEÇAS")
    linhas.append("="*60)
    linhas.append(f"Data/Hora: {obter_data_hora_atual()}")
    linhas.append(f"Valor do grama: {formatar_moeda(valor_grama)}")
    linhas.append("="*60)
    linhas.append("")
    
    linhas.append("RESUMO GERAL")
    linhas.append("-"*40)
    linhas.append(f"Total de peças processadas: {total_pecas}")
    linhas.append(f"  Peso total: {peso_total_geral:.1f}g")
    linhas.append(f"▶ Peças APROVADAS: {total_aprovadas} ({perc_aprovadas:.1f}%)")
    linhas.append(f"  Peso total aprovado: {peso_aprovadas:.1f}g")
    linhas.append(f"▶ Peças REPROVADAS: {total_reprovadas} ({perc_reprovadas:.1f}%)")
    linhas.append(f"  Peso total reprovado: {peso_reprovadas:.1f}g")
    linhas.append("")
    
    linhas.append("CUSTOS")
    linhas.append("-"*40)
    linhas.append(f"▶ Custo TOTAL das peças: {formatar_moeda(custos['total'])}")
    linhas.append(f"▶ Custo das APROVADAS: {formatar_moeda(custos['aprovadas'])}")
    linhas.append(f"▶ Custo das REPROVADAS (DESCARTE): {formatar_moeda(custos['reprovadas'])}")
    linhas.append("")
    
    linhas.append("DETALHAMENTO POR COR")
    linhas.append("-"*40)
    linhas.append(f"▶ Aprovadas - Cor AZUL: {len(aprovadas_azul)} ({perc_azul:.1f}% do total)")
    linhas.append(f"  Peso total: {peso_azul:.1f}g")
    linhas.append(f"  Custo: {formatar_moeda(custos['azul'])}")
    linhas.append(f"▶ Aprovadas - Cor VERDE: {len(aprovadas_verde)} ({perc_verde:.1f}% do total)")
    linhas.append(f"  Peso total: {peso_verde:.1f}g")
    linhas.append(f"  Custo: {formatar_moeda(custos['verde'])}")
    linhas.append("")
    
    linhas.append("ARMAZENAMENTO")
    linhas.append("-"*40)
    linhas.append(f"▶ Caixas fechadas: {total_caixas}")
    linhas.append(f"  Peso total em caixas: {peso_caixas:.1f}g")
    linhas.append(f"  Valor total em caixas: {formatar_moeda(custos['caixas'])}")
    linhas.append(f"▶ Caixa atual: {len(caixa_atual)}/10 peças")
    if caixa_atual:
        peso_atual = calcular_peso_total(caixa_atual)
        linhas.append(f"  Peso atual: {peso_atual:.1f}g")
        linhas.append(f"  Valor atual: {formatar_moeda(calcular_custo_pecas(caixa_atual, valor_grama))}")
    linhas.append("")
    
    if motivos:
        linhas.append("MOTIVOS DE REPROVAÇÃO")
        linhas.append("-"*40)
        for motivo, qtd in motivos.items():
            perc_motivo = (qtd / total_reprovadas) * 100 if total_reprovadas > 0 else 0
            linhas.append(f"  {motivo}: {qtd} peça(s) ({perc_motivo:.1f}% das reprovações)")
        linhas.append("")
    
    linhas.append("LISTA COMPLETA DE PEÇAS")
    linhas.append("-"*40)
    for p in pecas:
        status = "APROVADA" if p["aprovada"] else "REPROVADA"
        linha = f"  {p['id']} | {p['peso']}g | {p['cor']} | {p['comprimento']}cm | {status}"
        if not p["aprovada"]:
            linha += f" | Motivo: {p['motivo']}"
        linha += f" | {p['data_hora']}"
        linhas.append(linha)
    
    linhas.append("")
    linhas.append("="*60)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("="*60)
    
    texto = "\n".join(linhas)
    
    if not para_arquivo:
        print(texto)
    
    return texto

# ==================== FUNÇÕES PRINCIPAIS ====================

def cadastrar_peca():
    """Cadastra uma nova peça no sistema (individual)"""
    limpar_tela()
    print("\n" + "="*50)
    print("CADASTRAR NOVA PEÇA")
    print("="*50)
    
    try:
        print("\nDeseja informar o ID manualmente ou gerar automaticamente?")
        print("1. Gerar ID automaticamente")
        print("2. Informar ID manualmente")
        opcao_id = input("Escolha (1/2): ").strip()
        
        if opcao_id == "2":
            id_peca = input("Digite o ID da peça: ").strip()
            if not id_peca:
                print("✗ ID não pode estar vazio! Usando ID automático.")
                id_peca = gerar_id_automatico()
            else:
                peca_existente = buscar_peca_por_id(id_peca)
                if peca_existente:
                    print(f"\n⚠️ ID {id_peca} JÁ ESTÁ CADASTRADO!")
                    print("\nDados da peça existente:")
                    print("-" * 40)
                    print(f"  ID: {peca_existente['id']}")
                    print(f"  Peso: {peca_existente['peso']}g")
                    print(f"  Cor: {peca_existente['cor']}")
                    print(f"  Comprimento: {peca_existente['comprimento']}cm")
                    print(f"  Status: {'✓ APROVADA' if peca_existente['aprovada'] else '✗ REPROVADA'}")
                    print(f"  Data/Hora: {peca_existente['data_hora']}")
                    print("-" * 40)
                    
                    print("\nO que deseja fazer?")
                    print("1. Gerar ID automaticamente")
                    print("2. Voltar ao menu inicial")
                    opcao_duplicado = input("Escolha (1/2): ").strip()
                    
                    if opcao_duplicado == "1":
                        id_peca = gerar_id_automatico()
                        print(f"✓ Novo ID gerado automaticamente: {id_peca}")
                    else:
                        print("\n✓ Operação cancelada. Voltando ao menu...")
                        input("Pressione Enter para continuar...")
                        return
        else:
            id_peca = gerar_id_automatico()
            print(f"✓ ID gerado automaticamente: {id_peca}")
        
        peso = float(input("Peso da peça (g): "))
        cor = input("Cor da peça: ").strip()
        comprimento = float(input("Comprimento da peça (cm): "))
        
        cor_normalizada = validar_cor(cor)
        if cor_normalizada != cor:
            print(f"✓ Cor normalizada para: '{cor_normalizada}'")
            cor = cor_normalizada
        
        aprovada, motivo = avaliar_peca(peso, cor, comprimento)
        
        peca = {
            "id": id_peca,
            "peso": peso,
            "cor": cor,
            "comprimento": comprimento,
            "aprovada": aprovada,
            "motivo": motivo,
            "data_hora": obter_data_hora_atual()
        }
        
        pecas.append(peca)
        
        if aprovada:
            adicionar_a_caixa(peca)
            print(f"\n✓ Peça {id_peca} APROVADA! Adicionada à caixa.")
        else:
            print(f"\n✗ Peça {id_peca} REPROVADA!")
            print(f"  Motivo(s): {motivo}")
        
        print(f"  Peças na caixa atual: {len(caixa_atual)}/10")
        print(f"  Data/Hora: {peca['data_hora']}")
        
    except ValueError:
        print("\n✗ Erro: Digite valores numéricos válidos para peso e comprimento.")
    
    input("\nPressione Enter para continuar...")

def cadastrar_lote():
    """Cadastra um lote de peças com as mesmas características"""
    limpar_tela()
    print("\n" + "="*50)
    print("CADASTRAR LOTE DE PEÇAS")
    print("="*50)
    print("\n⚠️ ATENÇÃO: Em lote, os IDs serão gerados automaticamente.")
    
    try:
        quantidade = int(input("\nQuantas peças deseja cadastrar no lote? "))
        if quantidade <= 0:
            print("✗ Quantidade deve ser maior que zero!")
            return
        
        peso = float(input("Peso padrão das peças (g): "))
        cor = input("Cor padrão das peças: ").strip()
        comprimento = float(input("Comprimento padrão das peças (cm): "))
        
        cor_normalizada = validar_cor(cor)
        if cor_normalizada != cor:
            print(f"✓ Cor normalizada para: '{cor_normalizada}'")
            cor = cor_normalizada
        
        print(f"\n▶ Cadastrando {quantidade} peças...")
        print("-" * 40)
        
        aprovadas = 0
        reprovadas = 0
        
        for i in range(quantidade):
            id_peca = gerar_id_automatico()
            aprovada, motivo = avaliar_peca(peso, cor, comprimento)
            
            peca = {
                "id": id_peca,
                "peso": peso,
                "cor": cor,
                "comprimento": comprimento,
                "aprovada": aprovada,
                "motivo": motivo,
                "data_hora": obter_data_hora_atual()
            }
            
            pecas.append(peca)
            
            if aprovada:
                adicionar_a_caixa(peca)
                aprovadas += 1
                print(f"  ✓ {id_peca} - APROVADA")
            else:
                reprovadas += 1
                print(f"  ✗ {id_peca} - REPROVADA: {motivo}")
        
        print("\n" + "-" * 40)
        print(f"▶ RESUMO DO LOTE:")
        print(f"  Total: {quantidade}")
        print(f"  Aprovadas: {aprovadas}")
        print(f"  Reprovadas: {reprovadas}")
        print(f"  Caixa atual: {len(caixa_atual)}/10")
        
    except ValueError:
        print("\n✗ Erro: Digite valores numéricos válidos!")
    
    input("\nPressione Enter para continuar...")

def listar_pecas():
    """Lista todas as peças cadastradas com opção de ordenação"""
    limpar_tela()
    print("\n" + "="*50)
    print("LISTAGEM DE PEÇAS")
    print("="*50)
    
    if not pecas:
        print("Nenhuma peça cadastrada.")
        input("\nPressione Enter para continuar...")
        return
    
    print("\nOrdenar por:")
    print("1. ID (padrão)")
    print("2. Peso (crescente)")
    print("3. Peso (decrescente)")
    print("4. Comprimento (crescente)")
    print("5. Comprimento (decrescente)")
    opcao_ordem = input("Escolha (1-5): ").strip()
    
    lista_ordenada = pecas.copy()
    
    if opcao_ordem == "2":
        lista_ordenada.sort(key=lambda x: x["peso"])
    elif opcao_ordem == "3":
        lista_ordenada.sort(key=lambda x: x["peso"], reverse=True)
    elif opcao_ordem == "4":
        lista_ordenada.sort(key=lambda x: x["comprimento"])
    elif opcao_ordem == "5":
        lista_ordenada.sort(key=lambda x: x["comprimento"], reverse=True)
    
    aprovadas = [p for p in lista_ordenada if p["aprovada"]]
    reprovadas = [p for p in lista_ordenada if not p["aprovada"]]
    
    print(f"\n▶ PEÇAS APROVADAS ({len(aprovadas)})")
    print("-" * 50)
    for p in aprovadas:
        print(f"  {p['id']} | {p['peso']}g | {p['cor']} | {p['comprimento']}cm | {p['data_hora']}")
    
    print(f"\n▶ PEÇAS REPROVADAS ({len(reprovadas)})")
    print("-" * 50)
    for p in reprovadas:
        print(f"  {p['id']} | {p['peso']}g | {p['cor']} | {p['comprimento']}cm | {p['data_hora']}")
        print(f"    Motivo: {p['motivo']}")
    
    print(f"\n▶ CAIXA ATUAL: {len(caixa_atual)}/10 peças")
    input("\nPressione Enter para continuar...")

def buscar_peca():
    """Busca uma peça pelo ID"""
    limpar_tela()
    print("\n" + "="*50)
    print("BUSCAR PEÇA POR ID")
    print("="*50)
    
    if not pecas:
        print("Nenhuma peça cadastrada.")
        input("\nPressione Enter para continuar...")
        return
    
    id_busca = input("\nDigite o ID da peça: ").strip()
    if not id_busca:
        print("✗ ID não pode estar vazio!")
        input("\nPressione Enter para continuar...")
        return
    
    peca = buscar_peca_por_id(id_busca)
    
    if peca:
        print("\n" + "="*40)
        print(f"  ID: {peca['id']}")
        print(f"  Peso: {peca['peso']}g")
        print(f"  Cor: {peca['cor']}")
        print(f"  Comprimento: {peca['comprimento']}cm")
        print(f"  Status: {'✓ APROVADA' if peca['aprovada'] else '✗ REPROVADA'}")
        if not peca['aprovada']:
            print(f"  Motivo: {peca['motivo']}")
        print(f"  Data/Hora: {peca['data_hora']}")
        print("="*40)
    else:
        print(f"\n✗ Peça com ID '{id_busca}' não encontrada!")
    
    input("\nPressione Enter para continuar...")

def remover_peca():
    """Remove uma peça cadastrada pelo ID"""
    limpar_tela()
    print("\n" + "="*50)
    print("REMOVER PEÇA")
    print("="*50)
    
    if not pecas:
        print("Nenhuma peça cadastrada.")
        return
    
    print("\nPeças cadastradas:")
    for i, p in enumerate(pecas, 1):
        status = "✓" if p["aprovada"] else "✗"
        print(f"  {i}. {p['id']} - {p['cor']} ({p['peso']}g) - {status} - {p['data_hora']}")
    
    try:
        idx = int(input("\nNúmero da peça a remover: ")) - 1
        if 0 <= idx < len(pecas):
            removida = pecas.pop(idx)
            print(f"\n✓ Peça {removida['id']} removida com sucesso!")
            
            if removida["aprovada"] and removida in caixa_atual:
                caixa_atual.remove(removida)
                print(f"  Peça também removida da caixa atual ({len(caixa_atual)}/10)")
        else:
            print("✗ Número inválido!")
    except ValueError:
        print("✗ Digite um número válido!")
    
    input("\nPressione Enter para continuar...")

def listar_caixas():
    """Lista todas as caixas fechadas com seus pesos e valores"""
    limpar_tela()
    print("\n" + "="*50)
    print("CAIXAS FECHADAS")
    print("="*50)
    
    if not caixas_fechadas:
        print("Nenhuma caixa foi fechada ainda.")
        print(f"Caixa atual: {len(caixa_atual)}/10 peças")
    else:
        for i, caixa in enumerate(caixas_fechadas, 1):
            peso_total = calcular_peso_total(caixa)
            print(f"\n▶ CAIXA {i} ({len(caixa)} peças) - Peso total: {peso_total:.1f}g")
            if valor_grama_configurado:
                print(f"  Valor da caixa: {formatar_moeda(calcular_custo_pecas(caixa, valor_grama))}")
            print("-" * 50)
            for p in caixa:
                print(f"  {p['id']} | {p['cor']} | {p['peso']}g | {p['comprimento']}cm")
    
    if caixa_atual:
        peso_atual = calcular_peso_total(caixa_atual)
        print(f"\n▶ Caixa atual: {len(caixa_atual)}/10 peças - Peso: {peso_atual:.1f}g")
        if valor_grama_configurado:
            print(f"  Valor atual: {formatar_moeda(calcular_custo_pecas(caixa_atual, valor_grama))}")
    
    input("\nPressione Enter para continuar...")

def menu_relatorios():
    """Submenu para escolha do tipo de relatório"""
    while True:
        limpar_tela()
        print("\n" + "="*50)
        print("  RELATÓRIOS - SISTEMA DE PEÇAS")
        print("="*50)
        print("""
        1. Relatório Padrão (exibir em tela)
        2. Relatório Padrão (exportar para TXT)
        3. Relatório com Custos (exibir em tela)
        4. Relatório com Custos (exportar para TXT)
        5. Voltar ao menu principal
        """)
        print("="*50)
        print(f"  Total peças: {len(pecas)}")
        if valor_grama_configurado:
            print(f"  Valor do grama: {formatar_moeda(valor_grama)} ✓")
        else:
            print(f"  Valor do grama: NÃO CONFIGURADO ⚠️")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            limpar_tela()
            print("\n" + "="*50)
            print("RELATÓRIO PADRÃO")
            print("="*50)
            gerar_relatorio_padrao(para_arquivo=False)
            input("\nPressione Enter para continuar...")
        elif opcao == "2":
            limpar_tela()
            print("\n" + "="*50)
            print("EXPORTAR RELATÓRIO PADRÃO")
            print("="*50)
            if not pecas:
                print("Nenhuma peça cadastrada.")
                input("\nPressione Enter para continuar...")
                continue
            nome_arquivo = f"relatorio_padrao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                texto = gerar_relatorio_padrao(para_arquivo=True)
                with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                    arquivo.write(texto)
                print(f"\n✓ Relatório exportado com sucesso!")
                print(f"  Arquivo: {nome_arquivo}")
            except Exception as e:
                print(f"\n✗ Erro ao exportar: {e}")
            input("\nPressione Enter para continuar...")
        elif opcao == "3":
            limpar_tela()
            print("\n" + "="*50)
            print("RELATÓRIO COM CUSTOS")
            print("="*50)
            if not valor_grama_configurado:
                print("\n⚠️ Valor do grama não configurado!")
                print("Configure primeiro na Opção 9 do menu principal.")
                input("\nPressione Enter para continuar...")
                continue
            gerar_relatorio_com_custos(para_arquivo=False)
            input("\nPressione Enter para continuar...")
        elif opcao == "4":
            limpar_tela()
            print("\n" + "="*50)
            print("EXPORTAR RELATÓRIO COM CUSTOS")
            print("="*50)
            if not pecas:
                print("Nenhuma peça cadastrada.")
                input("\nPressione Enter para continuar...")
                continue
            if not valor_grama_configurado:
                print("\n⚠️ Valor do grama não configurado!")
                print("Configure primeiro na Opção 9 do menu principal.")
                input("\nPressione Enter para continuar...")
                continue
            nome_arquivo = f"relatorio_custos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                texto = gerar_relatorio_com_custos(para_arquivo=True)
                with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                    arquivo.write(texto)
                print(f"\n✓ Relatório exportado com sucesso!")
                print(f"  Arquivo: {nome_arquivo}")
            except Exception as e:
                print(f"\n✗ Erro ao exportar: {e}")
            input("\nPressione Enter para continuar...")
        elif opcao == "5":
            break
        else:
            print("\n✗ Opção inválida!")
            input("Pressione Enter para continuar...")

def main():
    """Função principal - Menu interativo"""
    while True:
        limpar_tela()
        print("\n" + "="*50)
        print("  SISTEMA DE GESTÃO DE PEÇAS - MÉTIS INDUSTRIAL")
        print("="*50)
        print("""
        1. Cadastrar nova peça (individual)
        2. Cadastrar lote de peças
        3. Listar peças aprovadas/reprovadas
        4. Buscar peça por ID
        5. Remover peça cadastrada
        6. Listar caixas fechadas
        7. Relatórios
        8. Configurar valor do grama
        0. Sair
        """)
        print("="*50)
        print(f"  Caixa atual: {len(caixa_atual)}/10 peças")
        print(f"  Total peças: {len(pecas)}")
        if valor_grama_configurado:
            print(f"  Valor do grama: {formatar_moeda(valor_grama)} ✓")
        else:
            print(f"  Valor do grama: NÃO CONFIGURADO ⚠️")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_peca()
        elif opcao == "2":
            cadastrar_lote()
        elif opcao == "3":
            listar_pecas()
        elif opcao == "4":
            buscar_peca()
        elif opcao == "5":
            remover_peca()
        elif opcao == "6":
            listar_caixas()
        elif opcao == "7":
            menu_relatorios()
        elif opcao == "8":
            configurar_valor_grama()
        elif opcao == "0":
            print("\n" + "="*50)
            print("  ENCERRANDO SISTEMA...")
            print("="*50)
            print(f"  Resumo final:")
            print(f"  - Peças processadas: {len(pecas)}")
            print(f"  - Caixas fechadas: {len(caixas_fechadas)}")
            if valor_grama_configurado:
                peso_total = calcular_peso_total(pecas)
                print(f"  - Peso total: {peso_total:.1f}g")
                print(f"  - Valor total: {formatar_moeda(calcular_custo_pecas(pecas, valor_grama))}")
            print("="*50)
            break
        else:
            print("\n✗ Opção inválida! Pressione Enter para tentar novamente.")
            input()

# ==================== EXECUÇÃO DO PROGRAMA ====================

if __name__ == "__main__":
    main()