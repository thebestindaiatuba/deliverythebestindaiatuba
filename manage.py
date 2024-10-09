import os
import sys
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line

# Configuração mínima do Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurações do Django
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    STATIC_URL='/static/',
    STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')],
    SECRET_KEY='sua_chave_secreta_aqui',
)

# Produtos Açaí e Sorvete
produtos = [
    "Açaí Amarena",
    "Açaí Banana",
    "Açaí Creme Kinder",
    "Açaí Cupuaçu",
    "Açaí Diet",
    "Açaí Morango",
    "Açaí Mousse de Maracujá",
    "Açaí Ninho c/ Avelã",
    "Açaí Paçoca",
    "Açaí Pistache",
    "Açaí Tradicional",
    "Açaí Trufado Branco",
    "Sorbet Limão",
    "Sorbet Morango",
    "Sorbet Pitaya",
    "Sorvete Abacaxi",
    "Sorvete Blue Ice",
    "Sorvete Brownie",
    "Sorvete Charge Trufado",
    "Sorvete Chocomenta",
    "Sorvete Chocopipoca",
    "Sorvete Cupuaçu",
    "Sorvete Ferrero Rocher",
    "Sorvete Flocos",
    "Sorvete Iogurte Amarena",
    "Sorvete Laka Oreo",
    "Sorvete Maçã Encantada",
    "Sorvete Merengue",
    "Sorvete Mokaccino",
    "Sorvete Morango",
    "Sorvete Mousse de Maracujá",
    "Sorvete Ninho Trufado",
    "Sorvete Ovomaltine",
    "Sorvete Passas ao Rum",
    "Sorvete Pistache c/ Chocolate",
    "Sorvete Raffaello",
    "Sorvete Red Velvet",
    "Sorvete Unicórnio",
    "Sorvete Uva",
]

# Acompanhamentos disponíveis
acompanhamentos = [
    "Creme Chocolate c/ Avela",
    "Creme de Leitinho",
    "Creme de Amendoim",
    "Creme Wafer Branco",
    "Creme Chocotine",
    "Geleia de Morango",
    "Gelatina de Cereja",
    "Mel",
    "Creme Cookies & Cream",
    "Beijinho",
    "Brigadeiro",
    "Creme Chocobombom",
    "Cajuzinho",
    "Leite Condensado",
    "Gotas de Chocolate",
    "Confete",
    "Granulado",
    "Gelatina de Beijo",
    "Gelatina Cobrinha Cítrica",
    "Power Ball Chocolate",
    "Power Ball Choc. Branco",
    "Micro Ball",
    "Paçoca Rolha",
    "Paçoca Branca",
    "Paçoca Preta",
    "Tubetes de Chocolate",
    "Tubetes",
    "Leite em Pó",
    "Amendoim Granulado",
    "Ovomaltine",
    "Granola",
    "Cobertura Blue Ice",
    "Cobertura Chiclete",
    "Cobertura de Amora",
    "Cobertura de Banana",
    "Cobertura de Caramelo",
    "Cobertura de Choc. Meio Amargo",
    "Cobertura de Limão",
    "Cobertura de Menta",
    "Cobertura de Uva",
    "Cobertura Tutti Frutti",
    "Cobertura de Chocolate",
    "Cobertura de Morango",
    "Creme de Pistache",
    "Morango",
    "Banana",
    "Abacaxi",
    "Kiwi",
    "Manga",
    "Uva",
]

# Preços dos tamanhos e limites
precos = {
    "300ml": (19.90, 2, 3),  # (preço, max sabores, max acompanhamentos)
    "500ml": (29.90, 2, 3),
    "1kg": (55.90, 3, 4),
}

# 1. Função para exibir a página de seleção de tamanhos
def selecionar_tamanho(request):
    tamanhos = ''.join([f'<option value="{tamanho}">{tamanho} - R${preco[0]:.2f}</option>' for tamanho, preco in precos.items()])
    
    page = f'''
    <html>
    <head>
        <title>Selecione o Tamanho do Copo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;  
                color: #fff; 
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #6a1b9a;
            }}
            form {{
                background-color: #222; 
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                margin-top: 20px;
                max-width: 400px;
                margin-left: auto; 
                margin-right: auto; 
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin-bottom: 20px; 
            }}
            input[type="submit"] {{
                background-color: #6a1b9a;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            input[type="submit"]:hover {{
                background-color: #8e24aa;
            }}
        </style>
    </head>
    <body>
        <img src="/static/logo.png" alt="Logo">
        <h1>Selecione o Tamanho do Copo</h1>
        <form method="post" action="/sabores">
            <select name="tamanho">{tamanhos}</select>
            <input type="submit" value="Continuar">
        </form>
    </body>
    </html>
    '''
    return HttpResponse(page)

