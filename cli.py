import argparse
import glob
import json
import os
import sys
import webbrowser

from signals import SIGNAL_CATALOG
from evaluator import avaliar_fluxo
from report_html import gerar_relatorio_html


def _print_resultado_terminal(r):
    print("=" * 70)
    print(f"Plataforma: {r.plataforma}")
    print(f"Fluxo:      {r.fluxo}")
    print(f"Canal:      {r.canal}")
    print(f"Nota de fricção: {r.nota_normalizada}/100  ->  {r.classificacao}")
    print("-" * 70)
    if r.sinais_disparados:
        print("Sinais de fricção detectados (do mais grave ao menos grave):")
        for s in r.sinais_disparados:
            print(f"  [{s.pontos:>4.1f} pts] ({s.categoria}) {s.pergunta}")
            print(f"            -> {s.detalhe}")
            print(f"            Recomendação: {s.recomendacao}")
    else:
        print("Nenhum sinal de fricção foi disparado.")
    if r.sinais_nao_observados:
        print("-" * 70)
        print(f"({len(r.sinais_nao_observados)} sinais não preenchidos nesta avaliação)")
    print("=" * 70)
    print()


def _gerar_html(resultados, caminho, titulo, abrir):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    gerar_relatorio_html(resultados, caminho, titulo=titulo)
    print(f"Relatório em HTML salvo em: {caminho}")
    if abrir:
        webbrowser.open(f"file://{os.path.abspath(caminho)}")


def cmd_evaluate(args):
    with open(args.arquivo, encoding="utf-8") as f:
        observacoes = json.load(f)
    resultado = avaliar_fluxo(observacoes)
    _print_resultado_terminal(resultado)

    if not args.sem_html:
        _gerar_html([resultado], args.out, titulo="avaliador de fricção", abrir=args.abrir)


def cmd_compare(args):
    arquivos = []
    for padrao in args.arquivos:
        arquivos.extend(glob.glob(padrao))
    if not arquivos:
        print("Nenhum arquivo encontrado para os padrões informados.")
        sys.exit(1)

    resultados = []
    for caminho in sorted(arquivos):
        with open(caminho, encoding="utf-8") as f:
            observacoes = json.load(f)
        resultados.append(avaliar_fluxo(observacoes))

    resultados.sort(key=lambda r: -r.nota_normalizada)

    print(f"\nComparação entre {len(resultados)} fluxo(s), do mais crítico ao menos crítico:\n")
    for r in resultados:
        _print_resultado_terminal(r)

    if not args.sem_html:
        _gerar_html(resultados, args.out, titulo="comparativo de fricção entre fluxos/plataformas", abrir=args.abrir)


def _pergunta_bool(pergunta):
    while True:
        resp = input(f"{pergunta} [s/n]: ").strip().lower()
        if resp in ("s", "sim", "y", "yes"):
            return True
        if resp in ("n", "nao", "não", "no"):
            return False
        print("Responda com 's' ou 'n'.")


def _pergunta_numerica(pergunta):
    while True:
        resp = input(f"{pergunta}: ").strip()
        if resp.isdigit():
            return int(resp)
        print("Digite um número inteiro.")


def cmd_interactive(args):
    print("=== Avaliador de Fricção — modo interativo ===")
    print("Responda com base no que você observou navegando o fluxo de verdade.\n")

    plataforma = input("Nome da plataforma avaliada (ex.: Rede Ipojuca): ").strip()
    fluxo = input("Nome do fluxo avaliado (ex.: Inscrição no Vale Ipojuca): ").strip()
    canal = input("Canal (Site / App / WhatsApp): ").strip()

    respostas = {}
    print()
    for sinal in SIGNAL_CATALOG:
        if sinal["tipo"] == "bool_problema":
            respostas[sinal["id"]] = _pergunta_bool(sinal["pergunta"])
        elif sinal["tipo"] == "numerico_limiar":
            respostas[sinal["id"]] = _pergunta_numerica(sinal["pergunta"])

    observacoes = {
        "plataforma": plataforma,
        "fluxo": fluxo,
        "canal": canal,
        "respostas": respostas,
    }

    resultado = avaliar_fluxo(observacoes)
    print()
    _print_resultado_terminal(resultado)

    salvar = input("Salvar essas observações em um arquivo JSON? [s/n]: ").strip().lower()
    if salvar in ("s", "sim"):
        nome_sugerido = f"examples/{plataforma.lower().replace(' ', '_')}_{fluxo.lower().replace(' ', '_')[:30]}.json"
        caminho = input(f"Caminho do arquivo [{nome_sugerido}]: ").strip() or nome_sugerido
        os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(observacoes, f, ensure_ascii=False, indent=2)
        print(f"Salvo em: {caminho}")

    gerar = input("Gerar relatório em HTML agora? [s/n]: ").strip().lower()
    if gerar in ("s", "sim"):
        caminho_html = input("Caminho do HTML [output/relatorio.html]: ").strip() or "output/relatorio.html"
        _gerar_html([resultado], caminho_html, titulo="avaliador de fricção", abrir=False)


def main():
    parser = argparse.ArgumentParser(
        description="Avaliador contínuo de experiência — protótipo Conecta Cidades."
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_eval = sub.add_parser("evaluate", help="Avalia um único arquivo de observações")
    p_eval.add_argument("arquivo", help="Caminho do arquivo JSON de observações")
    p_eval.add_argument("--out", default="output/relatorio.html", help="Caminho de saída do HTML (padrão: output/relatorio.html)")
    p_eval.add_argument("--sem-html", action="store_true", help="Não gerar o relatório em HTML, só mostrar no terminal")
    p_eval.add_argument("--abrir", action="store_true", help="Abrir o relatório no navegador automaticamente")
    p_eval.set_defaults(func=cmd_evaluate)

    p_cmp = sub.add_parser("compare", help="Compara vários arquivos de observações")
    p_cmp.add_argument("arquivos", nargs="+", help="Arquivos ou padrão glob, ex.: examples/*.json")
    p_cmp.add_argument("--out", default="output/comparativo.html", help="Caminho de saída do HTML (padrão: output/comparativo.html)")
    p_cmp.add_argument("--sem-html", action="store_true", help="Não gerar o relatório em HTML, só mostrar no terminal")
    p_cmp.add_argument("--abrir", action="store_true", help="Abrir o relatório no navegador automaticamente")
    p_cmp.set_defaults(func=cmd_compare)

    p_int = sub.add_parser("interactive", help="Preenche as observações respondendo perguntas no terminal")
    p_int.set_defaults(func=cmd_interactive)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
