# Avaliador de Fricção — protótipo Conecta Cidades

Protótipo de uma ferramenta que transforma observações de UX,
coletadas navegando um serviço de atendimento ao cidadão de verdade,
em uma nota de fricção de 0 a 100 com recomendações automáticas.

Feito como parte da avaliação de UX da Rede Ipojuca (site, app e
WhatsApp), respondendo à pergunta "quais pontos causam mais
fricção/abandono, e como identificar isso de forma contínua em
qualquer plataforma parceira".

## Como funciona

1. Um avaliador humano navega um fluxo real (agendamento, solicitação,
   inscrição, consulta) e responde a um catálogo fixo de perguntas
   sobre o que observou — ex.: "exige login obrigatório de terceiro?",
   "quantos campos tem o formulário?".
2. Cada resposta tem um peso de fricção associado.
3. A ferramenta soma os pesos, normaliza numa nota de 0 a 100,
   classifica o risco de abandono (baixo/médio/alto) e gera uma
   recomendação para cada problema identificado.

Não se conecta a nenhum backend real — funciona a partir
de observações estruturadas em arquivos JSON.

## Como rodar

Requisito: Python 3.9+. Nenhuma biblioteca externa é necessária.

```bash
python cli.py compare "examples/*.json" --abrir
```

Isso avalia todos os fluxos em `examples/`, mostra o resultado no
terminal e abre o relatório em `output/comparativo.html` no navegador.

Outros comandos:

```bash
python cli.py evaluate examples/rede_ipojuca_bolsa_escola.json  
```

Avalia um único fluxo específico, em vez de todos de uma vez


```bash
python cli.py interactive                                        
```

Responde as perguntas do catálogo direto no terminal.

## Generalizando para outra plataforma parceira

Basta criar um novo arquivo `.json` respondendo às mesmas perguntas de
`signals.py` — nenhuma linha de código muda. Exemplo:

```json
{
  "plataforma": "Nome da prefeitura",
  "fluxo": "Nome do serviço avaliado",
  "canal": "Site / App / WhatsApp",
  "respostas": {
    "login_terceiro_obrigatorio": true,
    "total_campos": 10,
    "campos_upload": 3
  }
}
```

Perguntas não respondidas aparecem como "não observadas" e não afetam
a nota.

## Relatório final

[Relatório de Avaliação de UX e Protótipo — Rede Ipojuca (PDF)](relatorio_final.pdf)

## Vídeo de demonstração

Assista aqui: https://youtu.be/RlbPM1t6mlA
