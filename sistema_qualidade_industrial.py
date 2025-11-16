"""
Sistema de Controle de Qualidade Industrial
Autor: Sistema de Automação Digital
Versão: 2.1
"""

import csv
import os

class Peca:
    """Classe que representa uma peça da linha de produção"""
    
    def __init__(self, id_peca, peso, cor, comprimento):
        self.id = id_peca
        self.peso = peso
        self.cor = cor.lower()
        self.comprimento = comprimento
        self.aprovada = False
        self.motivos_reprovacao = []
        self.caixa = None  # Referência à caixa onde está armazenada
    
    def __str__(self):
        return f"Peça #{self.id} - Peso: {self.peso}g, Cor: {self.cor}, Comprimento: {self.comprimento}cm"


class ControleQualidade:
    """Classe responsável pela inspeção e validação das peças"""
    
    # Critérios de qualidade
    PESO_MIN = 95
    PESO_MAX = 105
    CORES_VALIDAS = ['azul', 'verde']
    COMPRIMENTO_MIN = 10
    COMPRIMENTO_MAX = 20
    
    @classmethod
    def inspecionar_peca(cls, peca):
        """
        Avalia se a peça atende aos critérios de qualidade
        Retorna True se aprovada, False se reprovada
        """
        motivos = []
        
        # Verificar peso
        if peca.peso < cls.PESO_MIN or peca.peso > cls.PESO_MAX:
            motivos.append(f"Peso fora do padrão ({peca.peso}g - esperado: {cls.PESO_MIN}g a {cls.PESO_MAX}g)")
        
        # Verificar cor
        if peca.cor not in cls.CORES_VALIDAS:
            motivos.append(f"Cor inválida ({peca.cor} - esperado: {' ou '.join(cls.CORES_VALIDAS)})")
        
        # Verificar comprimento
        if peca.comprimento < cls.COMPRIMENTO_MIN or peca.comprimento > cls.COMPRIMENTO_MAX:
            motivos.append(f"Comprimento fora do padrão ({peca.comprimento}cm - esperado: {cls.COMPRIMENTO_MIN}cm a {cls.COMPRIMENTO_MAX}cm)")
        
        # Definir status da peça
        if len(motivos) == 0:
            peca.aprovada = True
            return True
        else:
            peca.aprovada = False
            peca.motivos_reprovacao = motivos
            return False


class Caixa:
    """Classe que representa uma caixa de armazenamento"""
    
    CAPACIDADE_MAXIMA = 10
    
    def __init__(self, numero):
        self.numero = numero
        self.pecas = []
        self.fechada = False
    
    def adicionar_peca(self, peca):
        """Adiciona uma peça aprovada à caixa"""
        if self.fechada:
            return False
        
        if len(self.pecas) < self.CAPACIDADE_MAXIMA:
            self.pecas.append(peca)
            peca.caixa = self.numero
            
            # Fechar caixa se atingir capacidade máxima
            if len(self.pecas) == self.CAPACIDADE_MAXIMA:
                self.fechar()
            
            return True
        return False
    
    def remover_peca(self, peca):
        """Remove uma peça da caixa"""
        if peca in self.pecas:
            self.pecas.remove(peca)
            peca.caixa = None
            # Reabrir caixa se estava fechada
            if self.fechada:
                self.fechada = False
            return True
        return False
    
    def fechar(self):
        """Fecha a caixa"""
        self.fechada = True
    
    def esta_cheia(self):
        """Verifica se a caixa está cheia"""
        return len(self.pecas) >= self.CAPACIDADE_MAXIMA
    
    def esta_vazia(self):
        """Verifica se a caixa está vazia"""
        return len(self.pecas) == 0
    
    def __str__(self):
        status = "FECHADA" if self.fechada else "ABERTA"
        return f"Caixa #{self.numero} - {len(self.pecas)}/{self.CAPACIDADE_MAXIMA} peças - Status: {status}"


