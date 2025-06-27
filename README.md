# 📖 EntreLivros: Sistema de Gerenciamento de Empréstimos

---

### Contexto do Projeto

Este projeto foi desenvolvido como **Projeto Aplicado Prático (PAPR)** para o curso de **Análise e Desenvolvimento de Sistemas**.

* **Instituição:** UNIASSELVI
* **Autor:** [Matheus da Rosa Paes]

<br>

**➡️ [Acesse a demonstração ao vivo aqui!](https://bit.ly/entrelivrosrp)**

![Placeholder para a imagem da aplicação](https://i.imgur.com/RfbcJoP.png)

---

### Sobre o Projeto

O **EntreLivros** é uma aplicação web full-stack desenvolvida para solucionar o problema de gerenciamento de empréstimos de livros entre amigos e pequenas comunidades. O objetivo é criar uma plataforma centralizada onde os usuários podem catalogar seus acervos, visualizar os livros de outros membros e administrar um sistema de solicitações de empréstimo de forma organizada e intuitiva.

A aplicação foi construída do zero, abrangendo desde a modelagem do banco de dados e desenvolvimento do backend com lógica de negócios, até a criação de uma interface de usuário interativa no frontend.

---

### ✨ Funcionalidades Principais

* 👤 **Autenticação de Usuários:** Sistema completo de registro e login.
* 📚 **Gerenciamento de Livros:** CRUD completo (Adicionar, Ler, Atualizar e Deletar) para os livros do acervo pessoal.
* 🖼️ **Upload de Imagens:** Adição de capas para cada livro.
* 🏷️ **Sistema de Categorias e Filtros:** Organização e busca por categoria e status (Disponível/Emprestado).
* 🔍 **Barra de Busca:** Pesquisa em tempo real por título ou autor.
* 🤝 **Sistema de Solicitação de Empréstimos:** Fluxo completo para solicitar, aprovar, negar e registrar a devolução de livros.
* 📊 **Painel Pessoal:** Área para gerenciar os empréstimos feitos e os pedidos recebidos.
* 👤 **Páginas de Perfil:** Visualização da coleção de outros usuários.
* 📱 **Design Responsivo:** Interface adaptável para computadores e celulares.

---

### 🚀 Tecnologias Utilizadas

Este projeto demonstra a aplicação prática das seguintes tecnologias:

* **Backend:**
    * **Python 3:** Linguagem principal para toda a lógica do servidor.
    * **Flask:** Micro-framework utilizado para construir a API RESTful que serve o frontend.
    * **SQLite3:** Banco de dados relacional baseado em arquivo para persistência de dados.

* **Frontend:**
    * **HTML5:** Estruturação do conteúdo da aplicação.
    * **CSS3** com **Tailwind CSS:** Para uma estilização rápida, moderna e responsiva.
    * **JavaScript (Vanilla):** Utilizado para criar toda a dinamicidade da interface (SPA - Single Page Application), manipular o DOM e se comunicar com a API do backend.

---

### ⚙️ Como Rodar o Projeto Localmente

Para executar e testar a aplicação em um ambiente de desenvolvimento:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)[SeuUsuario]/[nome-do-repositorio].git
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd [nome-do-repositorio]
    ```

3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Crie a estrutura inicial do banco de dados:**
    ```bash
    python database.py
    ```

6.  **Execute o servidor Flask:**
    ```bash
    python app.py
    ```

7.  Abra seu navegador e acesse `http://127.0.0.1:5000`.

---

Feito como parte da jornada de aprendizado em Análise e Desenvolvimento de Sistemas.
