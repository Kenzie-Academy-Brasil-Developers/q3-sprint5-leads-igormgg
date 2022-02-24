# URL base da API

https://leads-api-igor.herokuapp.com/

## Endpoints

Existem 4 endpoints nessa aplicação: Um pra registro de lead, um pra listagem dos registros, um pra atualização das visitas de um lead, e o último para deleção de um lead específico

### Registro

POST /leads

Essa rota serve para registrar um novo lead no banco de dados, sendo obrigatório passar no corpo da requisição o nome, email e telefone do lead a registrar. <br>
Exemplo de requisição:

```json
{
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "(41)90000-0000"
}
```

### Listagem

GET /leads

Essa segunda rota é usada para obter a listagem dos leads cadastrados no banco de dados. <br>
Aqui não é necessário passar nenhum dado no corpo da requisição.

### Atualização

PATCH /leads

Já a rota patch /leads pode ser usada para registrar a visita de um lead, aumentando em 1 o valor da coluna "visits" do lead no banco de dados. <br>
No corpo da requisição deve ser passado apenas o email do lead a atualizar. <br>
Exemplo de requisição:

```json
{
    "email": "john@email.com"
}
```

### Deleção

DELETE /leads <br/>

Por último, a requisição DELETE /leads pode ser usada para deletar um lead específico do banco de dados, sendo necessário passar apenas o email no corpo da requisição. <br>
Exemplo de requisição:

```json
{
    "email": "john@email.com"
}
```
