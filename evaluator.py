from dataclasses import dataclass, field
from signals import SIGNAL_CATALOG, get_max_score


def classificar_risco(nota_0_a_100):
    if nota_0_a_100 >= 60:
        return "ALTO risco de abandono"
    elif nota_0_a_100 >= 30:
        return "risco MÉDIO de abandono"
    else:
        return "risco BAIXO de abandono"


@dataclass
class SinalDisparado:
    id: str
    categoria: str
    pergunta: str
    pontos: float
    detalhe: str
    recomendacao: str


@dataclass
class ResultadoAvaliacao:
    plataforma: str
    fluxo: str
    canal: str
    nota_bruta: float
    nota_normalizada: float
    classificacao: str
    sinais_disparados: list = field(default_factory=list)
    sinais_nao_observados: list = field(default_factory=list)

    def por_categoria(self):
        cats = {}
        for s in self.sinais_disparados:
            cats.setdefault(s.categoria, 0)
            cats[s.categoria] += s.pontos
        return cats


def avaliar_fluxo(observacoes: dict) -> ResultadoAvaliacao:
    respostas = observacoes.get("respostas", {})
    disparados = []
    nao_observados = []
    nota_bruta = 0.0

    for sinal in SIGNAL_CATALOG:
        sid = sinal["id"]
        if sid not in respostas:
            nao_observados.append(sinal["pergunta"])
            continue

        valor = respostas[sid]

        if sinal["tipo"] == "bool_problema":
            if bool(valor):
                nota_bruta += sinal["peso"]
                disparados.append(SinalDisparado(
                    id=sid,
                    categoria=sinal["categoria"],
                    pergunta=sinal["pergunta"],
                    pontos=sinal["peso"],
                    detalhe="Observado: sim",
                    recomendacao=sinal["recomendacao"],
                ))

        elif sinal["tipo"] == "numerico_limiar":
            excesso = max(0, int(valor) - sinal["limiar"])
            pontos = min(excesso * sinal["peso_por_unidade"], sinal["peso_max"])
            if pontos > 0:
                nota_bruta += pontos
                disparados.append(SinalDisparado(
                    id=sid,
                    categoria=sinal["categoria"],
                    pergunta=sinal["pergunta"],
                    pontos=pontos,
                    detalhe=f"Observado: {valor} (limiar recomendado: "
                            f"{sinal['limiar']})",
                    recomendacao=sinal["recomendacao"],
                ))

    max_score = get_max_score()
    nota_normalizada = round((nota_bruta / max_score) * 100, 1) if max_score else 0

    return ResultadoAvaliacao(
        plataforma=observacoes.get("plataforma", "(não informado)"),
        fluxo=observacoes.get("fluxo", "(não informado)"),
        canal=observacoes.get("canal", "(não informado)"),
        nota_bruta=nota_bruta,
        nota_normalizada=nota_normalizada,
        classificacao=classificar_risco(nota_normalizada),
        sinais_disparados=sorted(disparados, key=lambda s: -s.pontos),
        sinais_nao_observados=nao_observados,
    )