# 2. Função para exibir a página de seleção de sabores
def selecionar_sabores(request):
    tamanho = request.POST.get('tamanho')
    max_sabores = precos[tamanho][1]

    sabores_html = ''.join([f'<input type="checkbox" name="sabores" value="{sabor}">{sabor}<br>' for sabor in produtos])

    page = f'''
    <html>
    <head>
        <title>Selecione os Sabores</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #6a1b9a;
            }}
            form {{
                background-color: #222;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                margin-top: 20px;
                max-width: 400px;
                margin-left: auto;
                margin-right: auto;
                text-align: left;
            }}
            input[type="submit"] {{
                background-color: #6a1b9a;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            input[type="submit"]:hover {{
                background-color: #8e24aa;
            }}
        </style>
        <script>
            function validateForm() {{
                var checkboxes = document.querySelectorAll('input[name="sabores"]:checked');
                if (checkboxes.length > {max_sabores}) {{
                    alert('Você pode selecionar no máximo {max_sabores} sabores.');
                    return false;
                }}
                return true;
            }}
        </script>
    </head>
    <body>
        <img src="/static/logo.png" alt="Logo">
        <h1>Selecione os Sabores</h1>
        <form method="post" action="/acompanhamentos" onsubmit="return validateForm()">
            <h3>Sabores (máx {max_sabores}):</h3>
            {sabores_html}
            <input type="hidden" name="tamanho" value="{tamanho}">
            <input type="submit" value="Continuar">
        </form>
    </body>
    </html>
    '''
    return HttpResponse(page)

# 3. Função para exibir a página de seleção de acompanhamentos
def selecionar_acompanhamentos(request):
    sabores = request.POST.getlist('sabores')
    tamanho = request.POST.get('tamanho')
    max_acompanhamentos = precos[tamanho][2]

    acompanhamentos_html = ''.join([f'<input type="checkbox" name="acompanhamentos" value="{acompanhamento}">{acompanhamento}<br>' for acompanhamento in acompanhamentos])

    page = f'''
    <html>
    <head>
        <title>Selecione os Acompanhamentos</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #6a1b9a;
            }}
            form {{
                background-color: #222;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                margin-top: 20px;
                max-width: 400px;
                margin-left: auto;
                margin-right: auto;
                text-align: left;
            }}
            input[type="submit"] {{
                background-color: #6a1b9a;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            input[type="submit"]:hover {{
                background-color: #8e24aa;
            }}
        </style>
        <script>
            function validateForm() {{
                var checkboxes = document.querySelectorAll('input[name="acompanhamentos"]:checked');
                if (checkboxes.length > {max_acompanhamentos}) {{
                    alert('Você pode selecionar no máximo {max_acompanhamentos} acompanhamentos.');
                    return false;
                }}
                return true;
            }}
        </script>
    </head>
    <body>
        <img src="/static/logo.png" alt="Logo">
        <h1>Selecione os Acompanhamentos</h1>
        <form method="post" action="/tipo_entrega" onsubmit="return validateForm()">
            <h3>Acompanhamentos (máx {max_acompanhamentos}):</h3>
            {acompanhamentos_html}
            <input type="hidden" name="sabores" value="{'|'.join(sabores)}">
            <input type="hidden" name="tamanho" value="{tamanho}">
            <input type="submit" value="Continuar">
        </form>
    </body>
    </html>
    '''
    return HttpResponse(page)

