# 🗺️ Mapeamento de User Stories - [AgroLocal]

**Visão do Produto:** Uma plataforma de marketplace mobile que elimina intermediários, permitindo que produtores da agricultura familiar vendam diretamente para consumidores finais em cidades pequenas.

**Diferencial:** Foco total na logística rural (ponto de encontro/encomenda) e repasse automatizado via API de pagamento com retenção de taxa operacional.

---

## 🎭 Personas

1.  **O Produtor (Vendedor):** Agricultor familiar que busca escoar sua produção sem depender de atravessadores. Valoriza simplicidade e clareza sobre quando e quanto vai receber.
2.  **O Consumidor (Cliente):** Morador da cidade que busca produtos frescos, locais e deseja apoiar a economia da região com a conveniência de um app.
3.  **Administrador (Nós):** Responsável por gerir as taxas, validar cadastros e garantir a saúde financeira da plataforma.

---

## 📍 Backlog Funcional

### 📦 Módulo 1: Onboarding e Perfil (Mobile)
*Fluxo de entrada para ambos os perfis no App.*

#### [US-01] Cadastro de Produtor Rural
* **Como:** Produtor Rural.
* **Eu quero:** Criar uma conta informando dados cadastrais, localização e chave PIX vinculada ao meu CPF.
* **Para que:** Eu possa legalizar minha presença na plataforma e configurar o destino dos meus recebimentos.
* **Regras de Negócio:**
    * O sistema deve validar o formato do CPF.
    * A chave PIX é campo obrigatório para ativação da conta.
    * O endereço deve permitir coordenadas de GPS (para áreas rurais sem CEP preciso).

#### [US-02] Cadastro de Consumidor
* **Como:** Cliente final.
* **Eu quero:** Criar uma conta rápida (e-mail/senha ou social login) e cadastrar meus endereços de entrega.
* **Para que:** Eu possa realizar pedidos de forma ágil e segura.

---

### 📦 Módulo 2: Gestão de Ofertas (Visão Produtor - Mobile)
*Onde o produtor gerencia seu "estoque" vivo.*

#### [US-03] Criação de Oferta Flexível
* **Como:** Produtor Rural.
* **Eu quero:** Cadastrar um produto definindo se é "Pronta Entrega" ou "Por Encomenda", incluindo fotos e especificações (peso, unidade, maço).
* **Para que:** O cliente saiba exatamente o que está comprando e o tempo de espera necessário.

#### [US-04] Configuração de Logística Rural
* **Como:** Produtor Rural.
* **Eu quero:** Definir para cada oferta as modalidades de entrega disponíveis: Domiciliar (com taxa extra opcional), Ponto de Encontro (ex: Feira de Sábado) ou Retirada na Propriedade.
* **Para que:** Eu consiga vender conforme minha capacidade logística, sem obrigatoriedade de entregar em toda a cidade.

---

### 📦 Módulo 3: Experiência de Compra (Visão Cliente - Mobile)
*O "iFood" da agricultura familiar.*

#### [US-05] Vitrine Virtual Geolocalizada
* **Como:** Consumidor.
* **Eu quero:** Visualizar as ofertas disponíveis na minha região, filtrando por categoria (frutas, legumes, queijos) e distância.
* **Para que:** Eu encontre produtos frescos e evite fretes proibitivos.

#### [US-06] Checkout com Pagamento Integrado
* **Como:** Consumidor.
* **Eu quero:** Pagar via App (Cartão de Crédito/PIX) e escolher a forma de recebimento (entrega/ponto de encontro).
* **Para que:** A transação seja segura e eu não precise de dinheiro em espécie no ato da entrega.

---

### 📦 Módulo 4: Financeiro e Painel (Web Admin)
*O cérebro da operação (Backend + Web).*

#### [US-07] Split de Pagamento e Taxas
* **Como:** Administrador da Plataforma (Sistema).
* **Eu quero:** Que a API de pagamento retenha automaticamente a taxa de manutenção (X%) e agende o repasse do saldo líquido para o produtor.
* **Para que:** A plataforma seja sustentável e o repasse ocorra conforme o prazo estipulado, reduzindo bitributação e processos manuais.

#### [US-08] Gestão de Pedidos e Repasses (Dashboard)
* **Como:** Administrador.
* **Eu quero:** Uma visão Web completa de todos os pedidos, status de entrega e cronograma de pagamentos a vencer.
* **Para que:** Eu possa dar suporte (estornos, cancelamentos) e auditar o fluxo financeiro.