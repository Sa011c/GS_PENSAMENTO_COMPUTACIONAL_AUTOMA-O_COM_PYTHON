# ==============================================================================
# MISSION CONTROL AI - FIAP GLOBAL SOLUTION
# Equipe: estagiarios00
# Missão: Orion FIAP test
# ==============================================================================

# Constante para evitar erros de codificação com o símbolo de grau
GRAU = "\u00B0"

# 1. Configurações Iniciais e Dados de Entrada
NOME_MISSAO = "Orion FIAP test"
NOME_EQUIPE = "estagiarios00"

# Matriz de dados simulados (6 ciclos x 5 telemetrias)
dados_missao = [
    [24, 92, 88, 96, 90],  # Ciclo 1
    [27, 80, 72, 94, 85],  # Ciclo 2
    [31, 65, 58, 91, 70],  # Ciclo 3
    [36, 42, 38, 87, 55],  # Ciclo 4
    [39, 28, 19, 78, 35],  # Ciclo 5
    [34, 55, 32, 82, 50]   # Ciclo 6
]

areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]

# ==============================================================================
# 2. Funções de Análise de Telemetria (Retornam: classificação, pontos, status)
# ==============================================================================

def analisar_temperatura(temp):
    if temp < 18:
        return "ATENÇÃO", 1, "Temperatura baixa"
    elif 18 <= temp <= 30:
        return "NORMAL", 0, "Temperatura estável"
    elif 30 < temp <= 35:
        return "ATENÇÃO", 1, "Temperatura elevada"
    else:
        return "CRÍTICO", 2, "Risco de superaquecimento"

def analisar_comunicacao(com):
    if com < 30:
        return "CRÍTICO", 2, "Comunicação com a base em nível crítico"
    elif 30 <= com <= 59:
        return "ATENÇÃO", 1, "Comunicação instável"
    else:
        return "NORMAL", 0, "Comunicação estável"

def analisar_bateria(bat):
    if bat < 20:
        return "CRÍTICO", 2, "Bateria em nível crítico"
    elif 20 <= bat <= 49:
        return "ATENÇÃO", 1, "Bateria abaixo do recomendado"
    else:
        return "NORMAL", 0, "Energia estável"

def analisar_oxigenio(ox):
    if ox < 80:
        return "CRÍTICO", 2, "Oxigênio em nível crítico"
    elif 80 <= ox <= 89:
        return "ATENÇÃO", 1, "Oxigênio abaixo do ideal"
    else:
        return "NORMAL", 0, "Oxigênio adequado"

def analisar_estabilidade(est):
    if est < 40:
        return "CRÍTICO", 2, "Estabilidade operacional crítica"
    elif 40 <= est <= 69:
        return "ATENÇÃO", 1, "Estabilidade operacional reduzida"
    else:
        return "NORMAL", 0, "Estabilidade operacional adequada"

# ==============================================================================
# 3. Funções de Processamento Lógico e Relatórios
# ==============================================================================

def classificar_ciclo(pontos_ciclo):
    if 0 <= pontos_ciclo <= 2:
        return "MISSÃO ESTÁVEL"
    elif 3 <= pontos_ciclo <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"

def gerar_recomendacao(classif_ciclo, temp_c, com_c, bat_c, ox_c, est_c):
    """Gera recomendação dinâmica baseada nos piores problemas encontrados."""
    if classif_ciclo == "MISSÃO ESTÁVEL":
        return "Manter operação normal e continuar monitoramento."
    
    criticos = []
    if temp_c == "CRÍTICO": criticos.append("verificar controle térmico da missão")
    if com_c == "CRÍTICO": criticos.append("tentar restabelecer contato com a base")
    if bat_c == "CRÍTICO": criticos.append("ativar modo de economia de energia")
    if ox_c == "CRÍTICO": criticos.append("acionar protocolo de suporte à vida")
    if est_c == "CRÍTICO": criticos.append("reduzir operações não essenciais")
    
    if criticos:
        return "Ação Urgente: " + ", ".join(criticos) + "."
    else:
        return "Monitorar sistemas em atenção e preparar plano de contingência."