class SistemaProducao:
    """Classe principal que gerencia todo o sistema de produção"""
    
    def __init__(self):
        self.pecas_aprovadas = []
        self.pecas_reprovadas = []
        self.todas_pecas = []  # Lista completa para controle de IDs
        self.caixas = []
        self.caixa_atual = None
        self.proximo_id = 1
    
    def cadastrar_peca(self, peso, cor, comprimento):
        """
        Cadastra uma nova peça no sistema
        Retorna a peça cadastrada
        """
        # Criar objeto da peça
        peca = Peca(self.proximo_id, peso, cor, comprimento)
        self.todas_pecas.append(peca)
        self.proximo_id += 1
        
        # Inspecionar qualidade
        if ControleQualidade.inspecionar_peca(peca):
            # Peça aprovada
            self.pecas_aprovadas.append(peca)
            self._armazenar_peca(peca)
            return peca, True, None
        else:
            # Peça reprovada
            self.pecas_reprovadas.append(peca)
            return peca, False, peca.motivos_reprovacao
    
    def _armazenar_peca(self, peca):
        """Armazena uma peça aprovada em uma caixa"""
        # Criar primeira caixa ou nova caixa se a atual estiver cheia
        if self.caixa_atual is None or self.caixa_atual.esta_cheia():
            nova_caixa = Caixa(len(self.caixas) + 1)
            self.caixas.append(nova_caixa)
            self.caixa_atual = nova_caixa
        
        # Adicionar peça à caixa atual
        self.caixa_atual.adicionar_peca(peca)
    
    def remover_peca(self, id_peca):
        """
        Remove uma peça cadastrada do sistema
        Retorna True se removida com sucesso, False caso contrário
        """
        peca_encontrada = None
        
        # Buscar peça
        for peca in self.todas_pecas:
            if peca.id == id_peca:
                peca_encontrada = peca
                break
        
        if not peca_encontrada:
            return False, "Peça não encontrada"
        
        # Remover de todas as listas
        self.todas_pecas.remove(peca_encontrada)
        
        if peca_encontrada.aprovada:
            self.pecas_aprovadas.remove(peca_encontrada)
            # Remover da caixa
            for caixa in self.caixas:
                if caixa.remover_peca(peca_encontrada):
                    # Remover caixa se ficou vazia
                    if caixa.esta_vazia():
                        self.caixas.remove(caixa)
                        # Atualizar caixa_atual se necessário
                        if self.caixa_atual == caixa:
                            self.caixa_atual = self.caixas[-1] if self.caixas else None
                    break
        else:
            self.pecas_reprovadas.remove(peca_encontrada)
        
        return True, "Peça removida com sucesso"
    
    def buscar_peca(self, id_peca):
        """Busca uma peça pelo ID"""
        for peca in self.todas_pecas:
            if peca.id == id_peca:
                return peca
        return None
    
    def listar_pecas_aprovadas(self):
        """Retorna lista de peças aprovadas"""
        return self.pecas_aprovadas.copy()
    
    def listar_pecas_reprovadas(self):
        """Retorna lista de peças reprovadas"""
        return self.pecas_reprovadas.copy()
    
    def listar_caixas_fechadas(self):
        """Retorna lista de caixas fechadas"""
        return [caixa for caixa in self.caixas if caixa.fechada]
    
    def processar_lote_csv(self, caminho_arquivo):
        """
        Processa peças em lote a partir de um arquivo CSV
        Retorna: (total_processadas, aprovadas, reprovadas, erros)
        """
        if not os.path.exists(caminho_arquivo):
            return 0, 0, 0, ["Arquivo não encontrado"]
        
        total_processadas = 0
        aprovadas = 0
        reprovadas = 0
        erros = []
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                
                # Verificar se o arquivo tem as colunas necessárias
                colunas_necessarias = {'peso', 'cor', 'comprimento'}
                colunas_arquivo = {col.lower().strip() for col in leitor.fieldnames}
                
                if not colunas_necessarias.issubset(colunas_arquivo):
                    return 0, 0, 0, [f"Arquivo CSV deve conter as colunas: {', '.join(colunas_necessarias)}"]
                
                # Processar cada linha
                for linha_num, linha in enumerate(leitor, start=2):  # start=2 pois linha 1 é cabeçalho
                    try:
                        # Extrair dados (com tratamento de case e espaços)
                        peso = float(linha['peso'].strip())
                        cor = linha['cor'].strip()
                        comprimento = float(linha['comprimento'].strip())
                        
                        # Cadastrar peça
                        peca, eh_aprovada, motivos = self.cadastrar_peca(peso, cor, comprimento)
                        total_processadas += 1
                        
                        if eh_aprovada:
                            aprovadas += 1
                        else:
                            reprovadas += 1
                    
                    except ValueError as e:
                        erros.append(f"Linha {linha_num}: Dados inválidos - {str(e)}")
                    except KeyError as e:
                        erros.append(f"Linha {linha_num}: Coluna ausente - {str(e)}")
                    except Exception as e:
                        erros.append(f"Linha {linha_num}: Erro inesperado - {str(e)}")
        
        except Exception as e:
            erros.append(f"Erro ao ler arquivo: {str(e)}")
        
        return total_processadas, aprovadas, reprovadas, erros
    
    def gerar_relatorio(self):
        """Gera relatório consolidado do processo de produção"""
        print("\n" + "="*70)
        print("RELATÓRIO CONSOLIDADO DE PRODUÇÃO E QUALIDADE")
        print("="*70)
        
        # Estatísticas gerais
        total_pecas = len(self.todas_pecas)
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   Total de peças processadas: {total_pecas}")
        print(f"   Peças aprovadas: {len(self.pecas_aprovadas)} ({self._calcular_percentual(len(self.pecas_aprovadas), total_pecas)}%)")
        print(f"   Peças reprovadas: {len(self.pecas_reprovadas)} ({self._calcular_percentual(len(self.pecas_reprovadas), total_pecas)}%)")
        
        # Análise de reprovações
        if self.pecas_reprovadas:
            print(f"\n❌ ANÁLISE DE REPROVAÇÕES:")
            motivos_count = {}
            
            for peca in self.pecas_reprovadas:
                for motivo in peca.motivos_reprovacao:
                    # Extrair categoria do motivo
                    categoria = motivo.split(' ')[0]
                    motivos_count[categoria] = motivos_count.get(categoria, 0) + 1
            
            for motivo, count in sorted(motivos_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {motivo}: {count} ocorrência(s)")
            
            print(f"\n   Detalhamento das peças reprovadas:")
            for peca in self.pecas_reprovadas:
                print(f"   • {peca}")
                for motivo in peca.motivos_reprovacao:
                    print(f"     └─ {motivo}")
        
        # Informações sobre caixas
        print(f"\n📦 ARMAZENAMENTO:")
        print(f"   Caixas utilizadas: {len(self.caixas)}")
        print(f"   Caixas fechadas: {len(self.listar_caixas_fechadas())}")
        
        for caixa in self.caixas:
            print(f"   • {caixa}")
            if caixa.pecas:
                ids_pecas = [str(p.id) for p in caixa.pecas]
                print(f"     └─ Peças: {', '.join(ids_pecas)}")
        
        # Taxa de eficiência
        if total_pecas > 0:
            eficiencia = (len(self.pecas_aprovadas) / total_pecas) * 100
            print(f"\n✨ EFICIÊNCIA DA LINHA: {eficiencia:.1f}%")
        
        print("="*70 + "\n")
    
    def _calcular_percentual(self, parte, total):
        """Calcula percentual com tratamento de divisão por zero"""
        if total == 0:
            return 0
        return round((parte / total) * 100, 1)


def limpar_tela():
    """Limpa a tela (multiplataforma)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa a execução até o usuário pressionar Enter"""
    input("\nPressione ENTER para continuar...")


def exibir_menu():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*70)
    print("🏭 SISTEMA DE CONTROLE DE QUALIDADE INDUSTRIAL")
    print("="*70)
    print("\n📋 MENU PRINCIPAL:\n")
    print("  1. Cadastrar nova peça")
    print("  2. Listar peças aprovadas/reprovadas")
    print("  3. Remover peça cadastrada")
    print("  4. Listar caixas fechadas")
    print("  5. Gerar relatório final")
    print("  6. Processar lote de peças (CSV)")
    print("  0. Sair do sistema")
    print("\n" + "="*70)


