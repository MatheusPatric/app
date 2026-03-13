# 🚀 Gerador de Propostas Comerciais

Aplicação web profissional para criação e gerenciamento de propostas comerciais para clientes de marketing digital e gestão de redes sociais.

## ✨ Funcionalidades

### Dashboard Principal
- ✅ Visualização de todas as propostas criadas
- ✅ Criação de novas propostas com formulário completo
- ✅ Edição de propostas existentes
- ✅ Exclusão de propostas
- ✅ Interface moderna com tema preto e verde limão

### Gerador de Propostas
- ✅ Upload de logo do cliente
- ✅ Upload de imagem de capa
- ✅ Título e descrição personalizáveis
- ✅ Seção de visão geral da estratégia
- ✅ Planos de serviço dinâmicos (adicionar/remover)
- ✅ Funcionalidades customizáveis por plano
- ✅ Upload de mockup/preview visual
- ✅ Seção de resultados esperados
- ✅ Notas personalizadas
- ✅ Informações de contato no rodapé

### Página de Proposta
- ✅ URL única e compartilhável para cada proposta
- ✅ Design profissional tipo landing page
- ✅ Hero section com logo e título
- ✅ Cards de preços destacados
- ✅ Call-to-action para WhatsApp
- ✅ Exportação em PDF
- ✅ Copiar link da proposta
- ✅ Totalmente responsivo (mobile-first)

## 🛠️ Tecnologias Utilizadas

- **Next.js 14** - Framework React
- **MongoDB** - Banco de dados
- **TailwindCSS** - Estilização
- **shadcn/ui** - Componentes UI
- **jsPDF + html2canvas** - Exportação PDF
- **react-dropzone** - Upload de imagens
- **Lucide React** - Ícones

## 🎨 Design

- Tema moderno preto e verde limão
- Gradientes sutis e efeitos de hover
- Animações suaves
- Layout responsivo para todos os dispositivos
- Tipografia grande e impactante

## 🚀 Como Usar

1. **Acessar o Dashboard**
   - Abra a aplicação no navegador
   - Veja todas as suas propostas criadas

2. **Criar Nova Proposta**
   - Clique em "Nova Proposta"
   - Preencha as informações do cliente
   - Adicione logo e imagens
   - Configure os planos de serviço
   - Adicione funcionalidades a cada plano
   - Salve a proposta

3. **Compartilhar Proposta**
   - Clique em "Ver" na proposta desejada
   - Copie o link único gerado
   - Compartilhe com o cliente

4. **Exportar PDF**
   - Na página da proposta, clique em "Exportar PDF"
   - O PDF será gerado automaticamente

## 📱 URLs

- **Dashboard**: `/`
- **Proposta**: `/proposal/{id}`

## 🔗 API Endpoints

- `GET /api/proposals` - Listar todas as propostas
- `POST /api/proposals` - Criar nova proposta
- `GET /api/proposals/{id}` - Buscar proposta específica
- `PUT /api/proposals/{id}` - Atualizar proposta
- `DELETE /api/proposals/{id}` - Excluir proposta

## 💾 Estrutura de Dados

Cada proposta contém:
- Informações do cliente (nome, empresa, logo)
- Detalhes da proposta (título, descrição, imagens)
- Visão geral da estratégia
- Planos de serviço com preços e funcionalidades
- Preview visual (mockup)
- Resultados esperados
- Notas personalizadas
- Informações de contato e rodapé

## 🎯 Casos de Uso

Ideal para:
- Agências de marketing digital
- Freelancers de social media
- Consultores de marketing
- Gestores de conteúdo
- Profissionais de growth

## 📸 Recursos Visuais

- Design premium e minimalista
- Cards com efeitos hover
- Plano "popular" destacado
- Botões com gradientes
- Imagens otimizadas
- Scrollbar personalizado

## ✅ Status do Projeto

**Concluído e Funcionando:**
- ✅ Backend API completo (MongoDB)
- ✅ CRUD de propostas
- ✅ Upload de imagens (base64)
- ✅ Dashboard interativo
- ✅ Formulário de criação/edição
- ✅ Página de proposta compartilhável
- ✅ Exportação PDF
- ✅ Design responsivo
- ✅ Integração WhatsApp

---

Desenvolvido com ❤️ para profissionais de marketing digital
