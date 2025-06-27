# 📖 EntreLivros

### _Sua biblioteca pessoal, compartilhada entre amigos._

<br>

![Status do Projeto](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)

Bem-vindo ao **EntreLivros**! Este projeto nasceu da ideia de criar uma forma simples e divertida para amigos compartilharem seus livros. Chega de livros acumulando poeira na estante! Com esta aplicação, você pode catalogar sua coleção, descobrir o que seus amigos estão lendo e gerenciar empréstimos de forma organizada.

---

### 🖼️ Demonstração Visual

*Tire um print da sua aplicação funcionando e coloque aqui! Isso faz toda a diferença. Para fazer isso, coloque a imagem na pasta `static` e use o caminho: `![Demonstração](static/nome_da_sua_imagem.png)`*

![Placeholder para a imagem da aplicação](https://i.imgur.com/lEGr84I.png)

---

### ✨ Funcionalidades Principais

* 👤 **Autenticação de Usuários:** Sistema completo de registro e login.
* 📚 **Gerenciamento de Livros:** CRUD completo (Adicionar, Ler, Atualizar e Deletar) para os livros do seu acervo pessoal.
* 🖼️ **Upload de Imagens:** Adicione uma capa para cada livro para deixar sua estante mais bonita.
* 🏷️ **Categorias e Filtros:** Organize e encontre livros por categoria (Ficção, Romance, etc.) e status (Disponível, Emprestado).
* 🔍 **Barra de Busca:** Pesquise livros em tempo real por título ou autor.
* 🤝 **Sistema de Empréstimos:** Um fluxo completo para solicitar, aprovar, negar e registrar a devolução de livros.
* 📊 **Painel Pessoal:** Uma área para gerenciar os empréstimos que você fez e os pedidos que recebeu.
* 👤 **Páginas de Perfil:** Visite o perfil de outros usuários para ver a coleção deles.
* 📱 **Design Responsivo:** Funciona bem tanto no computador quanto no celular.

---

### 🚀 Tecnologias Utilizadas

Este projeto foi construído do zero com as seguintes tecnologias:

* **Backend:**
    * **Python 3**
    * **Flask:** Um micro-framework leve e poderoso para criar a API.
    * **SQLite3:** Um banco de dados simples e baseado em arquivo, perfeito para projetos como este.

* **Frontend:**
    * **HTML5**
    * **CSS3** com **Tailwind CSS:** Para uma estilização rápida e moderna.
    * **JavaScript (Vanilla):** Todo o dinamismo da página foi construído com JavaScript puro, sem frameworks, para gerenciar a interação com o usuário e a comunicação com o backend.

---

### ⚙️ Como Rodar o Projeto Localmente

Para rodar este projeto na sua própria máquina, siga os passos:

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

5.  **Crie o banco de dados inicial:**
    ```bash
    python database.py
    ```

6.  **Rode a aplicação:**
    ```bash
    python app.py
    ```

7.  Abra seu navegador e acesse `http://127.0.0.1:5000`.

---

### 💡 Planos Futuros e Melhorias

Algumas ideias para evoluir o projeto:

* [ ] Sistema de avaliação com estrelas para os livros.
* [ ] Notificações no site para novos pedidos de empréstimo.
* [ ] Uma página de "Favoritos" ou "Lista de Desejos".

---

Feito com ❤️ por **[Seu Nome Aqui]**.

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/[seu-linkedin]/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/[SeuUsuario])
