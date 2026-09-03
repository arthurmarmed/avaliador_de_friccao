SIGNAL_CATALOG = [
    {
        "id": "login_terceiro_obrigatorio",
        "categoria": "Autenticação",
        "pergunta": "O fluxo exige login obrigatório via serviço de "
                     "terceiros (ex.: Gov.br) antes de iniciar a "
                     "solicitação?",
        "tipo": "bool_problema",
        "peso": 20,
        "recomendacao": (
            "Restringir a exigência de login via Gov.br apenas aos "
            "serviços que realmente necessitam dele, em vez de aplicá-la "
            "de forma padrão a todos os fluxos."
        ),
    },
    {
        "id": "nivel_conta_nao_informado",
        "categoria": "Autenticação",
        "pergunta": "O fluxo NÃO informa antecipadamente qual nível de "
                     "conta/verificação (ex.: Gov.br bronze/prata/ouro) "
                     "é exigido para aquele serviço específico?",
        "tipo": "bool_problema",
        "peso": 10,
        "recomendacao": (
            "Indicar de forma explícita, na tela do serviço, o nível de "
            "conta necessário, com um link direto para o cidadão "
            "verificar ou elevar seu nível antes de tentar."
        ),
    },
    {
        "id": "sem_canal_alternativo_login",
        "categoria": "Autenticação",
        "pergunta": "Caso o login falhe, o fluxo NÃO oferece nenhum "
                     "canal alternativo visível (presencial, telefone)?",
        "tipo": "bool_problema",
        "peso": 5,
        "recomendacao": (
            "Exibir uma opção alternativa (presencial/telefone/WhatsApp "
            "humano) quando o login falhar, em vez de apenas travar o "
            "fluxo."
        ),
    },
    {
        "id": "total_campos",
        "categoria": "Formulário",
        "pergunta": "Número total de campos do formulário",
        "tipo": "numerico_limiar",
        "limiar": 8,
        "peso_por_unidade": 4,
        "peso_max": 35,
        "recomendacao": (
            "Dividir o formulário em etapas curtas com indicador de "
            "progresso, em vez de uma lista longa de campos."
        ),
    },
    {
        "id": "campos_upload",
        "categoria": "Formulário",
        "pergunta": "Número de campos que exigem upload de documento/foto",
        "tipo": "numerico_limiar",
        "limiar": 2,
        "peso_por_unidade": 8,
        "peso_max": 40,
        "recomendacao": (
            "Reduzir a quantidade de uploads por formulário, ou permitir "
            "envio parcial com complementação posterior."
        ),
    },
    {
        "id": "documentos_nao_avisados",
        "categoria": "Formulário",
        "pergunta": "O formulário NÃO apresenta, antes de começar, uma "
                     "lista dos documentos que serão pedidos?",
        "tipo": "bool_problema",
        "peso": 30,
        "recomendacao": (
            "Mostrar a lista de documentos necessários antes do primeiro "
            "campo. Isso não elimina o abandono de quem não possui os "
            "documentos — essa pessoa provavelmente sairia de qualquer "
            "forma — mas evita que ela invista tempo preenchendo campos "
            "anteriores antes de descobrir o que falta, e aumenta a "
            "taxa de conclusão entre quem já está preparado."
        ),
    },
    {
        "id": "sem_salvar_progresso",
        "categoria": "Formulário",
        "pergunta": "O formulário NÃO salva o progresso automaticamente "
                     "se o cidadão sair para buscar um documento e "
                     "voltar depois?",
        "tipo": "bool_problema",
        "peso": 10,
        "recomendacao": (
            "Salvar o progresso do formulário automaticamente, "
            "permitindo retomar de onde parou."
        ),
    },
    {
        "id": "whatsapp_sem_contexto",
        "categoria": "Continuidade entre canais",
        "pergunta": "Ao ser direcionado ao WhatsApp a partir do site/app, "
                     "o cidadão perde o contexto do serviço que já "
                     "estava buscando (mensagem genérica, sem indicar "
                     "de qual página ele veio)?",
        "tipo": "bool_problema",
        "peso": 15,
        "recomendacao": (
            "Variar a mensagem pré-preenchida do WhatsApp por página, "
            "citando o nome do serviço de origem."
        ),
    },
    {
        "id": "login_nao_unificado",
        "categoria": "Continuidade entre canais",
        "pergunta": "O cidadão precisa se identificar novamente do zero "
                     "ao trocar de canal (ex.: site para app, ou app "
                     "para WhatsApp)?",
        "tipo": "bool_problema",
        "peso": 10,
        "recomendacao": (
            "Unificar a sessão/identificação do cidadão entre canais "
            "sempre que tecnicamente viável."
        ),
    },
    {
        "id": "meta_duplicada",
        "categoria": "Achabilidade",
        "pergunta": "As páginas de serviço têm título e descrição "
                     "(meta tags) genéricos/idênticos entre si, em vez "
                     "de específicos por serviço?",
        "tipo": "bool_problema",
        "peso": 10,
        "recomendacao": (
            "Definir título e meta-descrição únicos por página, citando "
            "o nome do serviço."
        ),
    },
    {
        "id": "conteudo_depende_js",
        "categoria": "Achabilidade",
        "pergunta": "O conteúdo da página só aparece depois de "
                     "JavaScript carregar (nada visível no HTML inicial)?",
        "tipo": "bool_problema",
        "peso": 8,
        "recomendacao": (
            "Renderizar ao menos o conteúdo essencial no servidor "
            "(SSR) para garantir indexação e carregamento mais rápido "
            "em conexões ruins."
        ),
    },
    {
        "id": "popup_bloqueante",
        "categoria": "Interrupções",
        "pergunta": "Um popup (ex.: 'instale o app') cobre o conteúdo "
                     "antes mesmo dele carregar?",
        "tipo": "bool_problema",
        "peso": 7,
        "recomendacao": (
            "Adiar a exibição do popup até depois do conteúdo "
            "carregar, ou torná-lo dispensável com um clique."
        ),
    },
]


def get_max_score():
    total = 0
    for s in SIGNAL_CATALOG:
        if s["tipo"] == "bool_problema":
            total += s["peso"]
        elif s["tipo"] == "numerico_limiar":
            total += s["peso_max"]
    return total