def opcao_cadastrar_peca(sistema):
    """Opção 1: Cadastrar nova peça"""
    print("\n" + "="*70)
    print("📝 CADASTRAR NOVA PEÇA")
    print("="*70)
    
    try:
        peso = float(input("\nPeso da peça (g): "))
        cor = input("Cor da peça: ").strip()
        comprimento = float(input("Comprimento da peça (cm): "))
        
        peca, aprovada, motivos = sistema.cadastrar_peca(peso, cor, comprimento)
        
        print(f"\n{'='*70}")
        if aprovada:
            print(f"✅ PEÇA APROVADA!")
            print(f"\n{peca}")
            print(f"Status: APROVADA")
            print(f"Armazenada na Caixa #{peca.caixa}")
        else:
            print(f"❌ PEÇA REPROVADA!")
            print(f"\n{peca}")
            print(f"Status: REPROVADA")
            print(f"\nMotivos da reprovação:")
            for motivo in motivos:
                print(f"  • {motivo}")
        print(f"{'='*70}")
        
    except ValueError:
        print("\n❌ Erro: Digite valores numéricos válidos para peso e comprimento.")
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar peça: {e}")
    
    pausar()


def opcao_listar_pecas(sistema):
    """Opção 2: Listar peças aprovadas/reprovadas"""
    print("\n" + "="*70)
    print("📊 LISTAR PEÇAS")
    print("="*70)
    print("\nEscolha uma opção:")
    print("  1. Listar peças aprovadas")
    print("  2. Listar peças reprovadas")
    print("  3. Listar todas as peças")
    
    opcao = input("\nOpção: ").strip()
    
    print("\n" + "="*70)
    
    if opcao == "1":
        pecas = sistema.listar_pecas_aprovadas()
        print("✅ PEÇAS APROVADAS")
        print("="*70)
        
        if not pecas:
            print("\nNenhuma peça aprovada cadastrada.")
        else:
            print(f"\nTotal: {len(pecas)} peça(s)\n")
            for peca in pecas:
                print(f"• {peca}")
                print(f"  Status: APROVADA | Caixa: #{peca.caixa}")
    
    elif opcao == "2":
        pecas = sistema.listar_pecas_reprovadas()
        print("❌ PEÇAS REPROVADAS")
        print("="*70)
        
        if not pecas:
            print("\nNenhuma peça reprovada cadastrada.")
        else:
            print(f"\nTotal: {len(pecas)} peça(s)\n")
            for peca in pecas:
                print(f"• {peca}")
                print(f"  Status: REPROVADA")
                print(f"  Motivos:")
                for motivo in peca.motivos_reprovacao:
                    print(f"    └─ {motivo}")
                print()
    
    elif opcao == "3":
        aprovadas = sistema.listar_pecas_aprovadas()
        reprovadas = sistema.listar_pecas_reprovadas()
        print("📋 TODAS AS PEÇAS")
        print("="*70)
        
        total = len(aprovadas) + len(reprovadas)
        if total == 0:
            print("\nNenhuma peça cadastrada.")
        else:
            print(f"\nTotal: {total} peça(s)")
            print(f"Aprovadas: {len(aprovadas)} | Reprovadas: {len(reprovadas)}\n")
            
            if aprovadas:
                print("✅ APROVADAS:")
                for peca in aprovadas:
                    print(f"  • {peca} | Caixa: #{peca.caixa}")
            
            if reprovadas:
                print("\n❌ REPROVADAS:")
                for peca in reprovadas:
                    print(f"  • {peca}")
    
    else:
        print("Opção inválida!")
    
    print("="*70)
    pausar()


