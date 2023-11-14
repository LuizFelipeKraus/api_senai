# Documentação da API Senai

## Visão Geral
Esta documentação fornece informações sobre a API Senai, projetada para gerenciar usuários, produtos, categorias, endereços e pedidos. A API facilita o registro de usuários, login, gerenciamento de produtos e categorias, tratamento de endereços e processamento de pedidos.

## URL Base

## Endpoints

### Usuários
#### Registrar um novo usuário
- **Endpoint:** `/users/register/`
- **Método:** `POST`
- **Descrição:** Registrar um novo usuário com as informações fornecidas.

#### Login de Usuário
- **Endpoint:** `/users/login`
- **Método:** `POST`
- **Descrição:** Autenticar um usuário e gerar um token de acesso.

#### Logout de Usuário
- **Endpoint:** `/users/logout`
- **Método:** `POST`
- **Descrição:** Sair do usuário autenticado.

#### Obter todos os usuários
- **Endpoint:** `/users`
- **Método:** `GET`
- **Descrição:** Obter uma lista de todos os usuários.

### Produtos
#### Obter todos os produtos
- **Endpoint:** `/products`
- **Método:** `GET`
- **Descrição:** Obter uma lista de todos os produtos.

#### Obter um produto específico
- **Endpoint:** `/products/<int:product_id>`
- **Método:** `GET`
- **Descrição:** Obter detalhes de um produto específico usando seu ID.

### Categorias
#### Obter todas as categorias
- **Endpoint:** `/categories`
- **Método:** `GET`
- **Descrição:** Obter uma lista de todas as categorias de produtos.

#### Obter uma categoria específica
- **Endpoint:** `/categories/<int:category_id>`
- **Método:** `GET`
- **Descrição:** Obter detalhes de uma categoria específica usando seu ID.

### Endereços
#### Obter todos os endereços de um usuário
- **Endpoint:** `/users/address`
- **Método:** `GET`
- **Descrição:** Obter todos os endereços associados ao usuário autenticado.

#### Obter um endereço específico
- **Endpoint:** `/address/<int:address_id>`
- **Método:** `GET`
- **Descrição:** Obter detalhes de um endereço específico usando seu ID.

### Pedidos
#### Obter todos os pedidos
- **Endpoint:** `/orders`
- **Método:** `GET`
- **Descrição:** Obter uma lista de todos os pedidos.

#### Obter um pedido específico
- **Endpoint:** `/orders/<int:orders_id>`
- **Método:** `GET`
- **Descrição:** Obter detalhes de um pedido específico usando seu ID.

### Itens do Pedido
#### Obter todos os itens do pedido de um usuário
- **Endpoint:** `/orders/items/users`
- **Método:** `GET`
- **Descrição:** Obter todos os itens do pedido associados ao usuário autenticado.

#### Obter um item de pedido específico
- **Endpoint:** `/orders/items/<int:order_item_id>`
- **Método:** `GET`
- **Descrição:** Obter detalhes de um item de pedido específico usando seu ID.

#### Obter todos os itens do pedido dentro de um intervalo de datas
- **Endpoint:** `/orders/items/<string:start_date>/<string:end_date>`
- **Método:** `GET`
- **Descrição:** Obter todos os itens do pedido dentro do intervalo de datas especificado.

## Autenticação
Todas as solicitações, exceto o registro e login de usuários, exigem autenticação. Inclua o token de acesso no cabeçalho de Autorização:
Autorização: Bearer <access_token>


