import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))


def _carregar_template() -> str:
    with open(os.path.join(PASTA_ATUAL, "template.html"), encoding="utf-8") as f:
        return f.read()


def _preencher(template: str, valores: dict) -> str:
    resultado = template
    for chave, valor in valores.items():
        resultado = resultado.replace("{{" + chave + "}}", str(valor))
    return resultado


def _escapar(texto) -> str:
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _tag_risco(classificacao: str) -> str:
    if "ALTO" in classificacao:
        return "[ALTO]"
    if "MÉDIO" in classificacao:
        return "[MEDIO]"
    return "[BAIXO]"


def _barra(nota: float, largura: int = 24) -> str:
    preenchido = round((nota / 100) * largura)
    preenchido = max(0, min(largura, preenchido))
    return "█" * preenchido + "░" * (largura - preenchido)


def _linha_resumo(r, indice: int) -> str:
    return f"""
    <tr>
      <td class="num">{indice:02d}</td>
      <td>{_escapar(r.plataforma)}</td>
      <td>{_escapar(r.fluxo)}</td>
      <td>{_escapar(r.canal)}</td>
      <td class="mono">{_barra(r.nota_normalizada)} {r.nota_normalizada:.1f}</td>
      <td class="mono tag">{_tag_risco(r.classificacao)}</td>
    </tr>"""


def _linha_sinal(s, indice: int) -> str:
    return f"""
    <tr>
      <td class="num">{indice:02d}</td>
      <td class="mono">{s.pontos:g}</td>
      <td>{_escapar(s.categoria)}</td>
      <td>
        {_escapar(s.pergunta)}
        <div class="detalhe">&gt; {_escapar(s.detalhe)}</div>
      </td>
      <td class="recomendacao">{_escapar(s.recomendacao)}</td>
    </tr>"""


def _bloco_detalhe(r, indice: int) -> str:
    cabecalho = f"[{indice:02d}] {r.plataforma} :: {r.fluxo} ({r.canal})"

    if r.sinais_disparados:
        linhas = "".join(
            _linha_sinal(s, i + 1) for i, s in enumerate(r.sinais_disparados)
        )
        tabela_sinais = f"""
        <table>
          <thead>
            <tr><th>#</th><th>pts</th><th>categoria</th><th>sinal observado</th><th>recomendação</th></tr>
          </thead>
          <tbody>{linhas}</tbody>
        </table>"""
    else:
        tabela_sinais = '<p class="vazio">-- nenhum sinal de fricção disparado --</p>'

    return f"""
    <section class="bloco-fluxo">
      <h2>{_escapar(cabecalho)}</h2>
      <p class="linha-nota">
        nota de fricção <span class="mono">{_barra(r.nota_normalizada)} {r.nota_normalizada:.1f}/100</span>
        &nbsp;&nbsp;{_tag_risco(r.classificacao)} {_escapar(r.classificacao)}
      </p>
      {tabela_sinais}
    </section>"""


def gerar_relatorio_html(resultados, caminho_saida: str,
                          titulo: str = "avaliador de fricção") -> str:
    template = _carregar_template()

    linhas_resumo = "".join(
        _linha_resumo(r, i + 1) for i, r in enumerate(resultados)
    )
    blocos_detalhe = "".join(
        _bloco_detalhe(r, i + 1) for i, r in enumerate(resultados)
    )

    html_final = _preencher(template, {
        "TITULO": _escapar(titulo),
        "SUBTITULO": "gerado a partir de observações estruturadas",
        "LINHAS_RESUMO": linhas_resumo,
        "BLOCOS_DETALHE": blocos_detalhe,
        "TOTAL_FLUXOS": str(len(resultados)),
    })

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html_final)
    return caminho_saida