def opcao_remover_peca(sistema):
    """Opção 3: Remover peça cadastrada"""
    print("\n" + "="*70)
    print("🗑️  REMOVER PEÇA")
    print("="*70)
    
    try:
        id_peca = int(input("\nDigite o ID da peça a ser removida: "))
        
        # Buscar peça antes de remover para exibir informações
        peca = sistema.buscar_peca(id_peca)
        
        if not peca:
            print(f"\n❌ Peça #{id_peca} não encontrada no sistema.")
        else:
            print(f"\n📦 Peça encontrada:")
            print(f"   {peca}")
            print(f"   Status: {'APROVADA' if peca.aprovada else 'REPROVADA'}")
            
            confirmar = input("\nConfirma a remoção? (S/N): ").strip().upper()
            
            if confirmar == 'S':
                sucesso, mensagem = sistema.remover_peca(id_peca)
                
                if sucesso:
                    print(f"\n✅ {mensagem}")
                else:
                    print(f"\n❌ {mensagem}")
            else:
                print("\n⚠️  Remoção cancelada.")
    
    except ValueError:
        print("\n❌ Erro: Digite um ID válido (número inteiro).")
    except Exception as e:
        print(f"\n❌ Erro ao remover peça: {e}")
    
    pausar()


def opcao_listar_caixas_fechadas(sistema):
    """Opção 4: Listar caixas fechadas"""
    print("\n" + "="*70)
    print("📦 CAIXAS FECHADAS")
    print("="*70)
    
    caixas_fechadas = sistema.listar_caixas_fechadas()
    
    if not caixas_fechadas:
        print("\nNenhuma caixa fechada no momento.")
    else:
        print(f"\nTotal de caixas fechadas: {len(caixas_fechadas)}\n")
        
        for caixa in caixas_fechadas:
            print(f"📦 {caixa}")
            print(f"   Conteúdo: {len(caixa.pecas)} peças")
            ids_pecas = [str(p.id) for p in caixa.pecas]
            print(f"   IDs das peças: {', '.join(ids_pecas)}")
            print()
    
    print("="*70)
    pausar()


