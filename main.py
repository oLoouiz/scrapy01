import scrapy

class PokeSpider(scrapy.Spider):
    name = 'pokespider'
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        # Seleciona as linhas da tabela de Pokémon
        linhas = response.css('table#pokedex > tbody > tr')

        # Itera por cada linha da tabela
        for linha in linhas:
            # Obtém o link para a página de detalhes do Pokémon
            coluna_href = linha.css('td:nth-child(2) > a::attr(href)').get()
            yield response.follow(coluna_href, self.parse_pokemon)

    def parse_pokemon(self, response):
        # Extrai informações sobre o Pokémon da página de detalhes
        link = response.css(
            '#main > div.infocard-list-evo > div:nth-child(1) > span.infocard-lg-data.text-muted > a::attr(href)').get()

        id = response.css('table.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
        nome = response.css('#main > h1::text').get()
        peso = response.css('table.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        altura = response.css('table.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        tipo1 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get()
        tipo2 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get()

        # Extrai informações sobre a primeira evolução, se houver
        linkEv1 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(3) > span.infocard-lg-data.text-muted > a::attr(href)').get()
        evolucao1 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(3) > span.infocard-lg-data.text-muted > a::text').get()
        id_evolucao1 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(3) > span.infocard-lg-data.text-muted > small:nth-child(1)::text').get()

        # Extrai informações sobre a segunda evolução, se houver
        linkEv2 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(5) > span.infocard-lg-data.text-muted > a::attr(href)').get()
        evolucao2 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(5) > span.infocard-lg-data.text-muted > a::text').get()
        id_evolucao2 = response.css(
            '#main > div.infocard-list-evo > div:nth-child(5) > span.infocard-lg-data.text-muted > small:nth-child(1)::text').get()

        # Extrai informações sobre as habilidades
        linkHab1 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(1) > a::attr(href)').get()
        habilidade1 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(1) > a::text').get()
        hab_desc1 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(1) > a[title]::attr(title)').get()

        linkHab2 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(3) > a::attr(href)').get()
        habilidade2 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(3) > a::text').get()
        hab_desc2 = response.css(
            'table.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(3) > a[title]::attr(title)').get()

        # Verifica se habilidade 1 existe antes de acessar hab_desc1
        if habilidade1:
            hab_desc1 = hab_desc1
        else:
            habilidade1 = None
            hab_desc1 = None

        # Verifica se a evolução 1 existe antes de acessá-la
        if evolucao1:
            linkEv1 = linkEv1
        else:
            linkEv1 = None
            evolucao1 = None
            id_evolucao1 = None

        # Verifica se a evolução 2 existe antes de acessá-la
        if evolucao2:
            linkEv2 = linkEv2
        else:
            linkEv2 = None
            evolucao2 = None
            id_evolucao2 = None

        # Retorna os dados coletados como um dicionário
        yield {
            'link': link,
            'id': id,
            'nome': nome,
            'peso': peso,
            'altura': altura,
            'tipo1': tipo1,
            'tipo2': tipo2,
            'link ev 1': linkEv1,
            'evolucao1': evolucao1,
            'id_evolucao1': id_evolucao1,
            'link ev 2': linkEv2,
            'evolucao2': evolucao2,
            'id_evolucao2': id_evolucao2,
            'link hab 1': linkHab1,
            'habilidade1': habilidade1,
            'hab_desc1': hab_desc1,
            'link hab 2': linkHab2,
            'habilidade2': habilidade2,
            'hab_desc2': hab_desc2,
        }
