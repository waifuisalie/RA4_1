#!/usr/bin/env python3
import json
import os
import sys

# --- CONFIGURAÇÃO DE CAMINHOS ---
# 1. Pega o diretório onde este arquivo de teste está:
#    .../RA4_1/tests/RA4
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe dois níveis para achar a raiz do projeto:
#    .../RA4_1
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))

# 3. Define o caminho para o código fonte do otimizador:
#    .../RA4_1/src/RA4/functions/python
SRC_PATH = os.path.join(PROJECT_ROOT, "src", "RA4", "functions", "python")

# 4. Adiciona o diretório fonte ao PATH do Python para permitir imports
if os.path.exists(SRC_PATH):
    sys.path.append(SRC_PATH)
    # print(f"📂 Diretório fonte configurado: {SRC_PATH}")
else:
    print(f"❌ ERRO CRÍTICO: Pasta fonte não encontrada em: {SRC_PATH}")
    sys.exit(1)
# -------------------------------

print("--- INICIANDO TESTE DE INTEGRAÇÃO ---")

try:
    # Importa os módulos agora que o PATH está configurado
    from tac_instructions import TACAssignment, TACLabel, TACGoto, TACCopy
    from otimizador_tac import TACOptimizer
    print("✅ Importações: SUCESSO")
except ImportError as e:
    print(f"❌ Erro de Importação: {e}")
    sys.exit(1)

def testar_integracao_real():
    print("\n=== LENDO JSON OFICIAL ===")
    
    # --- CAMINHO ALVO DO JSON ---
    # Monta o caminho exato: .../RA4_1/outputs/RA4/tac_instructions.json
    json_path = os.path.join(PROJECT_ROOT, "outputs", "RA4", "tac_instructions.json")
    
    # Verifica se o arquivo existe
    if not os.path.exists(json_path):
        print("⚠️ ERRO: Arquivo 'tac_instructions.json' não encontrado.")
        print(f"   O script buscou em: {json_path}")
        print("   Certifique-se de ter rodado o Gerador TAC antes.")
        return

    print(f"📂 Arquivo Oficial Encontrado:\n   {json_path}")
    
    try:
        # Instancia o Otimizador
        opt = TACOptimizer()
        
        # Carrega o JSON
        opt.carregar_tac(json_path)
        print(f"📥 Instruções carregadas: {len(opt.instructions)}")
        
        # Executa a Otimização
        print("⚙️ Executando otimização...")
        stats = opt.otimizarTAC(json_path)
        
        # Exibe Resultados
        print("\n📊 --- RELATÓRIO DE OTIMIZAÇÃO ---")
        print(f"   Instruções Iniciais: {stats.get('initial_instructions', 'N/A')}")
        print(f"   Instruções Finais:   {stats.get('final_instructions', 'N/A')}")
        
        if 'initial_instructions' in stats and stats['initial_instructions'] > 0:
            reducao = ((stats['initial_instructions'] - stats['final_instructions']) / stats['initial_instructions'] * 100)
            print(f"   Redução Total:       {reducao:.1f}%")
        
        print("-" * 30)
        print(f"   Iterações:           {stats.get('iterations', 0)}")
        print(f"   Constantes Propag.:  {stats.get('constant_propagation', 0)}")
        print(f"   Código Morto Elim.:  {stats.get('dead_code_elimination', 0)}")
        print(f"   Saltos Eliminados:   {stats.get('jump_elimination', 0)}")
        print("-" * 30)
        print("✅ SUCESSO: Otimização concluída e integrada com o arquivo oficial!")
        
    except Exception as e:
        print(f"❌ ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_integracao_real()