# 4. Função para escolher entre entrega ou retirada
def tipo_entrega(request):
    sabores = request.POST.get('sabores')
    tamanho = request.POST.get('tamanho')
    acompanhamentos = request.POST.getlist('acompanhamentos')

    page = f'''
    <html>
    <head>
        <title>Tipo de Entrega</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #6a1b9a;
            }}
            form {{
                background-color: #222;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                margin-top: 20px;
                max-width: 400px;
                margin-left: auto;
                margin-right: auto;
                text-align: left;
            }}
            input[type="submit"] {{
                background-color: #6a1b9a;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            input[type="submit"]:hover {{
                background-color: #8e24aa;
            }}
        </style>
    </head>
    <body>
        <img src="/static/logo.png" alt="Logo">
        <h1>Selecione o Tipo de Entrega</h1>
        <form method="post" action="/confirmar_entrega">
            <input type="hidden" name="sabores" value="{sabores}">
            <input type="hidden" name="tamanho" value="{tamanho}">
            <input type="hidden" name="acompanhamentos" value="{'|'.join(acompanhamentos)}">
            <input type="radio" name="tipo_entrega" value="entrega" required> Entrega<br>
            <input type="radio" name="tipo_entrega" value="retirada" required> Retirada<br>
            <input type="text" name="endereco" placeholder="Endereço de Entrega" required id="endereco" style="display: none;">
            <input type="submit" value="Confirmar Pedido">
        </form>
        <script>
            const tipoEntrega = document.querySelectorAll('input[name="tipo_entrega"]');
            const enderecoInput = document.getElementById('endereco');

            tipoEntrega.forEach(radio => {{
                radio.addEventListener('change', function() {{
                    if (this.value === 'entrega') {{
                        enderecoInput.style.display = 'block';
                        enderecoInput.required = true;
                    }} else {{
                        enderecoInput.style.display = 'none';
                        enderecoInput.required = false;
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    '''
    return HttpResponse(page)

# 5. Função para confirmar entrega e enviar pedido via WhatsApp
def confirmar_entrega(request):
    sabores = request.POST.get('sabores')
    tamanho = request.POST.get('tamanho')
    acompanhamentos = request.POST.get('acompanhamentos')
    tipo_entrega = request.POST.get('tipo_entrega')
    endereco = request.POST.get('endereco') if tipo_entrega == "entrega" else "Retirada na loja"

    # Formatar a mensagem do pedido para WhatsApp
    mensagem = f"Pedido de The Best\nTamanho: {tamanho}\nSabores: {sabores}\nAcompanhamentos: {acompanhamentos}\nTipo de Entrega: {tipo_entrega}\nEndereço: {endereco}"
    mensagem_encoded = mensagem.replace("\n", "%0A")  # Codifica as novas linhas para URL
    whatsapp_url = f"https://wa.me/5519991403797?text={mensagem_encoded}"

    page = f'''
    <html>
    <head>
        <title>Confirmação da Entrega</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                color: #6a1b9a;
            }}
            .whatsapp-button {{
                background-color: #25D366; /* Cor do WhatsApp */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                width: auto;
                text-align: center;
                display: inline-block;
                margin-top: 20px;
                font-size: 16px;
                text-decoration: none;
                transition: background-color 0.3s;
            }}
            .whatsapp-button:hover {{
                background-color: #128C7E; /* Cor do WhatsApp ao passar o mouse */
            }}
            img {{
                width: 24px; /* Tamanho do ícone do WhatsApp */
                height: 24px;
                vertical-align: middle; /* Alinha o ícone ao texto */
                margin-right: 5px; /* Espaço entre o ícone e o texto */
            }}
        </style>
    </head>
    <body>
        <h1>Confirmação da Entrega</h1>
        <p>Você escolheu o tamanho: {tamanho}</p>
        <p>Sabores selecionados: {sabores}</p>
        <p>Acompanhamentos: {acompanhamentos}</p>
        <p>Tipo de Entrega: {tipo_entrega}</p>
        <p>Endereço de entrega: {endereco}</p>
        <p>Para enviar o seu pedido pelo WhatsApp, clique no botão abaixo:</p>
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-button">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">Enviar Pedido via WhatsApp
        </a>
        <p>Porque o melhor açaí é do seu jeito!</p>
    </body>
    </html>
    '''
    return HttpResponse(page)

# 6. URL Configuration
urlpatterns = [
    path('', selecionar_tamanho),
    path('sabores', selecionar_sabores),
    path('acompanhamentos', selecionar_acompanhamentos),
    path('tipo_entrega', tipo_entrega),
    path('confirmar_entrega', confirmar_entrega),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
