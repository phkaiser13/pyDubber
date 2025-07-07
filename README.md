1.  **Pré-requisitos:**
    *   Python 3.9+
    *   FFmpeg instalado e acessível no PATH do sistema.
    *   Conta no [Hugging Face](https://huggingface.co/) para obter um token de acesso (para `pyannote`).
    *   Conta no [Google Cloud Platform](https://cloud.google.com/) com a API de Tradução ativada e um arquivo de credenciais (JSON).

2.  **Setup:**
    *   Crie uma pasta para o projeto: `mkdir PH-Dubber && cd PH-Dubber`
    *   Crie um ambiente virtual: `python -m venv venv`
    *   Ative o ambiente: `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows).
    *   Instale as dependências: `pip install -r requirements.txt`
    *   Configure as variáveis de ambiente:
        ```bash
        export HUGGING_FACE_TOKEN="seu_token_aqui"
        export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/seu/arquivo.json"
        ```

3.  **Execução:**
    *   No terminal, com o ambiente virtual ativado, execute o `main.py`:
        ```bash
        python main.py
        ```    *   Siga as instruções no terminal.
    *   Insira como input um video de outro idioma
    *   Aguarde o sistema.
    *   Retornará com um output 
