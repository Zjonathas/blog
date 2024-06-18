# Blog feito com Django
Projeto de blog desenvolvido com o framework Django. O objetivo desse projeto é colocar meus conhecimentos adquiridos no curso sobre Django do Luiz Otávio Miranda em prática.
----------------------------
## Instruções
- Clone o repositório no seu ambiente de desenvolvimento com `git clone https://github.com/Zjonathas/blog.git`;
- Instale os requerimentos com `pip install -r requeriments.txt`;
- Copie e cole o .env-example e subsitua as informações. Lembre-se de nomear o novo arquivo como ".env";
- Rode os seguintes comandos para fazer as migrações `python manage.py makemigrations` e `python manage.py migrate`;
- Crie um superuser com `python manage.py createsuperuser`;
- Agora coloque o server no ar com `python manage.py runserver`;
- Faça login com o superuser no seguinte endereço 127.0.0.1/admin;
- Agora acesse o localhost e poderá começar a criar os seus posts;
- Para torná-los publicados, acesse 127.0.0.1/admin.
## Tecnologias usadas
- Django
- Djangosummernote
- Pillow
## Dicas
- Usar a seguinte classe em imagens adicionados ao conteúdo do post: img-content-post