def opcao_processar_lote_csv(sistema):
    """Opção 6: Processar lote de peças a partir de arquivo CSV"""
    print("\n" + "="*70)
    print("📂 PROCESSAR LOTE DE PEÇAS (CSV)")
    print("="*70)
    
    print("\n📋 Formato esperado do arquivo CSV:")
    print("   • Cabeçalho: peso,cor,comprimento")
    print("   • Exemplo de linha: 100,azul,15")
    print("   • Separador: vírgula (,)")
    print("   • Codificação: UTF-8")
    
    print("\n💡 Dica: Coloque o arquivo CSV na mesma pasta do programa")
    
    caminho = input("\nDigite o caminho do arquivo CSV: ").strip()
    
    if not caminho:
        print("\n❌ Caminho não informado.")
        pausar()
        return
    
    print(f"\n{'='*70}")
    print("🔄 Processando arquivo...")
    print(f"{'='*70}\n")
    
    # Processar lote
    total, aprovadas, reprovadas, erros = sistema.processar_lote_csv(caminho)
    
    print(f"{'='*70}")
    
    if total == 0 and erros:
        print("❌ ERRO NO PROCESSAMENTO")
        print(f"{'='*70}\n")
        for erro in erros:
            print(f"  • {erro}")
    else:
        print("✅ PROCESSAMENTO CONCLUÍDO")
        print(f"{'='*70}\n")
        print(f"📊 Resumo do processamento:")
        print(f"   • Total de peças processadas: {total}")
        print(f"   • Peças aprovadas: {aprovadas} ({sistema._calcular_percentual(aprovadas, total)}%)")
        print(f"   • Peças reprovadas: {reprovadas} ({sistema._calcular_percentual(reprovadas, total)}%)")
        print(f"   • Caixas criadas/utilizadas: {len(sistema.caixas)}")
        
        if erros:
            print(f"\n⚠️  Avisos/Erros encontrados ({len(erros)}):")
            for erro in erros[:10]:  # Mostrar no máximo 10 erros
                print(f"   • {erro}")
            if len(erros) > 10:
                print(f"   ... e mais {len(erros) - 10} erro(s)")
    
    print(f"{'='*70}")
    pausar()


def main():
    """Função principal do programa"""
    sistema = SistemaProducao()
    
    while True:
        limpar_tela()
        exibir_menu()
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                opcao_cadastrar_peca(sistema)
            
            elif opcao == "2":
                opcao_listar_pecas(sistema)
            
            elif opcao == "3":
                opcao_remover_peca(sistema)
            
            elif opcao == "4":
                opcao_listar_caixas_fechadas(sistema)
            
            elif opcao == "5":
                sistema.gerar_relatorio()
                pausar()
            
            elif opcao == "6":
                opcao_processar_lote_csv(sistema)
            
            elif opcao == "0":
                print("\n" + "="*70)
                print("👋 Encerrando o sistema...")
                print("Obrigado por utilizar o Sistema de Controle de Qualidade!")
                print("="*70 + "\n")
                break
            
            else:
                print("\n❌ Opção inválida! Escolha uma opção de 0 a 6.")
                pausar()
        
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("👋 Sistema interrompido pelo usuário.")
            print("="*70 + "\n")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            pausar()


# Ponto de entrada do programa
if __name__ == "__main__":
    main()