def processar_missao():
    total_ciclos = len(dados_missao)
    pontos_por_area = [0, 0, 0, 0, 0]
    historico_risco_ciclos = []
    
    somas_telemetria = [0, 0, 0, 0, 0]
    ciclos_criticos_qtd = 0
    maior_risco_encontrado = -1
    ciclo_mais_critico_idx = 0

    print("=" * 60)
    print("MISSION CONTROL AI")
    print("=" * 60)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {total_ciclos}")
    print("=" * 60)

    # Loop pelos ciclos
    for i, ciclo in enumerate(dados_missao):
        num_ciclo = i + 1
        temp, com, bat, ox, est = ciclo
        
        somas_telemetria[0] += temp
        somas_telemetria[1] += com
        somas_telemetria[2] += bat
        somas_telemetria[3] += ox
        somas_telemetria[4] += est

        class_t, p_t, txt_t = analisar_temperatura(temp)
        class_c, p_c, txt_c = analisar_comunicacao(com)
        class_b, p_b, txt_b = analisar_bateria(bat)
        class_o, p_o, txt_o = analisar_oxigenio(ox)
        class_e, p_e, txt_e = analisar_estabilidade(est)

        pontos_por_area[0] += p_t
        pontos_por_area[1] += p_c
        pontos_por_area[2] += p_b
        pontos_por_area[3] += p_o
        pontos_por_area[4] += p_e

        pontos_ciclo = p_t + p_c + p_b + p_o + p_e
        historico_risco_ciclos.append(pontos_ciclo)
        
        classif_ciclo = classificar_ciclo(pontos_ciclo)
        
        if pontos_ciclo > maior_risco_encontrado:
            maior_risco_encontrado = pontos_ciclo
            ciclo_mais_critico_idx = num_ciclo
            
        if classif_ciclo == "MISSÃO CRÍTICA":
            ciclos_criticos_qtd += 1

        recomendacao = gerar_recomendacao(classif_ciclo, class_t, class_c, class_b, class_o, class_e)

        # Exibição usando a constante GRAU
        print(f"\nCICLO {num_ciclo}")
        print("-" * 60)
        print(f"Temperatura: {temp} {GRAU}C | {class_t} | {txt_t}")
        print(f"Comunicação: {com}% | {class_c} | {txt_c}")
        print(f"Bateria: {bat}% | {class_b} | {txt_b}")
        print(f"Oxigênio: {ox}% | {class_o} | {txt_o}")
        print(f"Estabilidade: {est}% | {class_e} | {txt_e}")
        print(f"Pontuação de risco do ciclo: {pontos_ciclo}")
        print(f"Classificação do ciclo: {classif_ciclo}")
        print(f"Recomendação: {recomendacao}")

    # ==========================================================================
    # Relatório Final
    # ==========================================================================
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL DA MISSÃO")
    print("=" * 60)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {total_ciclos}")
    
    # Média de temperatura corrigida com a constante GRAU
    media_temp = somas_telemetria[0] / total_ciclos
    print(f"Média de temperatura: {media_temp:.2f} {GRAU}C")
    print(f"Média de comunicação: {somas_telemetria[1]/total_ciclos:.2f}%")
    print(f"Média de bateria: {somas_telemetria[2]/total_ciclos:.2f}%")
    print(f"Média de oxigênio: {somas_telemetria[3]/total_ciclos:.2f}%")
    print(f"Média de estabilidade: {somas_telemetria[4]/total_ciclos:.2f}%")
    
    print(f"Ciclo mais crítico: Ciclo {ciclo_mais_critico_idx}")
    print(f"Maior pontuação de risco: {maior_risco_encontrado}")
    
    risco_medio = sum(historico_risco_ciclos) / total_ciclos
    print(f"Risco médio da missão: {risco_medio:.2f}")
    print(f"Quantidade de ciclos críticos: {ciclos_criticos_qtd}")

    print("Tendência da missão:")
    risco_inicial = historico_risco_ciclos[0]
    risco_final = historico_risco_ciclos[-1]
    if risco_final > risco_inicial:
        print("A missão apresentou tendência de piora.")
    elif risco_final < risco_inicial:
        print("A missão apresentou tendência de melhora.")
    else:
        print("A missão permaneceu estável em relação ao início.")

    print("Pontuação acumulada por área:")
    maior_pontuacao_area = -1
    area_mais_afetada = ""
    
    for idx, area in enumerate(areas_monitoradas):
        print(f"{area}: {pontos_por_area[idx]} pontos")
        if pontos_por_area[idx] > maior_pontuacao_area:
            maior_pontuacao_area = pontos_por_area[idx]
            area_mais_afetada = area
            
    print(f"Área mais afetada:\n{area_mais_afetada}")

    print("Classificação final da missão:")
    classif_final = classificar_ciclo(int(risco_medio))
    print(classif_final)

    print("Conclusão:")
    if classif_final == "MISSÃO ESTÁVEL":
        print("A operação seguiu dentro dos padrões nominais esperados.")
    elif classif_final == "MISSÃO EM ATENÇÃO":
        print("A missão apresentou instabilidade relevante durante a operação. Apesar "
              "da tentativa de recuperação no último ciclo, ainda existem sistemas em "
              "atenção e a equipe deve manter o plano de contingência ativo.")
    else:
        print("A missao terminou em estado crítico severo. Intervenção imediata de engenharia é necessária.")
    print("=" * 60)

if __name__ == "__main__":
    processar_missao()